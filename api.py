import random
import time
from utils import save_match_to_history, play_sound_async, calculate_run_rate, calculate_required_run_rate

# --- Static Data Databases ---

IPL_TEAMS = {
    "CSK": {
        "name": "Chennai Super Kings",
        "captain": "Ruturaj Gaikwad",
        "home": "M. A. Chidambaram Stadium, Chennai",
        "titles": "5 (2010, 2011, 2018, 2021, 2023)",
        "roster": [
            "Ruturaj Gaikwad", "Rachin Ravindra", "Shivam Dube", 
            "Daryl Mitchell", "Ravindra Jadeja", "MS Dhoni", 
            "Sameer Rizvi", "Shardul Thakur", "Deepak Chahar", 
            "Tushar Deshpande", "Matheesha Pathirana"
        ]
    },
    "MI": {
        "name": "Mumbai Indians",
        "captain": "Hardik Pandya",
        "home": "Wankhede Stadium, Mumbai",
        "titles": "5 (2013, 2015, 2017, 2019, 2020)",
        "roster": [
            "Rohit Sharma", "Ishan Kishan", "Suryakumar Yadav", 
            "Tilak Varma", "Hardik Pandya", "Tim David", 
            "Mohammad Nabi", "Gerald Coetzee", "Piyush Chawla", 
            "Jasprit Bumrah", "Akash Madhwal"
        ]
    },
    "RCB": {
        "name": "Royal Challengers Bengaluru",
        "captain": "Faf du Plessis",
        "home": "M. Chinnaswamy Stadium, Bengaluru",
        "titles": "None (Runners up: 2009, 2011, 2016)",
        "roster": [
            "Virat Kohli", "Faf du Plessis", "Rajat Patidar", 
            "Glenn Maxwell", "Cameron Green", "Dinesh Karthik", 
            "Mahipal Lomror", "Karn Sharma", "Mohammed Siraj", 
            "Yash Dayal", "Lockie Ferguson"
        ]
    },
    "KKR": {
        "name": "Kolkata Knight Riders",
        "captain": "Shreyas Iyer",
        "home": "Eden Gardens, Kolkata",
        "titles": "3 (2012, 2014, 2024)",
        "roster": [
            "Sunil Narine", "Phil Salt", "Angkrish Raghuvanshi", 
            "Shreyas Iyer", "Venkatesh Iyer", "Rinku Singh", 
            "Andre Russell", "Ramandeep Singh", "Mitchell Starc", 
            "Harshit Rana", "Varun Chakaravarthy"
        ]
    },
    "RR": {
        "name": "Rajasthan Royals",
        "captain": "Sanju Samson",
        "home": "Sawai Mansingh Stadium, Jaipur",
        "titles": "1 (2008)",
        "roster": [
            "Yashasvi Jaiswal", "Jos Buttler", "Sanju Samson", 
            "Riyan Parag", "Dhruv Jurel", "Shimron Hetmyer", 
            "Ravichandran Ashwin", "Trent Boult", "Avesh Khan", 
            "Sandeep Sharma", "Yuzvendra Chahal"
        ]
    }
}

POINTS_TABLE = [
    {"team": "Kolkata Knight Riders", "code": "KKR", "p": 14, "w": 9, "l": 4, "pts": 20, "nrr": "+1.428"},
    {"team": "Sunrisers Hyderabad", "code": "SRH", "p": 14, "w": 8, "l": 5, "pts": 17, "nrr": "+0.414"},
    {"team": "Rajasthan Royals", "code": "RR", "p": 14, "w": 8, "l": 5, "pts": 17, "nrr": "+0.273"},
    {"team": "Royal Challengers Bengaluru", "code": "RCB", "p": 14, "w": 7, "l": 7, "pts": 14, "nrr": "+0.593"},
    {"team": "Chennai Super Kings", "code": "CSK", "p": 14, "w": 7, "l": 7, "pts": 14, "nrr": "+0.428"},
    {"team": "Delhi Capitals", "code": "DC", "p": 14, "w": 7, "l": 7, "pts": 14, "nrr": "-0.377"},
    {"team": "Lucknow Super Giants", "code": "LSG", "p": 14, "w": 7, "l": 7, "pts": 14, "nrr": "-0.667"},
    {"team": "Gujarat Titans", "code": "GT", "p": 14, "w": 5, "l": 7, "pts": 12, "nrr": "-0.062"},
    {"team": "Punjab Kings", "code": "PBKS", "p": 14, "w": 5, "l": 9, "pts": 10, "nrr": "-0.353"},
    {"team": "Mumbai Indians", "code": "MI", "p": 14, "w": 4, "l": 10, "pts": 8, "nrr": "-0.318"}
]

UPCOMING_MATCHES = [
    {"match": "Match 1", "teams": "RCB vs CSK", "venue": "M. Chinnaswamy Stadium, Bengaluru", "time": "Tonight, 7:30 PM"},
    {"match": "Match 2", "teams": "MI vs KKR", "venue": "Wankhede Stadium, Mumbai", "time": "Tomorrow, 7:30 PM"},
    {"match": "Match 3", "teams": "RR vs SRH", "venue": "Sawai Mansingh Stadium, Jaipur", "time": "June 11, 7:30 PM"},
    {"match": "Match 4", "teams": "DC vs GT", "venue": "Arun Jaitley Stadium, Delhi", "time": "June 12, 7:30 PM"},
    {"match": "Match 5", "teams": "PBKS vs LSG", "venue": "PCA IS Bindra Stadium, Mohali", "time": "June 13, 7:30 PM"}
]

# --- Live Match Simulation Engine ---

class IPLMatchSimulator:
    def __init__(self, team1_code, team2_code):
        self.t1_code = team1_code
        self.t2_code = team2_code
        self.team1 = IPL_TEAMS[team1_code]["name"]
        self.team2 = IPL_TEAMS[team2_code]["name"]
        self.venue = IPL_TEAMS[team1_code]["home"]
        
        # Rosters
        self.t1_roster = IPL_TEAMS[team1_code]["roster"]
        self.t2_roster = IPL_TEAMS[team2_code]["roster"]
        
        # Toss
        self.toss_winner = random.choice([self.team1, self.team2])
        self.toss_decision = random.choice(["bat", "bowl"])
        
        # Determine who bats first
        if (self.toss_winner == self.team1 and self.toss_decision == "bat") or \
           (self.toss_winner == self.team2 and self.toss_decision == "bowl"):
            self.batting_team_code = self.t1_code
            self.bowling_team_code = self.t2_code
        else:
            self.batting_team_code = self.t2_code
            self.bowling_team_code = self.t1_code
            
        self.batting_team = IPL_TEAMS[self.batting_team_code]["name"]
        self.bowling_team = IPL_TEAMS[self.bowling_team_code]["name"]
        
        # Match Game State
        self.innings = 1
        self.is_over = False
        self.result_statement = ""
        self.winner = ""
        self.last_event = None  # Store if 'four', 'six', 'wicket' occurred
        
        # Score variables
        self.t1_runs = 0
        self.t1_wickets = 0
        self.t1_balls = 0
        self.t1_overs = "0.0"
        
        self.t2_runs = 0
        self.t2_wickets = 0
        self.t2_balls = 0
        self.t2_overs = "0.0"
        
        self.target = None
        
        # Player statistics managers
        self.initialize_innings_players()
        
        # Commentary list
        self.commentary = [f"Welcome to {self.venue}! The toss has been won by {self.toss_winner}, who decided to {self.toss_decision} first."]
        
        # Match Momentum: -5 (Bowling team dominant) to +5 (Batting team dominant)
        self.momentum = 0
        self.win_prob = 50.0  # Percentage for batting team
        self.potm_predict = "None yet"

    def initialize_innings_players(self):
        """Initializes the batsman scoreboard and selecting bowlers for the active innings"""
        curr_bat_roster = self.t1_roster if self.batting_team_code == self.t1_code else self.t2_roster
        curr_bowl_roster = self.t2_roster if self.batting_team_code == self.t1_code else self.t1_roster
        
        # Batter list containing runs, balls, fours, sixes, batting status
        self.batsmen_stats = []
        for name in curr_bat_roster:
            self.batsmen_stats.append({
                "name": name,
                "status": "yet_to_bat",  # "batting", "out", "yet_to_bat"
                "runs": 0,
                "balls": 0,
                "fours": 0,
                "sixes": 0,
                "how_out": ""
            })
            
        # Select current batters
        self.striker_idx = 0
        self.non_striker_idx = 1
        self.batsmen_stats[0]["status"] = "batting"
        self.batsmen_stats[1]["status"] = "batting"
        
        # Bowler list (select 5 bowlers from the bottom of the roster)
        self.bowler_stats = []
        # Usually, the last 5 players are bowlers/all-rounders
        for name in curr_bowl_roster[6:]:
            self.bowler_stats.append({
                "name": name,
                "balls_bowled": 0,
                "overs": "0.0",
                "maidens": 0,
                "runs_conceded": 0,
                "wickets": 0
            })
            
        self.current_bowler_idx = 0

    def get_overs_string(self, balls):
        """Converts total balls to over formatting (e.g. 15 balls -> 2.3 overs)"""
        overs = balls // 6
        rem = balls % 6
        return f"{overs}.{rem}"

    def update_ball(self):
        """
        Runs a single ball delivery simulation.
        Updates runs, wickets, player stats, commentary, momentum, and win probability.
        """
        if self.is_over:
            return
            
        self.last_event = None
        
        # 1. Identify active batters and bowler
        striker = self.batsmen_stats[self.striker_idx]
        non_striker = self.batsmen_stats[self.non_striker_idx]
        bowler = self.bowler_stats[self.current_bowler_idx]
        
        # 2. Select bowler for new over (if needed)
        current_balls = self.t1_balls if self.innings == 1 else self.t2_balls
        if current_balls > 0 and current_balls % 6 == 0 and self.last_event is not None:
            # Over completed, select new bowler (not the one who just bowled)
            allowed_bowlers = [i for i in range(len(self.bowler_stats)) if i != self.current_bowler_idx]
            self.current_bowler_idx = random.choice(allowed_bowlers)
            bowler = self.bowler_stats[self.current_bowler_idx]
            
        # 3. Simulate ball event
        # Probabilities adjusted for T20 batting (dot, single, boundaries, extras, wicket)
        rand = random.random()
        
        is_legal_ball = True
        runs = 0
        event_str = ""
        is_wicket = False
        extra_type = None
        
        if rand < 0.05:  # 5% Wicket
            is_wicket = True
            runs = 0
        elif rand < 0.08:  # 3% Extra (Wide / No Ball)
            is_legal_ball = False
            runs = 1  # 1 extra run added to team
            extra_type = "Wide" if random.random() < 0.8 else "No Ball"
        elif rand < 0.38:  # 30% Dot Ball
            runs = 0
        elif rand < 0.73:  # 35% Single
            runs = 1
        elif rand < 0.83:  # 10% Two Runs
            runs = 2
        elif rand < 0.85:  # 2% Three Runs
            runs = 3
        elif rand < 0.93:  # 8% Four
            runs = 4
            self.last_event = "four"
        else:  # 7% Six
            runs = 6
            self.last_event = "six"
            
        # Over/Ball indicators
        balls_in_over = (current_balls % 6) + 1 if is_legal_ball else (current_balls % 6)
        over_num = current_balls // 6
        ball_label = f"{over_num}.{balls_in_over}"
        
        # Process outcomes
        if not is_legal_ball:
            # Extra run
            if self.innings == 1:
                self.t1_runs += runs
            else:
                self.t2_runs += runs
                
            bowler["runs_conceded"] += runs
            commentary_text = f"{ball_label} - {bowler['name']} to {striker['name']}, {extra_type}! 1 Run added to extras."
            self.commentary.append(commentary_text)
            
            # Momentum slight dip
            self.momentum = max(-5, self.momentum - 1)
            
        else:
            # Legal ball
            if self.innings == 1:
                self.t1_balls += 1
                self.t1_overs = self.get_overs_string(self.t1_balls)
            else:
                self.t2_balls += 1
                self.t2_overs = self.get_overs_string(self.t2_balls)
                
            striker["balls"] += 1
            bowler["balls_bowled"] += 1
            bowler["overs"] = self.get_overs_string(bowler["balls_bowled"])
            
            if is_wicket:
                self.last_event = "wicket"
                if self.innings == 1:
                    self.t1_wickets += 1
                else:
                    self.t2_wickets += 1
                    
                bowler["wickets"] += 1
                
                # Formulate wicket details
                dismissal_types = [
                    f"c {random.choice(self.t2_roster if self.innings == 1 else self.t1_roster)} b {bowler['name']}",
                    f"b {bowler['name']}",
                    f"lbw b {bowler['name']}",
                    "run out (Direct Hit)"
                ]
                how_out = random.choice(dismissal_types)
                striker["status"] = "out"
                striker["how_out"] = how_out
                
                commentary_text = f"{ball_label} - 💥 WICKET! {striker['name']} {how_out} for {striker['runs']} runs. The crowd goes silent!"
                self.commentary.append(commentary_text)
                play_sound_async("wicket")
                
                # Check for next batsman
                curr_wickets = self.t1_wickets if self.innings == 1 else self.t2_wickets
                if curr_wickets < 10:
                    # Bring next bat
                    next_bat_idx = max(self.striker_idx, self.non_striker_idx) + 1
                    while next_bat_idx < len(self.batsmen_stats) and self.batsmen_stats[next_bat_idx]["status"] != "yet_to_bat":
                        next_bat_idx += 1
                        
                    if next_bat_idx < len(self.batsmen_stats):
                        self.striker_idx = next_bat_idx
                        self.batsmen_stats[self.striker_idx]["status"] = "batting"
                    
                # Heavy momentum swing to bowler
                self.momentum = -4
                
            else:
                # Regular runs
                if self.innings == 1:
                    self.t1_runs += runs
                else:
                    self.t2_runs += runs
                    
                striker["runs"] += runs
                bowler["runs_conceded"] += runs
                
                # Add sound alerts for boundaries
                if runs == 4:
                    striker["fours"] += 1
                    commentary_text = f"{ball_label} - 🔥 FOUR! {striker['name']} smashes {bowler['name']} through covers for boundary."
                    play_sound_async("four")
                    self.momentum = min(5, self.momentum + 3)
                elif runs == 6:
                    striker["sixes"] += 1
                    commentary_text = f"{ball_label} - 🚀 SIX! {striker['name']} launches {bowler['name']} deep into the stands!"
                    play_sound_async("six")
                    self.momentum = min(5, self.momentum + 4)
                elif runs == 0:
                    commentary_text = f"{ball_label} - {bowler['name']} to {striker['name']}, no run, defended solidly."
                    self.momentum = max(-5, self.momentum - 1)
                else:
                    commentary_text = f"{ball_label} - {bowler['name']} to {striker['name']}, {runs} run(s), tucked away."
                    self.momentum = int((self.momentum + runs) / 2)
                    
                self.commentary.append(commentary_text)
                
                # Rotate strike on singles/triples
                if runs in [1, 3]:
                    self.striker_idx, self.non_striker_idx = self.non_striker_idx, self.striker_idx
                    
            # Over completion check
            updated_balls = self.t1_balls if self.innings == 1 else self.t2_balls
            if updated_balls > 0 and updated_balls % 6 == 0 and is_legal_ball:
                # End of over: swap ends for next over
                self.striker_idx, self.non_striker_idx = self.non_striker_idx, self.striker_idx
                self.commentary.append(f"End of Over {updated_balls // 6}. Score: {self.t1_runs if self.innings == 1 else self.t2_runs}/{self.t1_wickets if self.innings == 1 else self.t2_wickets}")
                
                # Select a new bowler who didn't bowl this over
                allowed_bowlers = [i for i in range(len(self.bowler_stats)) if i != self.current_bowler_idx]
                self.current_bowler_idx = random.choice(allowed_bowlers)
                
        # 4. Check Innings completions
        t_runs = self.t1_runs if self.innings == 1 else self.t2_runs
        t_wickets = self.t1_wickets if self.innings == 1 else self.t2_wickets
        t_balls = self.t1_balls if self.innings == 1 else self.t2_balls
        
        # Innings 1 over
        if self.innings == 1:
            if t_wickets == 10 or t_balls >= 120:
                self.target = self.t1_runs + 1
                self.innings = 2
                self.commentary.append(f"★ Innings Break! {self.batting_team} finishes at {self.t1_runs}/{self.t1_wickets} in {self.t1_overs} overs.")
                self.commentary.append(f"★ {self.bowling_team} needs {self.target} runs to win in 120 balls.")
                
                # Swap batting & bowling
                self.batting_team_code, self.bowling_team_code = self.bowling_team_code, self.batting_team_code
                self.batting_team = IPL_TEAMS[self.batting_team_code]["name"]
                self.bowling_team = IPL_TEAMS[self.bowling_team_code]["name"]
                
                # Initialize new innings players
                self.initialize_innings_players()
                
        # Innings 2 over
        else:
            # Chased down target
            if self.t2_runs >= self.target:
                self.is_over = True
                wickets_left = 10 - self.t2_wickets
                balls_left = 120 - self.t2_balls
                self.winner = self.batting_team
                self.result_statement = f"🏆 {self.batting_team} won by {wickets_left} wickets (with {balls_left} balls remaining)!"
                self.commentary.append(f"🏁 MATCH FINISHED! {self.result_statement}")
                save_match_to_history(self.get_summary_dict())
                
            # Wickets out or overs finished
            elif self.t2_wickets == 10 or self.t2_balls >= 120:
                self.is_over = True
                if self.t2_runs == self.target - 1:
                    self.winner = "Tie"
                    self.result_statement = "👔 MATCH TIED! Super over matches are scheduled!"
                else:
                    self.winner = self.bowling_team
                    runs_difference = (self.target - 1) - self.t2_runs
                    self.result_statement = f"🏆 {self.bowling_team} won by {runs_difference} runs!"
                self.commentary.append(f"🏁 MATCH FINISHED! {self.result_statement}")
                save_match_to_history(self.get_summary_dict())
                
        # 5. Dynamic win probability, POTM Predictor & momentum
        self.update_live_analytics()

    def update_live_analytics(self):
        """Calculates win probability and Player of the Match updates dynamically"""
        # A simple algorithm to estimate win probability
        if self.innings == 1:
            # Innings 1: standard score-based projections
            if self.t1_balls == 0:
                self.win_prob = 50.0
            else:
                proj_score = (self.t1_runs / self.t1_balls) * 120
                # Cap project score scaling
                ratio = proj_score / 170.0  # 170 is par
                prob = 50.0 * ratio
                # Subtract based on wickets lost
                prob -= self.t1_wickets * 4.0
                self.win_prob = max(10, min(90, round(prob, 1)))
        else:
            # Innings 2: required runs vs balls left
            if self.is_over:
                self.win_prob = 100.0 if self.winner == self.batting_team else 0.0
            else:
                runs_needed = self.target - self.t2_runs
                balls_left = 120 - self.t2_balls
                wickets_lost = self.t2_wickets
                
                if balls_left <= 0:
                    self.win_prob = 0.0
                else:
                    req_rr = (runs_needed / (balls_left / 6))
                    # Calculate ratio compared to a reasonable chase
                    base_prob = 100.0 - (req_rr * 7.5) # higher required run rate reduces win probability
                    # Adjust for wickets left
                    wickets_penalty = wickets_lost * 8.0
                    final_prob = base_prob - wickets_penalty + 30.0
                    self.win_prob = max(5, min(95, round(final_prob, 1)))
                    
        # Player of the match predictor logic
        # Pick batsman with highest runs or bowler with most wickets
        top_batsman = max(self.batsmen_stats, key=lambda x: x["runs"])
        top_bowler = max(self.bowler_stats, key=lambda x: x["wickets"])
        
        if top_batsman["runs"] > 40:
            self.potm_predict = f"{top_batsman['name']} ({top_batsman['runs']} off {top_batsman['balls']})"
        elif top_bowler["wickets"] >= 2:
            self.potm_predict = f"{top_bowler['name']} ({top_bowler['wickets']}/{top_bowler['runs_conceded']})"
        else:
            # fallback
            self.potm_predict = f"{top_batsman['name']}"

    def get_summary_dict(self):
        """Returns match summary dictionary suited for history storage"""
        return {
            "team1": self.team1,
            "team2": self.team2,
            "t1_runs": self.t1_runs,
            "t1_wickets": self.t1_wickets,
            "t1_overs": self.t1_overs,
            "t2_runs": self.t2_runs,
            "t2_wickets": self.t2_wickets,
            "t2_overs": self.t2_overs,
            "winner": self.winner,
            "result_statement": self.result_statement
        }
