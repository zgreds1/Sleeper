import json
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
            all_trades[league_id].extend(trade_list) if league_id in all_trades else all_trades.update({league_id: trade_list})
    return all_trades


def main():
    api = SleeperAPI()
    league = CHICKS
    league_id = league["current_league_id"]
    drafts = league["drafts"]
    all_league_ids = api.get_all_previous_league_ids(league_id)
    # print(all_league_ids)
    # print(json.dumps(api.get_all_trades_in_leagues(list(all_league_ids.values())), indent=2))
    all_trades = list_all_trades(api, list(all_league_ids.values()))
    # trade =   {
  #   "status": "complete",
  #   "type": "trade",
  #   "created": 1696511788029,
  #   "leg": 5,
  #   "draft_picks": [
  #     {
  #       "round": 3,
  #       "season": "2024",
  #       "roster_id": 8,
  #       "owner_id": 4,
  #       "previous_owner_id": 8
  #     }
  #   ],
  #   "creator": "1003048704657448960",
  #   "transaction_id": "1015647688369135616",
  #   "adds": {
  #     "4017": 4,
  #     "6790": 4,
  #     "8167": 4,
  #     "9758": 8
  #   },
  #   "drops": {
  #     "4017": 8,
  #     "6790": 8,
  #     "8167": 8,
  #     "9758": 4
  #   },
  #   "consenter_ids": [
  #     4,
  #     8
  #   ],
  #   "roster_ids": [
  #     4,
  #     8
  #   ],
  #   "status_updated": 1696521156611,
  #   "waiver_budget": []
  # }

    # trade_info = api.get_trade_info(trade, league_id, drafts)
    trade_infos = []
    for trade in all_trades.values():
        for t in trade:
            trade_infos.append(api.get_trade_info(t, league_id, drafts))
    # save to file
    with open("trades.json", "w") as f:
        json.dump(trade_infos, f, indent=2)
    print(json.dumps(trade_infos, indent=2))
    # print(json.dumps(api.get_trade_info(trade, league_id, drafts), indent=2))
    # print(api.get_roster_name_by_roster_id(league_id, "1"))
if __name__ == '__main__':
    # main()
    main()
