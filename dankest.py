import json
import csv
import re
import os
from typing import Dict, Any, List

from sleeper_api_wrapper import SleeperAPI

DANKEST = {"current_league_id": "1182986456149786624",
           "drafts": {'2025': '1182986456149786625',
                      '2024': '1080545431282696193',
                      '2023': '1002944076578250752'}}
CHICKS = {"current_league_id": "1204869865995771904",
          "drafts": {'2025': '1225933046436347904',
                     '2024': '1063120292207251457',
                     '2023': '918476323692089345',
                     '2022': '789660475934760961',
                     '2021': '709955959941840896'}}


def list_all_trades(api: SleeperAPI, league_ids: List[str]) -> Dict[str, Any]:
    all_trades = {}
    for league_id in league_ids:
        for week in range(1, 18):
            trades = api.get_league_transactions(league_id, week=week)  # week=0 to get all transactions
            trade_list = [trade for trade in trades if trade['type'] == 'trade']
            if league_id in all_trades:
                all_trades[league_id].extend(trade_list)
            else:
                all_trades[league_id] = trade_list
    return all_trades


def normalize_name(name):
    """Removes suffixes like Jr., III, etc. and lowercases for comparison."""
    if not name:
        return ""
    # Remove common suffixes
    name = re.sub(r'\s+(Jr\.?|Sr\.?|III|II|IV|V)(\s|$)', '', name, flags=re.IGNORECASE)
    # Remove special characters and extra spaces
    name = re.sub(r'[^\w\s]', '', name)
    return name.strip().lower()


def load_ktc_values(csv_path):
    ktc_values = {}
    if not os.path.exists(csv_path):
        print(f"Warning: KTC CSV not found at {csv_path}")
        return ktc_values

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Player value
            name = row.get('Player', row.get('Name', '')) # Adjust based on actual CSV header
            # Based on view_file, the header is "Updated...", "Position Rank", "Position", "Team", "Value", ...
            # Wait, the first column seems to be the name but has a weird header "Updated 12/07/25..."
            # Let's look at the file content again.
            # Line 1: Updated 12/07/25 at 01:20pm,Position Rank,Position,Team,Value,...
            # Line 2: Josh Allen,QB1,QB,BUF,9986,...
            # So the first column is the Name, but the header is "Updated...".
            # We can access it by index or by the weird header name.
            
            # Let's try to get the first key from the row
            keys = list(row.keys())
            if not keys:
                continue
            name = row[keys[0]]
            
            value_str = row.get('Value', '0')
            try:
                value = int(value_str)
            except ValueError:
                value = 0
            
            ktc_values[normalize_name(name)] = value
            
            # Store raw name too just in case
            ktc_values[name.lower()] = value
            
    return ktc_values


def get_pick_value(season, round_num, ktc_values):
    # Format: "2025 Mid 1st", "2025 Mid 2nd", etc.
    # User said: "If it is a pick (with no player) find the value of a mid pick in that round."
    
    suffix = "th"
    if round_num == 1: suffix = "st"
    elif round_num == 2: suffix = "nd"
    elif round_num == 3: suffix = "rd"
    
    query = f"{season} Mid {round_num}{suffix}"
    
    # Try to find it in KTC values
    # KTC format in CSV: "2027 Early 1st", "2026 Mid 1st", etc.
    # We need to match "Mid".
    
    # Let's construct the key
    key = normalize_name(query)
    if key in ktc_values:
        return ktc_values[key]
        
    # Fallback: Try "Early" or "Late" if Mid not found? 
    # Or maybe the year is too far out.
    # KTC usually has current + 3 years.
    
    return 0


def enrich_trades(trade_infos, ktc_values):
    for trade in trade_infos:
        for team, sides in trade.items():
            if team == 'time_created': continue
            
            # Process additions
            for asset in sides.get('additions', []):
                asset['value'] = 0
                if 'name' in asset and asset['name']:
                    # Player
                    norm_name = normalize_name(asset['name'])
                    if norm_name in ktc_values:
                        asset['value'] = ktc_values[norm_name]
                    else:
                        # Try exact match lower
                        if asset['name'].lower() in ktc_values:
                            asset['value'] = ktc_values[asset['name'].lower()]
                    if asset['value'] == 0:
                        print("Warning: Could not find value for player:", asset['name'])
                else:
                    # Pick
                    if 'season' in asset and 'round' in asset:
                        asset['value'] = get_pick_value(asset['season'], asset['round'], ktc_values)

            # Process subtractions
            for asset in sides.get('subtractions', []):
                asset['value'] = 0
                if 'name' in asset and asset['name']:
                    # Player
                    norm_name = normalize_name(asset['name'])
                    if norm_name in ktc_values:
                        asset['value'] = ktc_values[norm_name]
                    else:
                        if asset['name'].lower() in ktc_values:
                            asset['value'] = ktc_values[asset['name'].lower()]
                else:
                    # Pick
                    if 'season' in asset and 'round' in asset:
                        asset['value'] = get_pick_value(asset['season'], asset['round'], ktc_values)
    return trade_infos


def main():
    api = SleeperAPI()
    league = CHICKS
    league_id = league["current_league_id"]
    drafts = league["drafts"]
    
    # Load KTC Values
    # Assuming ktc.csv is in ktc_scraper/ktc.csv based on previous find
    ktc_path = os.path.join('ktc_scraper', 'ktc.csv')
    if not os.path.exists(ktc_path):
        ktc_path = 'ktc.csv' # Fallback
        
    print(f"Loading KTC values from {ktc_path}...")
    ktc_values = load_ktc_values(ktc_path)
    print(f"Loaded {len(ktc_values)} values.")

    all_league_ids = api.get_all_previous_league_ids(league_id)
    all_trades = list_all_trades(api, list(all_league_ids.values()))

    trade_infos = []
    for trade in all_trades.values():
        for t in trade:
            trade_infos.append(api.get_trade_info(t, league_id, drafts))
            
    # Enrich with values
    print("Enriching trades with values...")
    trade_infos = enrich_trades(trade_infos, ktc_values)

    # save to file
    with open("trades.json", "w") as f:
        json.dump(trade_infos, f, indent=2)
    

    print("Done. trades.json updated.")

if __name__ == '__main__':
    main()
