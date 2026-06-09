from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.columns import Columns

console = Console()

# --- ASCII Logos & Welcomes ---

def get_welcome_screen():
    """Returns the welcome ASCII art screen styled with rich colors."""
    ascii_art = """
[bold gold1]
  ___ ____  _      _     ___     _______   ____   ____ ___  ____  _____ 
 |_ _|  _ \| |    | |   |_ _|   | ____\ \ / /  _ \ / ___/ _ \|  _ \| ____|
  | || |_) | |    | |    | |    |  _|  \ V /| |_) | |  | | | | |_) |  _|  
  | ||  __/| |___ | |___ | |    | |___  | | |  __/| |__| |_| |  _ <| |___ 
 |___|_|   |_____||_____|___|   |_____| |_| |_|    \____\___/|_| \_\_____|
[/bold gold1]
    """
    
    subtitle = Text("🏏 Ultimate Indian Premier League CLI Dashboard 🏏", style="bold cyan justify=center")
    
    menu_text = """
[bold yellow]Select an Option:[/bold yellow]
[green]1.[/green] 🚀 Live Match (Dynamic Ball-by-Ball)
[green]2.[/green] 📊 IPL Points Table
[green]3.[/green] 🗓️ Upcoming Matches
[green]4.[/green] 🛡️ Team Stats & Rosters
[green]5.[/green] ❌ Exit
    """
    
    welcome_panel = Panel(
        Align.center(ascii_art + "\n" + subtitle.markup + "\n" + menu_text),
        border_style="gold1",
        title="[bold yellow]Welcome to IPL Live Score CLI[/bold yellow]",
        subtitle="[bold grey50]Powered by Rich & Antigravity[/bold grey50]",
        padding=(1, 5)
    )
    return welcome_panel

def get_team_logo(team_code):
    """Returns a colorized ASCII emblem for the team."""
    if team_code == "CSK":
        logo = """
  ______  ____  _  __
 / ___/ |/ / _|| |/ /
| (__/    /\ \ | ' < 
 \___/_/|_/___/|_|\_\\
"""
        return Panel(Text(logo, style="bold yellow"), title="[yellow]CSK[/yellow]", border_style="yellow", expand=False)
        
    elif team_code == "MI":
        logo = """
 __  __ ___ 
|  \/  |_ _|
| |\/| || | 
|_|  |_|___|
"""
        return Panel(Text(logo, style="bold royal_blue1"), title="[royal_blue1]MI[/royal_blue1]", border_style="royal_blue1", expand=False)
        
    elif team_code == "RCB":
        logo = """
 ____   ____ ____  
|  _ \ / ___| __ ) 
| |_) | |   |  _ \ 
|  _ <| |___| |_) |
|_| \_\\____|____/ 
"""
        return Panel(Text(logo, style="bold red"), title="[red]RCB[/red]", border_style="red", expand=False)
        
    elif team_code == "KKR":
        logo = """
 _  __ _  __ ____  
| |/ /| |/ /|  _ \ 
| ' < | ' < | |_) |
| . \ | . \ |  _ < 
|_|\_\|_|\_\|_| \_\\
"""
        return Panel(Text(logo, style="bold purple"), title="[purple]KKR[/purple]", border_style="purple", expand=False)
        
    elif team_code == "RR":
        logo = """
 ____  ____  
|  _ \|  _ \ 
| |_) | |_) |
|  _ <|  _ < 
|_| \_\\_| \_\\
"""
        return Panel(Text(logo, style="bold hot_pink"), title="[hot_pink]RR[/hot_pink]", border_style="hot_pink", expand=False)
        
    else:
        logo = f"\n  {team_code}  \n"
        return Panel(Text(logo, style="bold white"), title=team_code, border_style="white", expand=False)

# --- Overlay Alerts ---

def get_overlay_panel(event_type, team_name=""):
    """Creates a full-width high-attention banner for boundaries or wickets."""
    if event_type == "four":
        banner = """
🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥
🔥                                                 🔥
🔥             🔥 🔥 🔥  🔥  🔥  🔥  🔥            🔥
🔥             🔥        🔥  🔥  🔥  🔥            🔥
🔥             🔥 🔥     🔥  🔥  🔥  🔥            🔥
🔥             Brief     [bold gold1]🔥 FOUR! 🔥[/bold gold1]           🔥
🔥                                                 🔥
🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥
        """
        return Panel(Align.center(Text.from_markup(banner)), border_style="gold1", padding=(1, 2))
        
    elif event_type == "six":
        banner = """
🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀
🚀                                                 🚀
🚀             🚀 🚀 🚀  🚀  🚀  🚀  🚀            🚀
🚀             🚀        🚀  🚀  🚀  🚀            🚀
🚀             🚀 🚀     🚀  🚀  🚀  🚀            🚀
🚀             Super     [bold magenta1]🚀 SIX! 🚀[/bold magenta1]           🚀
🚀                                                 🚀
🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀
        """
        return Panel(Align.center(Text.from_markup(banner)), border_style="magenta1", padding=(1, 2))
        
    elif event_type == "wicket":
        banner = """
💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥
💥                                                 💥
💥           💥 WICKET! WICKET! WICKET! 💥         💥
💥                                                 💥
💥             💥 The crowd goes silent! 💥        💥
💥                                                 💥
💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥 💥
        """
        return Panel(Align.center(Text.from_markup(banner)), border_style="red1", padding=(1, 2))
        
    return None

# --- Main Live Match Board ---

def get_live_dashboard(sim):
    """
    Renders the beautiful scorecard UI panel for the active match.
    Uses nested rich components, tables, and momentum meters.
    """
    # 1. Header with Match Context
    title_style = "bold white on red" if sim.is_over else "bold white on green"
    header_text = Text(f"🏏 IPL LIVE SCORECARD - {sim.team1.upper()} vs {sim.team2.upper()} 🏏", style="bold yellow")
    venue_text = Text(f"Venue: {sim.venue} | Toss: {sim.toss_winner} elected to {sim.toss_decision}", style="italic grey50")
    
    # 2. Scoreboard Section
    bat_runs = sim.t1_runs if sim.innings == 1 else sim.t2_runs
    bat_wckts = sim.t1_wickets if sim.innings == 1 else sim.t2_wickets
    bat_overs = sim.t1_overs if sim.innings == 1 else sim.t2_overs
    bat_balls = sim.t1_balls if sim.innings == 1 else sim.t2_balls
    
    bowl_runs = sim.t2_runs if sim.innings == 1 else sim.t1_runs
    bowl_wckts = sim.t2_wickets if sim.innings == 1 else sim.t1_wickets
    bowl_overs = sim.t2_overs if sim.innings == 1 else sim.t1_overs
    
    score_markup = f"[bold green]{sim.batting_team}: {bat_runs}/{bat_wckts}[/bold green] ({bat_overs} Overs)"
    crr = round(bat_runs / (bat_balls / 6), 2) if bat_balls > 0 else 0.0
    
    score_text = Text.from_markup(f"{score_markup}\n[bold cyan]Current Run Rate (CRR):[/bold cyan] {crr:.2f}")
    
    # Target and chase info
    if sim.innings == 2:
        runs_needed = sim.target - bat_runs
        balls_left = 120 - bat_balls
        req_rr = round(runs_needed / (balls_left / 6), 2) if balls_left > 0 else 99.99
        score_text.append(f"\n[bold yellow]Target:[/bold yellow] {sim.target} | Needs [bold red]{runs_needed}[/bold red] off [bold red]{balls_left}[/bold red] balls")
        score_text.append(f"\n[bold pink]Required Run Rate (RRR):[/bold pink] {req_rr:.2f}")
    else:
        score_text.append(f"\n[bold yellow]1st Innings[/bold yellow] | Projected Score: {int(crr*20) if crr > 0 else 0}")
        
    score_panel = Panel(
        Align.center(score_text),
        title=f"[bold]Active Batting: {sim.batting_team}[/bold]",
        border_style="green" if not sim.is_over else "grey50",
        expand=True
    )
    
    # 3. Logo columns
    logo1 = get_team_logo(sim.t1_code)
    logo2 = get_team_logo(sim.t2_code)
    logos_column = Columns([logo1, logo2], align="center")
    
    # 4. Batsmen Table
    bat_table = Table(title="🏏 Batting Card", title_style="bold yellow", expand=True)
    bat_table.add_column("Batter", style="bold white", width=25)
    bat_table.add_column("Status", style="grey70")
    bat_table.add_column("Runs", justify="right", style="green")
    bat_table.add_column("Balls", justify="right", style="cyan")
    bat_table.add_column("4s", justify="right")
    bat_table.add_column("6s", justify="right")
    bat_table.add_column("S/R", justify="right", style="magenta")
    
    for idx, b in enumerate(sim.batsmen_stats):
        # Indicate current strikers
        name = b["name"]
        if idx == sim.striker_idx and b["status"] == "batting":
            name = f"🏏 [bold green]{name} *[/bold green]"
        elif idx == sim.non_striker_idx and b["status"] == "batting":
            name = f"[bold white]{name}[/bold white]"
            
        status = b["status"]
        if status == "batting":
            status_str = "[bold green]Batting[/bold green]"
        elif status == "out":
            status_str = f"[red]{b['how_out']}[/red]"
        else:
            status_str = "[grey50]Yet to Bat[/grey50]"
            
        # Display only batting or out players to keep screen compact
        if b["status"] in ["batting", "out"]:
            sr = round((b["runs"] / b["balls"]) * 100, 1) if b["balls"] > 0 else 0.0
            bat_table.add_row(
                name,
                status_str,
                str(b["runs"]),
                str(b["balls"]),
                str(b["fours"]),
                str(b["sixes"]),
                f"{sr:.1f}"
            )
            
    # 5. Bowlers Table
    bowl_table = Table(title="🥎 Bowling Card", title_style="bold yellow", expand=True)
    bowl_table.add_column("Bowler", style="bold white", width=25)
    bowl_table.add_column("Overs", justify="right", style="cyan")
    bowl_table.add_column("Maidens", justify="right")
    bowl_table.add_column("Runs", justify="right", style="red")
    bowl_table.add_column("Wkts", justify="right", style="bold green")
    bowl_table.add_column("Econ", justify="right", style="magenta")
    
    for idx, bw in enumerate(sim.bowler_stats):
        name = bw["name"]
        if idx == sim.current_bowler_idx:
            name = f"🥎 [bold cyan]{name} *[/bold cyan]"
            
        runs_c = bw["runs_conceded"]
        balls_b = bw["balls_bowled"]
        overs_str = bw["overs"]
        
        econ = round(runs_c / (balls_b / 6), 2) if balls_b > 0 else 0.00
        
        # Display bowlers who have bowled or are currently bowling
        if balls_b > 0 or idx == sim.current_bowler_idx:
            bowl_table.add_row(
                name,
                overs_str,
                str(bw["maidens"]),
                str(runs_c),
                str(bw["wickets"]),
                f"{econ:.2f}"
            )
            
    # 6. Win Probability & Momentum Gauges
    # Build dynamic visual win probability bar
    prob_t1 = sim.win_prob if sim.batting_team_code == sim.t1_code else (100.0 - sim.win_prob)
    prob_t2 = 100.0 - prob_t1
    
    bar_width = 30
    filled_t1 = int(round(prob_t1 / 100.0 * bar_width))
    filled_t2 = bar_width - filled_t1
    
    prob_bar = f"[bold yellow]{sim.t1_code}[/bold yellow] {'█' * filled_t1}[grey30]█[/grey30]{'█' * filled_t2} [bold royal_blue1]{sim.t2_code}[/bold royal_blue1]"
    prob_stat = f"{sim.t1_code}: {prob_t1:.1f}% | {sim.t2_code}: {prob_t2:.1f}%"
    
    # Momentum Emojis
    momentum_emojis = {
        -5: "❄️❄️❄️ [bold royal_blue1]Deep Freeze[/bold royal_blue1] (Bowling team dominates)",
        -4: "❄️❄️ [bold royal_blue1]Cold Pressure[/bold royal_blue1]",
        -3: "❄️ [bold royal_blue1]Tight overs[/bold royal_blue1]",
        -2: "⚖️ [bold grey70]Defensive Bowling[/bold grey70]",
        -1: "⚖️ [bold grey70]Steady bowling[/bold grey70]",
         0: "⚖️ [bold yellow]Equally Balanced[/bold yellow]",
         1: "🔥 [bold green]Steady Chasing[/bold green]",
         2: "🔥 [bold green]Intent building[/bold green]",
         3: "🔥🔥 [bold green]Batting Charge[/bold green]",
         4: "🔥🔥🔥 [bold orange1]On Fire![/bold orange1] (Boundaries flowing)",
         5: "🚀🚀🚀 [bold red]Carnage![/bold red] (Total dominance)"
    }
    mom_val = max(-5, min(5, sim.momentum))
    momentum_str = momentum_emojis[mom_val]
    
    analysis_text = Text.from_markup(
        f"📊 [bold]Win Probability:[/bold]\n   {prob_bar} ({prob_stat})\n\n"
        f"📈 [bold]Match Momentum:[/bold] {momentum_str}\n\n"
        f"🌟 [bold]POTM Predictor:[/bold] [bold gold1]{sim.potm_predict}[/bold gold1]"
    )
    analysis_panel = Panel(analysis_text, title="⚙️ Analytics & Predictors", border_style="cyan")
    
    # 7. Commentary Section (show last 4 events)
    comm_box = Text()
    for comm in sim.commentary[-4:]:
        # Highlight boundaries and wickets inside commentary
        if "FOUR!" in comm:
            comm_box.append(comm + "\n", style="bold yellow")
        elif "SIX!" in comm:
            comm_box.append(comm + "\n", style="bold orange1")
        elif "WICKET!" in comm:
            comm_box.append(comm + "\n", style="bold red1")
        elif "finished" in comm.lower() or "won" in comm.lower():
            comm_box.append(comm + "\n", style="bold green")
        else:
            comm_box.append(comm + "\n", style="grey70")
            
    comm_panel = Panel(comm_box, title="💬 Mini Commentary", border_style="yellow")
    
    # 8. Assemble Full Dashboard
    # Organize layout elements
    main_column = Table.grid(expand=True)
    main_column.add_column(ratio=1)
    
    main_column.add_row(Align.center(header_text))
    main_column.add_row(Align.center(venue_text))
    main_column.add_row(Text("")) # Spacer
    
    # Layout grid for middle section: Scoreboard + Logo/Emblems
    middle_grid = Table.grid(expand=True)
    middle_grid.add_column(ratio=2)
    middle_grid.add_column(ratio=1)
    middle_grid.add_row(score_panel, Align.center(logos_column))
    
    main_column.add_row(middle_grid)
    main_column.add_row(Text("")) # Spacer
    
    # Statistics cards
    main_column.add_row(bat_table)
    main_column.add_row(Text("")) # Spacer
    main_column.add_row(bowl_table)
    main_column.add_row(Text("")) # Spacer
    
    # Analysis & Commentary
    lower_grid = Table.grid(expand=True)
    lower_grid.add_column(ratio=1, pad_edge=True)
    lower_grid.add_column(ratio=1, pad_edge=True)
    lower_grid.add_row(analysis_panel, comm_panel)
    
    main_column.add_row(lower_grid)
    
    # If match is finished, display results clearly
    if sim.is_over:
        result_panel = Panel(
            Align.center(f"[bold gold1]🏁 {sim.result_statement} 🏁[/bold gold1]\n[grey70]Press Ctrl+C to return to main menu.[/grey70]"),
            border_style="gold1",
            expand=True
        )
        main_column.add_row(Text(""))
        main_column.add_row(result_panel)
        
    dashboard_wrapper = Panel(main_column, border_style="gold1", padding=(1, 2))
    return dashboard_wrapper
