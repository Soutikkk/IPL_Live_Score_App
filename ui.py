"""Rich-based IPL CLI dashboard components.

This module renders UI only; a separate match simulation object (``sim``)
with the attributes used below must be provided by the main application.
"""

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
    ascii_art = r"""
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
        logo = r"""
  ______  ____  _  __
 / ___/ |/ / _|| |/ /
| (__/    /\ \ | ' < 
 \___/_/|_/___/|_|\_\\
"""
        return Panel(Text(logo, style="bold yellow"), title="[yellow]CSK[/yellow]", border_style="yellow", expand=False)
        
    elif team_code == "MI":
        logo = r"""
 __  __ ___ 
|  \/  |_ _|
| |\/| || | 
|_|  |_|___|
"""
        return Panel(Text(logo, style="bold royal_blue1"), title="[royal_blue1]MI[/royal_blue1]", border_style="royal_blue1", expand=False)
        
    elif team_code == "RCB":
        logo = r"""
 ____   ____ ____  
|  _ \ / ___| __ ) 
| |_) | |   |  _ \ 
|  _ <| |___| |_) |
|_| \_\\____|____/ 
"""
        return Panel(Text(logo, style="bold red"), title="[red]RCB[/red]", border_style="red", expand=False)
        
    elif team_code == "KKR":
        logo = r"""
 _  __ _  __ ____  
| |/ /| |/ /|  _ \ 
| ' < | ' < | |_) |
| . \ | . \ |  _ < 
|_|\_\|_|\_\|_| \_\\
"""
        return Panel(Text(logo, style="bold purple"), title="[purple]KKR[/purple]", border_style="purple", expand=False)
        
    elif team_code == "RR":
        logo = r"""
 ____  ____  
|  _ \|  _ \ 
| |_) | |_) |
|  _ <|  _ < 
|_| \_\\_| \_\\
