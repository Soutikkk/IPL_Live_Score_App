import os
import json
import threading
import time

# Windows specific beep sounds fallback
IS_WINDOWS = os.name == 'nt'
if IS_WINDOWS:
    import winsound

def play_sound_async(sound_type):
    """
    Plays a sound in a background thread to prevent UI freezing.
    First checks if a custom MP3 exists in a 'sounds' directory.
    If not, or if playsound fails, falls back to Windows system beeps.
    """
    def worker():
        try:
            # Custom sounds directory check
            sound_file = f"sounds/{sound_type}.mp3"
            if os.path.exists(sound_file):
                try:
                    from playsound import playsound
                    playsound(sound_file)
                    return
                except Exception:
                    pass # Fall back to winsound or system alert
            
            # Windows beep fallback
            if IS_WINDOWS:
                if sound_type == "four":
                    # Two rapid high-pitched beeps for a boundary
                    winsound.Beep(1000, 150)
                    time.sleep(0.05)
                    winsound.Beep(1000, 150)
                elif sound_type == "six":
                    # Rising pitch beep for a six
                    winsound.Beep(800, 150)
                    winsound.Beep(1200, 250)
                elif sound_type == "wicket":
                    # Deep descending sound for wicket
                    winsound.Beep(400, 400)
                elif sound_type == "welcome":
                    # Friendly opening chime
                    winsound.Beep(600, 100)
                    winsound.Beep(800, 100)
                    winsound.Beep(1000, 200)
            else:
                # Unix system beep (terminal bell) as a fallback
                print("\a", end="", flush=True)
        except Exception:
            pass # Silent failure so user doesn't experience crashes
            
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

# --- Match History Storage ---

HISTORY_FILE = "match_history.json"

def save_match_to_history(match_data):
    """
    Appends a finished match log to the local JSON file.
    """
    history = load_match_history()
    history.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "match_name": f"{match_data['team1']} vs {match_data['team2']}",
        "winner": match_data.get("winner", "Unknown"),
        "result_statement": match_data.get("result_statement", ""),
        "scorecard": {
            "team1": {
                "name": match_data["team1"],
                "score": f"{match_data['t1_runs']}/{match_data['t1_wickets']}",
                "overs": f"{match_data['t1_overs']}"
            },
            "team2": {
                "name": match_data["team2"],
                "score": f"{match_data['t2_runs']}/{match_data['t2_wickets']}",
                "overs": f"{match_data['t2_overs']}"
            }
        }
    })
    
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)
        return True
    except Exception:
        return False

def load_match_history():
    """
    Loads historical match scores from the local JSON file.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

# --- Calculations ---

def calculate_run_rate(runs, balls):
    """
    Returns the run rate formatted to 2 decimal places.
    """
    if balls == 0:
        return 0.00
    overs = balls / 6
    return round(runs / overs, 2)

def calculate_required_run_rate(target, current_runs, balls_left):
    """
    Returns the required run rate formatted to 2 decimal places.
    """
    if balls_left <= 0:
        return 99.99 if current_runs < target else 0.00
    runs_needed = target - current_runs
    if runs_needed <= 0:
        return 0.00
    overs_left = balls_left / 6
    return round(runs_needed / overs_left, 2)
