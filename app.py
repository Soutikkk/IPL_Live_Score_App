import sys
import time
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

from api import IPL_TEAMS, POINTS_TABLE, UPCOMING_MATCHES, IPLMatchSimulator
from ui import get_welcome_screen, get_live_dashboard, get_overlay_panel
from utils import play_sound_async, load_match_history

console = Console()

def clear_console():
    """Clears the terminal screen for clean UI transitions."""
    console.clear()

def view_points_table():
    """Displays the IPL points table, highlighting playoff contenders."""
    clear_console()
    table = Table(
        title="🏆 IPL POINTS TABLE 🏆",
        title_style="bold gold1",
        caption="Top 4 Teams Qualify for the Play-offs",
        expand=True
    )
    table.add_column("Pos", justify="center", style="cyan", width=4)
    table.add_column("Team", style="bold white")
    table.add_column("Played", justify="center")
    table.add_column("Won", justify="center", style="green")
    table.add_column("Lost", justify="center", style="red")
    table.add_column("Points", justify="center", style="bold yellow")
    table.add_column("NRR", justify="center", style="magenta")

    for idx, row in enumerate(POINTS_TABLE, 1):
        # Highlight top 4 teams (Playoffs)
        row_style = "bold green" if idx <= 4 else "grey70"
        table.add_row(
            str(idx),
            row["team"],
            str(row["p"]),
            str(row["w"]),
            str(row["l"]),
            str(row["pts"]),
            row["nrr"],
            style=row_style
        )
        
    console.print(table)
    console.print("\n[bold yellow]Press Enter to return to Main Menu...[/bold yellow]")
    input()

def view_upcoming_matches():
    """Displays upcoming IPL fixtures."""
    clear_console()
    table = Table(title="🗓️ UPCOMING MATCHES 🗓️", title_style="bold gold1", expand=True)
    table.add_column("Match", justify="center", style="cyan")
    table.add_column("Teams", style="bold white")
    table.add_column("Venue", style="italic yellow")
    table.add_column("Time (IST)", style="bold green")

    for match in UPCOMING_MATCHES:
        table.add_row(
            match["match"],
            match["teams"],
            match["venue"],
            match["time"]
        )

    console.print(table)
    console.print("\n[bold yellow]Press Enter to return to Main Menu...[/bold yellow]")
    input()

def view_team_stats():
    """Interactive menu to view statistics and roster of specific IPL teams."""
    while True:
        clear_console()
        console.print("[bold gold1]🛡️ IPL TEAM STATS & ROSTERS 🛡️[/bold gold1]\n")
        
        # Display team selection options
        teams_list = list(IPL_TEAMS.keys())
        for idx, code in enumerate(teams_list, 1):
            console.print(f"[green]{idx}.[/green] {IPL_TEAMS[code]['name']} ({code})")
        console.print(f"[green]{len(teams_list) + 1}.[/green] Back to Main Menu")
        
        choice = input("\nSelect a team (number): ").strip()
        if not choice.isdigit():
            console.print("[red]Invalid input! Please enter a number.[/red]")
            time.sleep(1)
            continue
            
        choice_idx = int(choice) - 1
        if choice_idx == len(teams_list):
            break
        elif 0 <= choice_idx < len(teams_list):
            team_code = teams_list[choice_idx]
            team_info = IPL_TEAMS[team_code]
            
            clear_console()
            
            # Format roster as a table
            roster_table = Table(title="👥 Current Squad Roster", title_style="bold cyan", show_header=False, expand=True)
            roster_table.add_column("Player", style="white")
            
            # Split roster into columns for cleaner presentation
            roster = team_info["roster"]
            for i in range(0, len(roster), 2):
                p1 = roster[i]
                p2 = roster[i+1] if i+1 < len(roster) else ""
                roster_table.add_row(f"• {p1:<25} • {p2}")

            team_details_markup = (
                f"[bold yellow]Team Name:[/bold yellow] {team_info['name']}\n"
                f"[bold yellow]Captain:[/bold yellow] {team_info['captain']}\n"
                f"[bold yellow]Home Ground:[/bold yellow] {team_info['home']}\n"
                f"[bold yellow]IPL Titles:[/bold yellow] {team_info['titles']}\n"
            )
            
            detail_panel = Panel(
                team_details_markup,
                title=f"[bold gold1]{team_info['name']} Info[/bold gold1]",
                border_style="yellow"
            )
            
            console.print(detail_panel)
            console.print(roster_table)
            console.print("\n[bold yellow]Press Enter to go back to Team List...[/bold yellow]")
            input()
        else:
            console.print("[red]Invalid option! Select from list.[/red]")
            time.sleep(1)

def run_live_match():
    """Configures and runs the ball-by-ball simulated match live update screen."""
    clear_console()
    console.print("[bold gold1]⚡ SELECT A LIVE MATCH TO SIMULATE ⚡[/bold gold1]\n")
    
    match_options = [
        ("CSK", "MI"),
        ("RCB", "KKR"),
        ("RR", "CSK"),
        ("MI", "RCB"),
        ("KKR", "RR")
    ]
    
    for idx, (t1, t2) in enumerate(match_options, 1):
        console.print(f"[green]{idx}.[/green] {IPL_TEAMS[t1]['name']} vs {IPL_TEAMS[t2]['name']}")
    console.print(f"[green]{len(match_options) + 1}.[/green] Cancel & Back")
    
    choice = input("\nSelect match to simulate (number): ").strip()
    if not choice.isdigit():
        console.print("[red]Invalid choice![/red]")
        time.sleep(1)
        return
        
    choice_idx = int(choice) - 1
    if choice_idx == len(match_options):
        return
    elif 0 <= choice_idx < len(match_options):
        t1_code, t2_code = match_options[choice_idx]
        
        # Sound confirmation
        sound_choice = input("Enable sound alerts? (y/n): ").strip().lower()
        enable_sound = sound_choice in ["y", "yes", ""]
        
        # Initialize Simulator
        sim = IPLMatchSimulator(t1_code, t2_code)
        
        if enable_sound:
            play_sound_async("welcome")
            
        clear_console()
        console.print("[bold yellow]Match is loading and toss is underway...[/bold yellow]")
        time.sleep(2)
        
        try:
            # Using rich Live to refresh scorecard output in-place
            with Live(get_live_dashboard(sim), refresh_per_second=2) as live:
                while not sim.is_over:
                    # Execute a ball delivery
                    sim.update_ball()
                    
                    # Highlight boundaries & wickets with animated flash screens
                    if sim.last_event in ["four", "six", "wicket"]:
                        overlay = get_overlay_panel(sim.last_event, sim.batting_team)
                        if overlay:
                            live.update(overlay)
                            time.sleep(1.5)  # Let the overlay display
                            
                    # Update live scorecard view
                    live.update(get_live_dashboard(sim))
                    
                    # Wait 10 seconds before next ball (sleep in 0.1s increments for snappy Ctrl+C escape)
                    for _ in range(100):
                        if sim.is_over:
                            break
                        time.sleep(0.1)
                        
                # Match finished - display final dashboard
                live.update(get_live_dashboard(sim))
                
                # Keep final dashboard on screen until user manually escapes
                while True:
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            # Clean exit back to menu on Ctrl+C
            clear_console()
            console.print("[bold yellow]Exited live match scorecard. Returning to main menu...[/bold yellow]")
            time.sleep(1.5)
    else:
        console.print("[red]Invalid selection![/red]")
        time.sleep(1)

def display_history():
    """Lists completed matches stored in the JSON history log."""
    clear_console()
    console.print("[bold gold1]📚 COMPLETED MATCHES ARCHIVE 📚[/bold gold1]\n")
    history = load_match_history()
    
    if not history:
        console.print("[grey50]No completed matches found in history yet.[/grey50]")
    else:
        table = Table(expand=True)
        table.add_column("Date/Time", style="cyan")
        table.add_column("Matchup", style="bold white")
        table.add_column("Scores", style="yellow")
        table.add_column("Result Details", style="green")
        
        for record in history:
            t1 = record["scorecard"]["team1"]
            t2 = record["scorecard"]["team2"]
            scores = f"{t1['name']}: {t1['score']} ({t1['overs']} O) vs {t2['name']}: {t2['score']} ({t2['overs']} O)"
            table.add_row(
                record["timestamp"],
                record["match_name"],
                scores,
                record["result_statement"]
            )
        console.print(table)
        
    console.print("\n[bold yellow]Press Enter to return to Main Menu...[/bold yellow]")
    input()

# --- Entry Point ---

def main():
    while True:
        try:
            clear_console()
            # Show Welcome Screen
            console.print(get_welcome_screen())
            
            choice = input("\nEnter your choice (1-5, or 'h' for history): ").strip().lower()
            if choice == "1":
                run_live_match()
            elif choice == "2":
                view_points_table()
            elif choice == "3":
                view_upcoming_matches()
            elif choice == "4":
                view_team_stats()
            elif choice == "5" or choice == "exit":
                clear_console()
                console.print(Panel(
                    Align.center("[bold gold1]🏏 Thank you for playing! See you next match day! 🏏[/bold gold1]"),
                    border_style="gold1"
                ))
                sys.exit(0)
            elif choice == "h":
                display_history()
            else:
                console.print("[red]Invalid input! Please enter a option from 1 to 5.[/red]")
                time.sleep(1)
        except KeyboardInterrupt:
            # Handle Ctrl+C on main menu gracefully
            clear_console()
            console.print("[bold yellow]Exiting application...[/bold yellow]")
            sys.exit(0)

if __name__ == "__main__":
    main()
