import json
from collections import Counter, defaultdict

def generate_frequent_player_wrapped(data):
    # Get the list of frequent players to filter by
    frequent_players = set(data.get('frequentNames', []))
    
    # Tracking dictionaries
    leads_count = Counter()
    leads_wins = Counter()
    leads_points = defaultdict(list)
    
    tm_count = Counter()
    tm_wins = Counter()
    
    clutch_wins = Counter()
    over_sellers = Counter()
    
    # Leader -> Teammate mapping
    partnerships = defaultdict(Counter)
    # Trio tracking
    trios = Counter()

    for game in data.get('pastGames', []):
        for rd in game.get('rounds', []):
            l = rd['leader']
            tms = rd['teammates']
            pts = rd['points']
            won = rd['result']
            
            # --- FILTERING LOGIC ---
            # We only record stats if the Leader is in our frequent list
            is_frequent_leader = l in frequent_players
            
            if is_frequent_leader:
                leads_count[l] += 1
                leads_points[l].append(pts)
                if won:
                    leads_wins[l] += 1
                    if pts > 200:
                        clutch_wins[l] += 1
                else:
                    over_sellers[l] += 1
            
            # Teammate Stats (only for frequent players)
            for tm in tms:
                if tm in frequent_players:
                    tm_count[tm] += 1
                    if is_frequent_leader:
                        partnerships[l][tm] += 1
                    if won:
                        tm_wins[tm] += 1
            
            # Unstoppable Trio (Only if all 3 are frequent players)
            if len(tms) == 2 and won:
                trio_members = [l] + tms
                if all(member in frequent_players for member in trio_members):
                    trio_key = " & ".join(sorted(trio_members))
                    trios[trio_key] += 1

    # --- PROCESSING RESULTS ---
    final_results = []
    for p in frequent_players:
        # Calculate stats for the frequent player
        avg_bid = sum(leads_points[p]) / len(leads_points[p]) if leads_points[p] else 0
        l_win_rate = (leads_wins[p] / leads_count[p] * 100) if leads_count[p] > 0 else 0
        tm_win_rate = (tm_wins[p] / tm_count[p] * 100) if tm_count[p] > 0 else 0
        fav_ally = partnerships[p].most_common(1)[0][0] if partnerships[p] else "None"

        final_results.append({
            "name": p,
            "avg_bid": round(avg_bid, 1),
            "l_win_rate": round(l_win_rate, 1),
            "clutch": clutch_wins[p],
            "called": tm_count[p],
            "tm_win_rate": round(tm_win_rate, 1),
            "over_sells": over_sellers[p],
            "fav_ally": fav_ally
        })

    # --- PRINTING THE RECAP ---
    print("═══ KALI TEERI WRAPPED (FREQUENT PLAYERS ONLY) ═══\n")

    def print_leaderboard(title, key_name, unit="", reverse=True):
        print(f"--- {title} ---")
        sorted_list = sorted(final_results, key=lambda x: x[key_name], reverse=reverse)
        for i, r in enumerate(sorted_list, 1):
            print(f"{i}. {r['name']}: {r[key_name]}{unit}")
        print()

    print_leaderboard("THE BOLD BIDDERS", "avg_bid", " pts")
    print_leaderboard("LEADER CONVERSION RATE", "l_win_rate", "%")
    print_leaderboard("CLUTCH LEADERS (>200 Wins)", "clutch")
    print_leaderboard("THE MOST WANTED (Times Called)", "called")
    print_leaderboard("THE KINGMAKERS (Teammate Win %)", "tm_win_rate", "%")
    print_leaderboard("THE OVER-SELLERS (Lead Losses)", "over_sells")
    
    print("--- FAVORITE ALLIES ---")
    for r in final_results:
        print(f"{r['name']} ➔ {r['fav_ally']}")

    print("\n--- UNSTOPPABLE TRIOS ---")
    if trios:
        for combo, count in trios.most_common(5):
            print(f"{combo}: {count} wins")
    else:
        print("No 3-player team wins recorded yet.")

# Usage
with open("data.json", "r") as f:
    game_data = json.load(f)
generate_frequent_player_wrapped(game_data)