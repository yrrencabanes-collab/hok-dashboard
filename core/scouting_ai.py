import pandas as pd
from collections import Counter

class ScoutingAI:

    def __init__(self, match_history_df):
        self.df = match_history_df

    def team_identity_profile(self, team_name):
        team_data = self.df[self.df["team"] == team_name]

        hero_pool = Counter(team_data["hero"])
        role_bias = Counter(team_data["role"])

        return {
            "top_heroes": hero_pool.most_common(5),
            "role_preference": role_bias,
            "avg_game_style": team_data["playstyle"].mode()[0]
        }

    def predict_next_heroes(self, team_name):
        profile = self.team_identity_profile(team_name)

        top_heroes = [h[0] for h in profile["top_heroes"]]

        # probability-style weighting simulation
        predictions = []
        for hero in top_heroes:
            predictions.append({
                "hero": hero,
                "pick_probability": 0.65  # upgraded later to ML model
            })

        return sorted(predictions, key=lambda x: x["pick_probability"], reverse=True)
