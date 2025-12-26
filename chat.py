import json
from collections import defaultdict, Counter
from itertools import combinations

DATA_FILE = "games.json"  # path to your JSON file


def load_data(file_path: str) -> dict:
    """Load JSON data from file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_leader_stats(data: dict):
    """
    Compute leader and team-related stats for each frequent player.
    Returns a dict with all stats grouped by type.
    """
    frequent_players = data.get("frequentNames", [])
    past_games = data.get("pastGames", [])

    # Initialize player stats
    stats = {player: {
        "rounds_played": 0,
        "rounds_as_leader": 0,
        "points_as_leader": 0,
        "clutch_leader_rounds": 0,
        "games_played": 0,
        "top_3_finishes": 0
    } for player in frequent_players}

    # Team stats
    teammate_counter = {player: Counter() for player in frequent_players}
    team_combinations = defaultdict(lambda: {"rounds_played": 0, "rounds_won": 0, "total_points": 0})

    # Process rounds
    for game in past_games:
        # Top 3 finishes
        scores = game.get("scores", {})
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top3 = [player for player, _ in sorted_scores[:3] if player in frequent_players]
        for player in top3:
            stats[player]["top_3_finishes"] += 1

        # Increment games played for frequent players in this game
        for player in game.get("players", []):
            if player in frequent_players:
                stats[player]["games_played"] += 1

        # Process rounds
        for round_data in game.get("rounds", []):
            leader = round_data.get("leader")
            teammates = round_data.get("teammates", [])
            points = round_data.get("points", 0)
            result = round_data.get("result", False)

            # Count rounds played for all participants
            for player in [leader] + teammates:
                if player in frequent_players:
                    stats[player]["rounds_played"] += 1

            # Leader stats
            if leader in frequent_players:
                stats[leader]["rounds_as_leader"] += 1
                stats[leader]["points_as_leader"] += points
                if points > 200:
                    stats[leader]["clutch_leader_rounds"] += 1

            # Teammate stats
            for player in teammates:
                if player in frequent_players:
                    teammate_counter[player].update(teammates)  # count all teammates
                    teammate_counter[player].subtract({player: 1})  # remove self-count

            # 3-person team combinations
            full_team = [leader] + teammates
            if all(p in frequent_players for p in full_team) and len(full_team) == 3:
                team_key = tuple(sorted(full_team))
                team_combinations[team_key]["rounds_played"] += 1
                if result:
                    team_combinations[team_key]["rounds_won"] += 1
                team_combinations[team_key]["total_points"] += points

    # Build labeled outputs
    output = {
        "Total Rounds Played": {},
        "Rounds as Leader": {},
        "% as Leader": {},
        "Avg Points per Round as Leader": {},
        "Clutch Rounds as Leader (>200 pts)": {},
        "% Clutch Rounds as Leader": {},
        "Top 3 Finishes": {},
        "Most Frequent Teammates (%)": {},
        "Most Successful 3-Person Teams": {}
    }

    # Player stats
    for player in frequent_players:
        sp = stats[player]
        rounds_played = sp["rounds_played"]
        rounds_as_leader = sp["rounds_as_leader"]
        points_as_leader = sp["points_as_leader"]
        clutch_rounds = sp["clutch_leader_rounds"]

        output["Total Rounds Played"][player] = rounds_played
        output["Rounds as Leader"][player] = rounds_as_leader
        output["% as Leader"][player] = round((rounds_as_leader / rounds_played * 100) if rounds_played > 0 else 0, 1)
        output["Avg Points per Round as Leader"][player] = round((points_as_leader / rounds_as_leader) if rounds_as_leader > 0 else 0, 1)
        output["Clutch Rounds as Leader (>200 pts)"][player] = clutch_rounds
        output["% Clutch Rounds as Leader"][player] = round((clutch_rounds / rounds_as_leader * 100) if rounds_as_leader > 0 else 0, 1)
        output["Top 3 Finishes"][player] = sp["top_3_finishes"]

        # Most frequent teammates as percentages
        most_common_teammates = teammate_counter[player].most_common(3)
        teammate_percentages = [
            f"{p} ({round((c / rounds_played * 100), 1)}%)" for p, c in most_common_teammates
        ]
        output["Most Frequent Teammates (%)"][player] = teammate_percentages

    # Most Successful 3-Person Teams
    team_stats_list = []
    for team, vals in team_combinations.items():
        rounds_played = vals["rounds_played"]
        rounds_won = vals["rounds_won"]
        avg_points = round(vals["total_points"] / rounds_played if rounds_played > 0 else 0, 1)
        win_rate = round((rounds_won / rounds_played * 100) if rounds_played > 0 else 0, 1)
        team_stats_list.append((team, rounds_played, rounds_won, win_rate, avg_points))

    # Top 10 teams
    team_stats_list.sort(key=lambda x: (x[3], x[2]), reverse=True)
    output["Most Successful 3-Person Teams"] = [
        f"{', '.join(team)}: {rounds_played} rounds, {rounds_won} wins, {win_rate}% win, {avg_points} avg pts"
        for team, rounds_played, rounds_won, win_rate, avg_points in team_stats_list[:10]
    ]

    return output


def main():
    data = load_data(DATA_FILE)
    stats = compute_leader_stats(data)

    # Print grouped stats
    for stat_name, stat_dict in stats.items():
        print(f"\n{stat_name}:")
        if isinstance(stat_dict, dict):
            for player, value in stat_dict.items():
                print(f"{player}: {value}")
        else:  # list of strings (for teams)
            for value in stat_dict:
                print(value)


if __name__ == "__main__":
    main()
