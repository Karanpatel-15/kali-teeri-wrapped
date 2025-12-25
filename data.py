import json
from collections import Counter, defaultdict

def calculate_stats(data):
    """
    Calculate all statistics for Kali Teeri Wrapped 2025.
    Only processes players in frequentNames array, ignores "Guest" players.
    """
    # Get the list of frequent players to filter by
    frequent_players = set(data.get('frequentNames', []))
    
    # Statistics tracking dictionaries
    games_played = defaultdict(set)  # Track unique games each player participated in
    total_rounds = Counter()  # Total rounds participated (as leader or teammate)
    total_wins = Counter()    # Total wins (as leader or teammate)
    
    # Leader stats
    leader_count = Counter()  # Total times bidding/leading
    leader_wins = Counter()   # Total wins as leader
    clutch_wins = Counter()   # Wins as leader with bid >= 200
    
    # Teammate stats
    teammate_count = Counter()  # Total times called as teammate
    teammate_wins = Counter()   # Total wins as teammate
    
    # Trio tracking (only for games with 8+ players)
    trios = Counter()  # Key: sorted tuple of 3 names, Value: win count
    
    # Process all games and rounds
    for game_idx, game in enumerate(data.get('pastGames', [])):
        game_players = set(game.get('players', []))
        num_players = len(game_players)
        
        # Only process trios for games with 8 or more players
        process_trios = num_players >= 8
        
        for rd in game.get('rounds', []):
            leader = rd['leader']
            teammates = rd['teammates']
            points = rd['points']
            won = rd['result']
            
            # Only process if leader is in frequentNames (ignore Guest players)
            if leader not in frequent_players:
                continue
            
            # Count as leader
            leader_count[leader] += 1
            total_rounds[leader] += 1
            games_played[leader].add(game_idx)
            
            if won:
                leader_wins[leader] += 1
                total_wins[leader] += 1
                
                # Check for clutch win (bid >= 200)
                if points >= 200:
                    clutch_wins[leader] += 1
            
            # Process teammates (only if they're in frequentNames)
            for tm in teammates:
                if tm not in frequent_players:
                    continue
                
                # Count as teammate
                teammate_count[tm] += 1
                total_rounds[tm] += 1
                games_played[tm].add(game_idx)
                
                if won:
                    teammate_wins[tm] += 1
                    total_wins[tm] += 1
            
            # Track trios (only for games with 8+ players, and all must be frequent players)
            if process_trios and won and len(teammates) == 2:
                trio_members = [leader] + teammates
                if all(member in frequent_players for member in trio_members):
                    trio_key = tuple(sorted(trio_members))
                    trios[trio_key] += 1
    
    # Calculate Podium Finishes (1st, 2nd, 3rd place)
    podium_counts = {
        '1st': Counter(),
        '2nd': Counter(),
        '3rd': Counter()
    }
    
    for game in data.get('pastGames', []):
        scores = game.get('scores', {})
        if not scores:
            continue
        
        # Sort players by score (descending)
        sorted_players = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Assign podium positions (only to frequent players)
        for position, (player, score) in enumerate(sorted_players[:3], 1):
            if player in frequent_players:
                if position == 1:
                    podium_counts['1st'][player] += 1
                elif position == 2:
                    podium_counts['2nd'][player] += 1
                elif position == 3:
                    podium_counts['3rd'][player] += 1
    
    # Calculate statistics for each frequent player
    player_stats = {}
    
    for player in frequent_players:
        # Most Active (Games Played)
        games_count = len(games_played[player])
        
        # Round Win %: (Total wins) / (Total rounds participated)
        round_win_pct = (total_wins[player] / total_rounds[player] * 100) if total_rounds[player] > 0 else 0
        
        # Leader Conversion Rate: (Wins as leader) / (Times bidding/leading)
        leader_conv_rate = (leader_wins[player] / leader_count[player] * 100) if leader_count[player] > 0 else 0
        
        # The Clutch Player: Total wins as leader with bid >= 200
        clutch_count = clutch_wins[player]
        
        # Teammate Win Rate: (Wins as teammate) / (Times called as teammate)
        teammate_win_rate = (teammate_wins[player] / teammate_count[player] * 100) if teammate_count[player] > 0 else 0
        
        # Podium finishes
        podium_1st = podium_counts['1st'][player]
        
        player_stats[player] = {
            'games_played': games_count,
            'round_win_pct': round(round_win_pct, 1),
            'leader_conv_rate': round(leader_conv_rate, 1),
            'clutch_wins': clutch_count,
            'teammate_count': teammate_count[player],
            'teammate_win_rate': round(teammate_win_rate, 1),
            'podium_1st': podium_1st
        }
    
    # Find The Most Wanted (most called as teammate)
    most_wanted_player = None
    most_wanted_count = 0
    for player in frequent_players:
        if teammate_count[player] > most_wanted_count:
            most_wanted_count = teammate_count[player]
            most_wanted_player = player
    
    # Find The Clutch King (most clutch wins)
    clutch_king = None
    clutch_king_count = 0
    for player in frequent_players:
        if clutch_wins[player] > clutch_king_count:
            clutch_king_count = clutch_wins[player]
            clutch_king = player
    
    # Find Unstoppable Trio (top trio with most wins)
    unstoppable_trio = None
    unstoppable_trio_wins = 0
    if trios:
        top_trio_key, unstoppable_trio_wins = trios.most_common(1)[0]
        unstoppable_trio = list(top_trio_key)
    
    return {
        'player_stats': player_stats,
        'most_wanted': {'player': most_wanted_player, 'count': most_wanted_count},
        'clutch_king': {'player': clutch_king, 'count': clutch_king_count},
        'unstoppable_trio': {'players': unstoppable_trio, 'wins': unstoppable_trio_wins}
    }


def print_stats(stats):
    """Print all statistics to console for verification."""
    player_stats = stats['player_stats']
    
    print("=" * 60)
    print("KALI TEERI WRAPPED 2025 - STATISTICS")
    print("=" * 60)
    print()
    
    # Most Active (Games Played)
    print("--- THE ACTIVE LEGENDS (Games Played) ---")
    sorted_games = sorted(player_stats.items(), key=lambda x: x[1]['games_played'], reverse=True)
    for i, (player, data) in enumerate(sorted_games, 1):
        print(f"{i}. {player}: {data['games_played']} games")
    print()
    
    # Round Win % (Champions)
    print("--- THE CHAMPIONS (Round Win %) ---")
    sorted_win_pct = sorted(player_stats.items(), key=lambda x: x[1]['round_win_pct'], reverse=True)
    for i, (player, data) in enumerate(sorted_win_pct, 1):
        print(f"{i}. {player}: {data['round_win_pct']}%")
    print()
    
    # Leader Conversion Rate (Closers)
    print("--- THE CLOSERS (Leader Conversion Rate) ---")
    sorted_conv = sorted(player_stats.items(), key=lambda x: x[1]['leader_conv_rate'], reverse=True)
    for i, (player, data) in enumerate(sorted_conv, 1):
        if data['leader_conv_rate'] > 0:  # Only show players who have led
            print(f"{i}. {player}: {data['leader_conv_rate']}%")
    print()
    
    # Clutch King
    clutch_king = stats['clutch_king']
    print("--- CLUTCH KING ---")
    if clutch_king['player']:
        print(f"{clutch_king['player']}: {clutch_king['count']} wins with bid >= 200")
    else:
        print("No clutch wins recorded")
    print()
    
    # Most Wanted
    most_wanted = stats['most_wanted']
    print("--- THE MOST WANTED ---")
    if most_wanted['player']:
        print(f"{most_wanted['player']}: Called {most_wanted['count']} times")
    else:
        print("No teammate calls recorded")
    print()
    
    # Teammate Win Rate (Kingmakers)
    print("--- THE KINGMAKERS (Teammate Win Rate) ---")
    sorted_tm_win = sorted(player_stats.items(), key=lambda x: x[1]['teammate_win_rate'], reverse=True)
    for i, (player, data) in enumerate(sorted_tm_win, 1):
        if data['teammate_win_rate'] > 0:  # Only show players who have been teammates
            print(f"{i}. {player}: {data['teammate_win_rate']}%")
    print()
    
    # Unstoppable Trio
    unstoppable_trio = stats['unstoppable_trio']
    print("--- UNSTOPPABLE TRIO ---")
    if unstoppable_trio['players']:
        players_str = ", ".join(unstoppable_trio['players'])
        print(f"{players_str}: {unstoppable_trio['wins']} wins together")
    else:
        print("No trio wins recorded")
    print()
    
    # Podium Finishes (1st place)
    print("--- THE PODIUM (Most 1st Place Finishes) ---")
    sorted_podium = sorted(player_stats.items(), key=lambda x: x[1]['podium_1st'], reverse=True)
    for i, (player, data) in enumerate(sorted_podium, 1):
        print(f"{i}. {player}: {data['podium_1st']} first place finishes")
    print()
    
    print("=" * 60)


def generate_wrapped_data_js(stats):
    """
    Generate the wrapped_data.js file content in the correct format.
    Returns the JavaScript code as a string.
    """
    player_stats = stats['player_stats']
    
    # Build the slides array
    slides = []
    
    # 1. Intro Slide
    slides.append({
        'type': 'intro',
        'title': '2025',
        'subtitle': 'Kali Teeri Wrapped',
        'theme': 'theme-intro'
    })
    
    # 2. The Active Legends (Games Played)
    sorted_games = sorted(player_stats.items(), key=lambda x: x[1]['games_played'], reverse=True)
    slides.append({
        'type': 'ranked_list',
        'title': 'The Active Legends',
        'items': [{'label': player, 'value': f"{data['games_played']} games"} 
                 for player, data in sorted_games],
        'theme': 'theme-1'
    })
    
    # 3. The Champions (Round Win %)
    sorted_win_pct = sorted(player_stats.items(), key=lambda x: x[1]['round_win_pct'], reverse=True)
    slides.append({
        'type': 'ranked_list',
        'title': 'The Champions',
        'items': [{'label': player, 'value': f"{data['round_win_pct']}%"} 
                 for player, data in sorted_win_pct],
        'theme': 'theme-4'
    })
    
    # 4. The Closers (Leader Conversion Rate)
    sorted_conv = sorted(player_stats.items(), key=lambda x: x[1]['leader_conv_rate'], reverse=True)
    sorted_conv = [(p, d) for p, d in sorted_conv if d['leader_conv_rate'] > 0]  # Filter out zeros
    slides.append({
        'type': 'ranked_list',
        'title': 'The Closers',
        'items': [{'label': player, 'value': f"{data['leader_conv_rate']}%"} 
                 for player, data in sorted_conv],
        'theme': 'theme-2'
    })
    
    # 5. Clutch King
    clutch_king = stats['clutch_king']
    if clutch_king['player']:
        slides.append({
            'type': 'big_highlight',
            'title': 'Clutch King',
            'name': clutch_king['player'],
            'stat': f"{clutch_king['count']} Wins ≥ 200 pts",
            'description': 'The master of high-stakes victories.',
            'theme': 'theme-5'
        })
    
    # 6. The Most Wanted
    most_wanted = stats['most_wanted']
    if most_wanted['player']:
        slides.append({
            'type': 'big_highlight',
            'title': 'The Most Wanted',
            'name': most_wanted['player'],
            'stat': f"{most_wanted['count']} Times Called",
            'description': 'The most sought-after teammate of 2025.',
            'theme': 'theme-3'
        })
    
    # 7. The Kingmakers (Teammate Win Rate)
    sorted_tm_win = sorted(player_stats.items(), key=lambda x: x[1]['teammate_win_rate'], reverse=True)
    sorted_tm_win = [(p, d) for p, d in sorted_tm_win if d['teammate_win_rate'] > 0]  # Filter out zeros
    slides.append({
        'type': 'ranked_list',
        'title': 'The Kingmakers',
        'items': [{'label': player, 'value': f"{data['teammate_win_rate']}%"} 
                 for player, data in sorted_tm_win],
        'theme': 'theme-1'
    })
    
    # 8. Unstoppable Trio
    unstoppable_trio = stats['unstoppable_trio']
    if unstoppable_trio['players']:
        players_str = ", ".join(unstoppable_trio['players'])
        slides.append({
            'type': 'big_highlight',
            'title': 'Unstoppable Trio',
            'name': players_str,
            'stat': f"{unstoppable_trio['wins']} Wins Together",
            'description': 'The dream team that dominated the deck.',
            'theme': 'theme-4'
        })
    
    # 9. The Podium (Most 1st place finishes)
    sorted_podium = sorted(player_stats.items(), key=lambda x: x[1]['podium_1st'], reverse=True)
    slides.append({
        'type': 'ranked_list',
        'title': 'The Podium',
        'items': [{'label': player, 'value': f"{data['podium_1st']} first place finishes"} 
                 for player, data in sorted_podium],
        'theme': 'theme-2'
    })
    
    # Generate JavaScript code
    js_lines = ["// Kali Teeri Wrapped 2025 Data", "const wrappedData = ["]
    
    for i, slide in enumerate(slides):
        js_lines.append("  {")
        if slide['type'] == 'intro':
            js_lines.append(f"    type: \"{slide['type']}\",")
            js_lines.append(f"    title: \"{slide['title']}\",")
            js_lines.append(f"    subtitle: \"{slide['subtitle']}\",")
            js_lines.append(f"    theme: \"{slide['theme']}\",")
        elif slide['type'] == 'ranked_list':
            js_lines.append(f"    type: \"{slide['type']}\",")
            js_lines.append(f"    title: \"{slide['title']}\",")
            js_lines.append("    items: [")
            for item in slide['items']:
                js_lines.append(f"      {{ label: \"{item['label']}\", value: \"{item['value']}\" }},")
            js_lines.append("    ],")
            js_lines.append(f"    theme: \"{slide['theme']}\",")
        elif slide['type'] == 'big_highlight':
            js_lines.append(f"    type: \"{slide['type']}\",")
            js_lines.append(f"    title: \"{slide['title']}\",")
            js_lines.append(f"    name: \"{slide['name']}\",")
            js_lines.append(f"    stat: \"{slide['stat']}\",")
            js_lines.append(f"    description: \"{slide['description']}\",")
            js_lines.append(f"    theme: \"{slide['theme']}\",")
        
        js_lines.append("  },")
    
    js_lines.append("];")
    
    return "\n".join(js_lines)


# Main execution
if __name__ == "__main__":
    # Load data
    with open("data.json", "r") as f:
        game_data = json.load(f)
    
    # Calculate statistics
    stats = calculate_stats(game_data)
    
    # Print statistics to console
    print_stats(stats)
    
    # Generate wrapped_data.js content
    js_content = generate_wrapped_data_js(stats)
    
    # Write to file
    with open("wrapped_data.js", "w") as f:
        f.write(js_content)
    
    print("\n✓ wrapped_data.js has been generated successfully!")
