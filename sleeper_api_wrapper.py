import os.path

import requests
from typing import Any, Dict, List, Optional

BASE = "https://api.sleeper.app/v1"


class SleeperAPI:
    def __init__(self, players_cache_path: str = r"C:\Projects\Sleeper\players.json"):
        self.session = requests.Session()
        # read players from file if provided file exists otherwise fetch from API
        if os.path.exists(players_cache_path):
            print("Loading players from cache file")
            import json
            with open(players_cache_path, "r") as f:
                self._cached_players = json.load(f)
        else:
            print("WARNING: Players cache file not found, fetching from API")
            self._cached_players = self.get_players()

    # -------------------------
    # USER ENDPOINTS
    # -------------------------

    def get_user(self, username: str) -> Dict[str, Any]:
        return self.session.get(f"{BASE}/user/{username}").json()

    def get_user_leagues(self, user_id: str, season: int, sport: str = "nfl") -> List[Dict[str, Any]]:
        return self.session.get(f"{BASE}/user/{user_id}/leagues/{sport}/{season}").json()

    def get_user_drafts(self, user_id: str, sport: str = "nfl") -> List[Dict[str, Any]]:
        return self.session.get(f"{BASE}/user/{user_id}/drafts/{sport}").json()

    # -------------------------
    # LEAGUE ENDPOINTS
    # -------------------------

    def get_league(self, league_id: str) -> Dict[str, Any]:
        return self.session.get(f"{BASE}/league/{league_id}").json()

    def get_league_users(self, league_id: str) -> List[Dict[str, Any]]:
        return self.session.get(f"{BASE}/league/{league_id}/users").json()

    def get_league_rosters(self, league_id: str) -> List[Dict[str, Any]]:
        return self.session.get(f"{BASE}/league/{league_id}/rosters").json()

    def get_league_matchups(self, league_id: str, week: int) -> List[Dict[str, Any]]:
        return self.session.get(f"{BASE}/league/{league_id}/matchups/{week}").json()

    def get_league_transactions(self, league_id: str, week: int) -> List[Dict[str, Any]]:
        return self.session.get(f"{BASE}/league/{league_id}/transactions/{week}").json()

    def get_league_winners_bracket(self, league_id: str):
        return self.session.get(f"{BASE}/league/{league_id}/winners_bracket").json()

    def get_league_losers_bracket(self, league_id: str):
        return self.session.get(f"{BASE}/league/{league_id}/losers_bracket").json()

    # -------------------------
    # DRAFT ENDPOINTS
    # -------------------------

    def get_draft(self, draft_id: str) -> Dict[str, Any]:
        return self.session.get(f"{BASE}/draft/{draft_id}").json()

    def get_draft_picks(self, draft_id: str) -> List[Dict[str, Any]]:
        return self.session.get(f"{BASE}/draft/{draft_id}/picks").json()

    def get_draft_traded_picks(self, draft_id: str) -> List[Dict[str, Any]]:
        return self.session.get(f"{BASE}/draft/{draft_id}/traded_picks").json()

    # -------------------------
    # PLAYERS ENDPOINTS
    # -------------------------

    def get_players(self, sport: str = "nfl") -> Dict[str, Any]:
        return self.session.get(f"{BASE}/players/{sport}").json()

    def get_trending_players(self, sport: str = "nfl", type_: str = "add", lookback_hours: int = 24):
        return self.session.get(
            f"{BASE}/players/{sport}/trending/{type_}?lookback_hours={lookback_hours}"
        ).json()

    # -------------------------
    # STATE & OTHER ENDPOINTS
    # -------------------------

    def get_state(self, sport: str = "nfl") -> Dict[str, Any]:
        return self.session.get(f"{BASE}/state/{sport}").json()

    def get_drafts_for_league(self, league_id: str) -> List[Dict[str, Any]]:
        return self.session.get(f"{BASE}/league/{league_id}/drafts").json()

    def get_avatar_url(self, avatar_id: str) -> str:
        return f"https://sleepercdn.com/avatars/{avatar_id}"

    # ======================================================================
    # HIGH-VALUE HELPER FUNCTIONS (COMBINE MULTIPLE ENDPOINTS)
    # ======================================================================
    def get_player_name_from_id(self, player_id: str) -> Optional[str]:
        player = self._cached_players.get(player_id)
        if player:
            return player.get("full_name")
        return None

    def get_all_previous_league_ids(self, current_id: str) -> Dict[str, str]:
        league = self.get_league(current_id)
        season = league.get("season")
        all_ids = {season: current_id}
        while league.get("previous_league_id"):
            previous_id = league.get("previous_league_id")
            league = self.get_league(previous_id)
            season = league.get("season")
            all_ids[season] = previous_id
        return all_ids

    def get_all_previous_drafts(self, current_league_id):
        league = self.get_league(current_league_id)
        season = league.get("season")
        drafts = {season: [d['draft_id'] for d in self.get_drafts_for_league(current_league_id)]}
        while league.get("previous_league_id"):
            previous_id = league.get("previous_league_id")
            league = self.get_league(previous_id)
            season = league.get("season")
            draft_list = [d["draft_id"] for d in self.get_drafts_for_league(previous_id)]
            drafts[season] = draft_list
        return drafts

    def get_player_drafted_with_pick(self, draft_id: str, draft_pick: Dict[str, Any]) -> Dict[str, Any]:
        draft_picks = self.get_draft_picks(draft_id)
        roster_id = draft_pick.get("roster_id")
        pick_round = draft_pick.get("round")
        draft = self.get_draft(draft_id)
        if not draft:
            return {"id": "", "round": pick_round, "slot": "", "season": draft_pick.get("season")}  # John Elway
        slots = draft.get("slot_to_roster_id", {})
        # get draft slot from the roster id
        draft_slot = None
        for slot, r_id in slots.items():
            if str(r_id) == str(roster_id):
                draft_slot = slot
                break
        for pick in draft_picks:
            if str(pick.get("draft_slot")) == str(draft_slot) and str(pick.get("round")) == str(pick_round):
                player_id = pick.get("player_id")
                player_name = self.get_player_name_from_id(player_id)
                return {"id": player_id, "name": player_name, "round": pick_round, "slot": draft_slot, "season": draft_pick.get("season")}
        return {"id": "4759", "round": "1", "slot": "1"}  # John Elway

    def get_all_trades_in_leagues(self, league_ids: List[str]) -> List[Dict[str, Any]]:
        all_trades = []
        for league_id in league_ids:
            for i in range(1, 25):
                trades = self.get_league_transactions(league_id, week=i)
                trade_list = [trade for trade in trades if trade['type'] == 'trade']
                all_trades.extend(trade_list)
        return all_trades

    def get_roster_name_by_roster_id(self, league_id: str, roster_id: str) -> Optional[str]:
        rosters = self.get_league_rosters(league_id)
        for roster in rosters:
            if str(roster.get("roster_id")) == str(roster_id):
                owner_id = roster.get("owner_id")
                return self.user_from_id(owner_id, league_id).get("display_name")
        return None

    def get_trade_info(self, trade: Dict[str, Any], current_league_id: str, drafts: Dict[str, str]) -> dict[Any, Any]:
        roster_ids = trade.get("roster_ids", [])
        trade_info = {}
        trade_changes = {k: {"additions": [], "subtractions": []} for k in roster_ids}
        draft_picks_info = trade.get("draft_picks", [])
        for pick in draft_picks_info:
            drafted_player = self.get_player_drafted_with_pick(
                draft_id=drafts.get(pick.get("season")),
                draft_pick=pick
            )
            new_owner = pick.get("owner_id")
            old_owner = pick.get("previous_owner_id")
            trade_changes[new_owner]["additions"].append(drafted_player)
            trade_changes[old_owner]["subtractions"].append(drafted_player)
        adds = trade.get("adds", {})
        if adds:
            for player_id in adds.keys():
                new_owner = adds[player_id]
                trade_changes[new_owner]["additions"].append({"id": player_id, "name": self.get_player_name_from_id(player_id)})
        drops = trade.get("drops", {})
        if drops:
            for player_id in drops.keys():
                old_owner = drops[player_id]
                trade_changes[old_owner]["subtractions"].append({"id": player_id, "name": self.get_player_name_from_id(player_id)})
        for roster_id, changes in trade_changes.items():
            roster_name = self.get_roster_name_by_roster_id(current_league_id, roster_id)
            trade_info[roster_name] = changes
        trade_info["time_created"] = trade.get("created")
        return trade_info




    def user_from_id(self, user_id: str, league_id: str) -> Dict[str, Any]:
        users = self.get_league_users(league_id)
        for user in users:
            if user.get("user_id") == user_id:
                return user
        return {}


# Example of basic usage:
# api = SleeperAPI()
# print(api.get_user("zgreen"))
# print(api.get_week_scores("league_id_here", 9))
