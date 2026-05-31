class MatchAnalyzer:

    def generate_report(self, match_data):

        report = {
            "objective_control": match_data["towers_taken"] / match_data["towers_lost"],
            "teamfight_score": match_data["teamfight_win_rate"],
            "early_game_strength": match_data["first_10min_gold_diff"],
        }

        summary = "Team performed strong mid-game rotations." if report["teamfight_score"] > 0.6 else "Weak teamfight execution."

        return report, summary
