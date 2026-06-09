# 🏏 IPL Live Score CLI App

A colorful, interactive, and premium command-line dashboard for cricket lovers, inspired by Cricbuzz. Built using Python 3 and the `rich` terminal library, it simulates live IPL matches ball-by-ball with dynamic scoreboards, real-time commentary, win probabilities, match momentum shifts, and play-of-the-match predictors.

---

## ✨ Key Features

1. **🚀 Dynamic Live Match Simulator**:
   - Updates automatically every **10 seconds** with new ball-by-ball actions.
   - Leverages realistic T20-weighted cricketing probability (dots, singles, doubles, boundaries, wickets, and extras).
   - Simulates batter stats (runs, balls faced, boundaries, strike rate) and bowler details (overs, maidens, wickets, economy).
2. **💥 Flashing Special Event Overlays**:
   - Interactive high-attention splash screens when boundaries occur (`🔥 FOUR!`, `🚀 SIX!`) or when a wicket falls (`💥 WICKET!`).
3. **📊 Real-time Game Analytics**:
   - **Win Probability Gauge**: Updates live as required run rates or wickets shift.
   - **Emoji-based Match Momentum**: Visual representation of match pressure (from "Deep Freeze" for tight bowling to "Carnage!" for high-speed batting).
   - **Player-of-the-Match Predictor**: Highlights the top-performing player dynamically based on current game statistics.
4. **🔊 Immersive Sound Effects**:
   - Plays sound alerts for boundaries, wickets, and welcome bells in a non-blocking background thread.
   - Automatic system chime/beep fallback if sound assets are missing.
5. **🗃️ Match History Archives**:
   - Completed match results are automatically persisted in a local `match_history.json` database.
   - Review all historical scores through the CLI points archive menu.
6. **📋 Extras & Standings**:
   - **IPL Points Table**: Standings table with top-4 playoff contenders highlighted in green.
   - **Upcoming Matches**: Visual display of upcoming match fixtures and details.
   - **Team Stats & Rosters**: View squad configurations, captaincy, and home grounds for franchises.

---

## 📂 Project Structure

- **`app.py`**: The application hub containing menu selectors, routing handlers, and the `rich.Live` interface engine.
- **`api.py`**: The simulation processor housing points tables, rosters, and the `IPLMatchSimulator` state logic.
- **`ui.py`**: The visual presentation engine for ASCII team emblems, scoreboard tables, commentary lists, and alert boxes.
- **`utils.py`**: Mathematical operations, background audio dispatchers, and JSON-based file access utilities.
- **`requirements.txt`**: Declares package versions.

---

## 🚀 Installation & Setup

### Prerequisites
Make sure you have **Python 3.7+** installed on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/Soutikkk/IPL_Live_Score_App.git
cd IPL_Live_Score_App
```

### 2. Install Dependencies
Run the following command to install required modules (`rich` and `playsound`):
```bash
pip install -r requirements.txt
```

---

## 🎮 How to Play

Start the application by running:
```bash
python app.py
```

### Main Menu Navigation
Select an option by entering a number:
1. **Live Match**: Pick a game to simulate and toggle sound alerts.
2. **IPL Points Table**: Display the latest standing list.
3. **Upcoming Matches**: View the fixture schedule.
4. **Team Stats & Rosters**: Browse captain info, titles, and squad lists.
5. **Exit**: Terminate application gracefully.

*Shortcut*: Enter `h` on the main menu to open the **Completed Matches Archive**.

---

## 🔊 Sound Effects Integration (Optional)

By default, the application uses **Windows Beep API** (`winsound`) or system bell bells as fallback. If you want custom HQ audio alerts:
1. Create a folder named `sounds/` in the project root.
2. Add your audio files named:
   - `sounds/welcome.mp3`
   - `sounds/four.mp3`
   - `sounds/six.mp3`
   - `sounds/wicket.mp3`
3. Launch the game, select a match, enable sound alerts, and enjoy the realistic commentary sound!

---

## 📝 License
This project is open-source. Feel free to copy, modify, and improve it for your own personal tracks.
