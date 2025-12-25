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
    
    # Leader -> Teammate mapping (for wins and losses)
    partnerships = defaultdict(Counter)
    partnership_losses = defaultdict(Counter)
    
    # Overall win rate tracking
    total_rounds = Counter()  # Total rounds participated (as leader or teammate)
    total_wins = Counter()    # Total wins (as leader or teammate)
    
    # Traitor tracking (points lost as teammate)
    tm_losses = Counter()     # Count of losses as teammate
    tm_points_lost = Counter()  # Total points lost when teammate (sum of bid points on losses)
    
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
                total_rounds[l] += 1
                if won:
                    leads_wins[l] += 1
                    total_wins[l] += 1
                    if pts >= 220:  # Changed to >=220 for "The Clutch" Factor
                        clutch_wins[l] += 1
                else:
                    over_sellers[l] += 1
            
            # Teammate Stats (only for frequent players)
            for tm in tms:
                if tm in frequent_players:
                    tm_count[tm] += 1
                    total_rounds[tm] += 1
                    if is_frequent_leader:
                        partnerships[l][tm] += 1
                        if not won:
                            partnership_losses[l][tm] += 1
                    if won:
                        tm_wins[tm] += 1
                        total_wins[tm] += 1
                    else:
                        tm_losses[tm] += 1
                        tm_points_lost[tm] += pts  # Track points lost when teammate loses
            
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
        
        # Overall Win Rate (Champion Stat)
        overall_win_rate = (total_wins[p] / total_rounds[p] * 100) if total_rounds[p] > 0 else 0
        
        # The Traitor (Net Point Loss as Teammate)
        avg_points_lost = (tm_points_lost[p] / tm_losses[p]) if tm_losses[p] > 0 else 0
        
        # Find nemesis (partnership with most losses)
        # Check both directions: when p is leader, and when p is teammate
        nemesis_losses = Counter()
        # When p is leader, track which teammates they lose with
        if partnership_losses[p]:
            for tm, loss_count in partnership_losses[p].items():
                nemesis_losses[tm] += loss_count
        # When p is teammate, track which leaders they lose with
        for leader in frequent_players:
            if p in partnership_losses[leader]:
                loss_count = partnership_losses[leader][p]
                nemesis_losses[leader] += loss_count
        
        nemesis = None
        if nemesis_losses:
            nemesis_player, nemesis_count = nemesis_losses.most_common(1)[0]
            if nemesis_count > 0:
                nemesis = nemesis_player

        final_results.append({
            "name": p,
            "avg_bid": round(avg_bid, 1),
            "l_win_rate": round(l_win_rate, 1),
            "clutch": clutch_wins[p],
            "called": tm_count[p],
            "tm_win_rate": round(tm_win_rate, 1),
            "over_sells": over_sellers[p],
            "fav_ally": fav_ally,
            "overall_win_rate": round(overall_win_rate, 1),
            "avg_points_lost": round(avg_points_lost, 1),
            "nemesis": nemesis
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
    print_leaderboard("CLUTCH LEADERS (≥220 Wins)", "clutch")
    print_leaderboard("THE MOST WANTED (Times Called)", "called")
    print_leaderboard("THE KINGMAKERS (Teammate Win %)", "tm_win_rate", "%")
    print_leaderboard("THE OVER-SELLERS (Lead Losses)", "over_sells")
    
    # NEW STATISTICS
    print_leaderboard("THE CHAMPIONS (Overall Win Rate)", "overall_win_rate", "%")
    print_leaderboard("THE TRAITORS (Avg Points Lost as Teammate)", "avg_points_lost", " pts", reverse=False)
    
    print("--- FAVORITE ALLIES ---")
    for r in final_results:
        print(f"{r['name']} ➔ {r['fav_ally']}")
    
    print("\n--- NEMESIS TRACKING (Worst Partnerships) ---")
    # Build a comprehensive list of all losing partnerships
    all_nemesis_pairs = []
    for leader in frequent_players:
        for teammate, loss_count in partnership_losses[leader].items():
            if teammate in frequent_players and loss_count > 0:
                all_nemesis_pairs.append({
                    "pair": f"{leader} + {teammate}",
                    "losses": loss_count
                })
    if all_nemesis_pairs:
        all_nemesis_pairs.sort(key=lambda x: x['losses'], reverse=True)
        for item in all_nemesis_pairs[:10]:  # Top 10 worst partnerships
            print(f"{item['pair']}: {item['losses']} losses")
    else:
        print("No nemesis partnerships recorded yet.")
    
    print("\n--- INDIVIDUAL NEMESIS (Each Player's Worst Partner) ---")
    for r in final_results:
        if r['nemesis'] and r['nemesis'] in frequent_players:
            # Calculate total losses with nemesis (both directions)
            losses_as_leader = partnership_losses[r['name']][r['nemesis']]
            losses_as_teammate = partnership_losses[r['nemesis']][r['name']] if r['nemesis'] in partnership_losses else 0
            total_losses = losses_as_leader + losses_as_teammate
            print(f"{r['name']} ↔ {r['nemesis']}: {total_losses} losses")

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