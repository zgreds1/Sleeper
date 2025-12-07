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
        """
        Get a user by username or user_id.

        Args:
            username (str): The username or user_id of the user.

        Returns:
            Dict[str, Any]: A dictionary containing user details.

        Example:
            >>> api.get_user("paswordistaco22")
            {
              "username": "paswordistaco22",
              "user_id": "404405834722852864",
              "display_name": "paswordistaco22",
              "avatar": "b7a486917eb76fc6b018fdd343fcf4e4",
              "is_bot": false,
              ...
            }
        """
        return self.session.get(f"{BASE}/user/{username}").json()

    def get_user_leagues(self, user_id: str, season: int, sport: str = "nfl") -> List[Dict[str, Any]]:
        """
        Get all leagues for a user in a specific season.

        Args:
            user_id (str): The ID of the user.
            season (int): The season year (e.g., 2024).
            sport (str, optional): The sport (default is "nfl").

        Returns:
            List[Dict[str, Any]]: A list of league dictionaries.

        Example:
            >>> api.get_user_leagues("404405834722852864", 2024)
            [
              {
                "league_id": "1123252569876344832",
                "name": "Dank Ass Keeper🏆",
                "season": "2024",
                "status": "complete",
                "sport": "nfl",
                "total_rosters": 12,
                ...
              },
              ...
            ]
        """
        return self.session.get(f"{BASE}/user/{user_id}/leagues/{sport}/{season}").json()

    def get_user_drafts(self, user_id: str, sport: str = "nfl") -> List[Dict[str, Any]]:
        """
        Get all drafts for a user.

        Args:
            user_id (str): The ID of the user.
            sport (str, optional): The sport (default is "nfl").

        Returns:
            List[Dict[str, Any]]: A list of draft dictionaries.

        Example:
            >>> api.get_user_drafts("404405834722852864")
            [
              {
                "draft_id": "1182986456149786625",
                "season": "2025",
                "status": "complete",
                "sport": "nfl",
                ...
              }
            ]
        """
        return self.session.get(f"{BASE}/user/{user_id}/drafts/{sport}").json()

    # -------------------------
    # LEAGUE ENDPOINTS
    # -------------------------

    def get_league(self, league_id: str) -> Dict[str, Any]:
        """
        Get a league by its ID.

        Args:
            league_id (str): The ID of the league.

        Returns:
            Dict[str, Any]: A dictionary containing league details.

        Example:
            >>> api.get_league("1182986456149786624")
            {
              "name": "Dankest Dynasty",
              "league_id": "1182986456149786624",
              "season": "2025",
              "status": "in_season",
              "total_rosters": 10,
              ...
            }
        """
        return self.session.get(f"{BASE}/league/{league_id}").json()

    def get_league_users(self, league_id: str) -> List[Dict[str, Any]]:
        """
        Get all users in a league.

        Args:
            league_id (str): The ID of the league.

        Returns:
            List[Dict[str, Any]]: A list of user dictionaries.

        Example:
            >>> api.get_league_users("1182986456149786624")
            [
              {
                "user_id": "404405834722852864",
                "display_name": "paswordistaco22",
                "league_id": "1182986456149786624",
                ...
              },
              ...
            ]
        """
        return self.session.get(f"{BASE}/league/{league_id}/users").json()

    def get_league_rosters(self, league_id: str) -> List[Dict[str, Any]]:
        """
        Get all rosters in a league.

        Args:
            league_id (str): The ID of the league.

        Returns:
            List[Dict[str, Any]]: A list of roster dictionaries.

        Example:
            >>> api.get_league_rosters("1182986456149786624")
            [
              {
                "roster_id": 1,
                "owner_id": "470017653449158656",
                "players": ["10229", "11435", ...],
                "starters": ["4984", "4046", ...],
                "settings": {"wins": 10, "losses": 3, ...},
                ...
              },
              ...
            ]
        """
        return self.session.get(f"{BASE}/league/{league_id}/rosters").json()

    def get_league_matchups(self, league_id: str, week: int) -> List[Dict[str, Any]]:
        """
        Get matchups for a specific week in a league.

        Args:
            league_id (str): The ID of the league.
            week (int): The week number.

        Returns:
            List[Dict[str, Any]]: A list of matchup dictionaries.

        Example:
            >>> api.get_league_matchups("1182986456149786624", 1)
            [
              {
                "matchup_id": 4,
                "roster_id": 1,
                "points": 158.88,
                "starters": ["4984", "5849", ...],
                ...
              },
              ...
            ]
        """
        return self.session.get(f"{BASE}/league/{league_id}/matchups/{week}").json()

    def get_league_transactions(self, league_id: str, week: int) -> List[Dict[str, Any]]:
        """
        Get all transactions (trades, waivers, free agents) for a specific week.

        Args:
            league_id (str): The ID of the league.
            week (int): The week number.

        Returns:
            List[Dict[str, Any]]: A list of transaction dictionaries.

        Example:
            >>> api.get_league_transactions("1182986456149786624", 1)
            [
              {
                "transaction_id": "1271379102917492736",
                "type": "free_agent",
                "status": "complete",
                "roster_ids": [1],
                "adds": null,
                "drops": {"12467": 1},
                ...
              },
              ...
            ]
        """
        return self.session.get(f"{BASE}/league/{league_id}/transactions/{week}").json()

    def get_league_winners_bracket(self, league_id: str):
        """
        Get the winners bracket for a league.

        Args:
            league_id (str): The ID of the league.

        Returns:
            List[Dict[str, Any]]: A list of bracket matches.

        Example:
            >>> api.get_league_winners_bracket("1182986456149786624")
            [
              {
                "r": 1,
                "m": 1,
                "t1": 4,
                "t2": 6,
                ...
              },
              ...
            ]
        """
        return self.session.get(f"{BASE}/league/{league_id}/winners_bracket").json()

    def get_league_losers_bracket(self, league_id: str):
        """
        Get the losers bracket for a league.

        Args:
            league_id (str): The ID of the league.

        Returns:
            List[Dict[str, Any]]: A list of bracket matches.

        Example:
            >>> api.get_league_losers_bracket("1182986456149786624")
            [
              {
                "r": 1,
                "m": 1,
                "t1": 8,
                "t2": 3,
                ...
              },
              ...
            ]
        """
        return self.session.get(f"{BASE}/league/{league_id}/losers_bracket").json()

    # -------------------------
    # DRAFT ENDPOINTS
    # -------------------------

    def get_draft(self, draft_id: str) -> Dict[str, Any]:
        """
        Get a draft by its ID.

        Args:
            draft_id (str): The ID of the draft.

        Returns:
            Dict[str, Any]: A dictionary containing draft details.

        Example:
            >>> api.get_draft("1182986456149786625")
            {
              "draft_id": "1182986456149786625",
              "status": "complete",
              "type": "linear",
              "season": "2025",
              "settings": {"rounds": 4, "teams": 10, ...},
              ...
            }
        """
        return self.session.get(f"{BASE}/draft/{draft_id}").json()

    def get_draft_picks(self, draft_id: str) -> List[Dict[str, Any]]:
        """
        Get all picks in a draft.

        Args:
            draft_id (str): The ID of the draft.

        Returns:
            List[Dict[str, Any]]: A list of pick dictionaries.

        Example:
            >>> api.get_draft_picks("1182986456149786625")
            [
              {
                "pick_no": 1,
                "round": 1,
                "draft_slot": 1,
                "player_id": "12527",
                "roster_id": 3,
                "picked_by": "404405834722852864",
                ...
              },
              ...
            ]
        """
        return self.session.get(f"{BASE}/draft/{draft_id}/picks").json()

    def get_draft_traded_picks(self, draft_id: str) -> List[Dict[str, Any]]:
        """
        Get all traded picks in a draft.

        Args:
            draft_id (str): The ID of the draft.

        Returns:
            List[Dict[str, Any]]: A list of traded pick dictionaries.

        Example:
            >>> api.get_draft_traded_picks("1182986456149786625")
            [
              {
                "season": "2025",
                "round": 1,
                "roster_id": 1,
                "owner_id": 10,
                "previous_owner_id": 3,
                ...
              },
              ...
            ]
        """
        return self.session.get(f"{BASE}/draft/{draft_id}/traded_picks").json()

    # -------------------------
    # PLAYERS ENDPOINTS
    # -------------------------

    def get_players(self, sport: str = "nfl") -> Dict[str, Any]:
        """
        Get all players for a sport.

        Args:
            sport (str, optional): The sport (default is "nfl").

        Returns:
            Dict[str, Any]: A dictionary of all players, keyed by player_id.

        Example:
            >>> api.get_players()
            {
              "1234": {
                "first_name": "Christian",
                "last_name": "McCaffrey",
                "position": "RB",
                ...
              },
              ...
            }
        """
        return self.session.get(f"{BASE}/players/{sport}").json()

    def get_trending_players(self, sport: str = "nfl", type_: str = "add", lookback_hours: int = 24):
        """
        Get trending players (adds or drops).

        Args:
            sport (str, optional): The sport (default is "nfl").
            type_ (str, optional): "add" or "drop" (default is "add").
            lookback_hours (int, optional): Hours to look back (default is 24).

        Returns:
            List[Dict[str, Any]]: A list of trending player dictionaries.

        Example:
            >>> api.get_trending_players()
            [
              {
                "count": 218856,
                "player_id": "12519"
              },
              ...
            ]
        """
        return self.session.get(
            f"{BASE}/players/{sport}/trending/{type_}?lookback_hours={lookback_hours}"
        ).json()

    # -------------------------
    # STATE & OTHER ENDPOINTS
    # -------------------------

    def get_state(self, sport: str = "nfl") -> Dict[str, Any]:
        """
        Get the current state of the sport (season, week, etc.).

        Args:
            sport (str, optional): The sport (default is "nfl").

        Returns:
            Dict[str, Any]: A dictionary containing state details.

        Example:
            >>> api.get_state()
            {
              "week": 14,
              "leg": 14,
              "season": "2025",
              "season_type": "regular",
              "league_season": "2025",
              ...
            }
        """
        return self.session.get(f"{BASE}/state/{sport}").json()

    def get_drafts_for_league(self, league_id: str) -> List[Dict[str, Any]]:
        """
        Get all drafts associated with a league.

        Args:
            league_id (str): The ID of the league.

        Returns:
            List[Dict[str, Any]]: A list of draft dictionaries.

        Example:
            >>> api.get_drafts_for_league("1182986456149786624")
            [
              {
                "draft_id": "1182986456149786625",
                "status": "complete",
                "season": "2025",
                ...
              }
            ]
        """
        return self.session.get(f"{BASE}/league/{league_id}/drafts").json()

    def get_avatar_url(self, avatar_id: str) -> str:
        """
        Get the full URL for an avatar ID.

        Args:
            avatar_id (str): The avatar ID.

        Returns:
            str: The URL of the avatar image.

        Example:
            >>> api.get_avatar_url("b7a486917eb76fc6b018fdd343fcf4e4")
            "https://sleepercdn.com/avatars/b7a486917eb76fc6b018fdd343fcf4e4"
        """
        return f"https://sleepercdn.com/avatars/{avatar_id}"

    # ======================================================================
    # HIGH-VALUE HELPER FUNCTIONS (COMBINE MULTIPLE ENDPOINTS)
    # ======================================================================
    def get_player_name_from_id(self, player_id: str) -> Optional[str]:
        """
        Get a player's full name from their ID using the cache.

        Args:
            player_id (str): The ID of the player.

        Returns:
            Optional[str]: The full name of the player, or None if not found.

        Example:
            >>> api.get_player_name_from_id("4046")
            "Patrick Mahomes"
        """
        player = self._cached_players.get(player_id)
        if player:
            return player.get("full_name")
        return None

    def get_all_previous_league_ids(self, current_id: str) -> Dict[str, str]:
        """
        Get all previous league IDs for a league, tracing back through history.

        Args:
            current_id (str): The current league ID.

        Returns:
            Dict[str, str]: A dictionary mapping season to league ID.

        Example:
            >>> api.get_all_previous_league_ids("1182986456149786624")
            {
              "2025": "1182986456149786624",
              "2024": "1080545431282696192",
              "2023": "1002944074959167488"
            }
        """
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
        """
        Get all previous drafts for a league, tracing back through history.

        Args:
            current_league_id (str): The current league ID.

        Returns:
            Dict[str, List[str]]: A dictionary mapping season to a list of draft IDs.

        Example:
            >>> api.get_all_previous_drafts("1182986456149786624")
            {
              "2025": ["1182986456149786625"],
              "2024": ["1080545431282696193"],
              ...
            }
        """
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
        """
        Find which player was drafted with a specific pick (e.g. for traded picks).

        Args:
            draft_id (str): The ID of the draft.
            draft_pick (Dict[str, Any]): The pick dictionary containing round, roster_id, season.

        Returns:
            Dict[str, Any]: A dictionary with player details (id, name, round, slot, season).

        Example:
            >>> api.get_player_drafted_with_pick("1182986456149786625", {"round": 1, "roster_id": 3, "season": "2025"})
            {
              "id": "12527",
              "name": "Ashton Jeanty",
              "round": 1,
              "slot": "1",
              "season": "2025"
            }
        """
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
        """
        Get all trades across multiple leagues (or seasons of a league).

        Args:
            league_ids (List[str]): A list of league IDs.

        Returns:
            List[Dict[str, Any]]: A list of trade transaction dictionaries.

        Example:
            >>> api.get_all_trades_in_leagues(["1182986456149786624"])
            [
              {
                "transaction_id": "...",
                "type": "trade",
                ...
              },
              ...
            ]
        """
        all_trades = []
        for league_id in league_ids:
            for i in range(1, 25):
                trades = self.get_league_transactions(league_id, week=i)
                trade_list = [trade for trade in trades if trade['type'] == 'trade']
                all_trades.extend(trade_list)
        return all_trades

    def get_roster_name_by_roster_id(self, league_id: str, roster_id: str) -> Optional[str]:
        """
        Get the display name of the owner of a roster.

        Args:
            league_id (str): The ID of the league.
            roster_id (str): The roster ID.

        Returns:
            Optional[str]: The display name of the owner, or None.

        Example:
            >>> api.get_roster_name_by_roster_id("1182986456149786624", "1")
            "ZFox3"
        """
        rosters = self.get_league_rosters(league_id)
        for roster in rosters:
            if str(roster.get("roster_id")) == str(roster_id):
                owner_id = roster.get("owner_id")
                return self.user_from_id(owner_id, league_id).get("display_name")
        return None

    def get_trade_info(self, trade: Dict[str, Any], current_league_id: str, drafts: Dict[str, str]) -> dict[Any, Any]:
        """
        Process a trade transaction into a readable format with player names and draft pick resolutions.

        Args:
            trade (Dict[str, Any]): The trade transaction dictionary.
            current_league_id (str): The current league ID (for roster names).
            drafts (Dict[str, str]): A mapping of season to draft ID (to resolve picks).

        Returns:
            dict[Any, Any]: A dictionary with roster names as keys, containing additions and subtractions.

        Example:
            >>> api.get_trade_info(trade_dict, "1182986456149786624", drafts_dict)
            {
              "paswordistaco22": {
                "additions": [{"id": "11569", "name": "Jarquez Hunter"}, ...],
                "subtractions": [{"id": "8205", "name": "Isiah Pacheco"}, ...]
              },
              "ZFox3": { ... },
              "time_created": 1754859515981
            }
        """
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
        """
        Get user details from a user ID within a league context.

        Args:
            user_id (str): The user ID.
            league_id (str): The league ID.

        Returns:
            Dict[str, Any]: The user dictionary.

        Example:
            >>> api.user_from_id("404405834722852864", "1182986456149786624")
            {
              "user_id": "404405834722852864",
              "display_name": "paswordistaco22",
              ...
            }
        """
        users = self.get_league_users(league_id)
        for user in users:
            if user.get("user_id") == user_id:
                return user
        return {}


# Example of basic usage:
# api = SleeperAPI()
# print(api.get_user("zgreen"))
# print(api.get_week_scores("league_id_here", 9))
