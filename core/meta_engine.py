import pandas as pd

class MetaEngine:

    def __init__(self, df):
        self.df = df

    def get_s_tier(self):
        return self.df[self.df["tier"] == "S"]

    def trending_heroes(self):
        return self.df.sort_values("pick_rate", ascending=False).head(10)

    def winrate_shift(self):
        self.df["meta_score"] = self.df["win_rate"] * self.df["pick_rate"]
        return self.df.sort_values("meta_score", ascending=False)
