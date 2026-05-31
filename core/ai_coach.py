import pandas as pd

class AICoach:

    def __init__(self, hero_df):
        self.hero_df = hero_df

    def recommend_pick(self, role, enemy_comp):
        pool = self.hero_df[self.hero_df["role"] == role]

        # Simple AI scoring (upgradeable to ML later)
        pool["score"] = (
            pool["win_rate"] * 0.5 +
            pool["pick_rate"] * 0.3 +
            pool["ban_pressure"] * 0.2
        )

        best = pool.sort_values("score", ascending=False).head(3)

        return best[["hero", "score"]]

    def counter_pick(self, enemy_hero):
        counters = self.hero_df[self.hero_df["counters"].str.contains(enemy_hero)]
        return counters[["hero", "win_rate"]].sort_values("win_rate", ascending=False)
