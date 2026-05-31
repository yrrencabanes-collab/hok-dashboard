class MetaIntelligence:

    def __init__(self, hero_df):
        self.df = hero_df

    def meta_pressure_score(self):
        self.df["meta_score"] = (
            self.df["win_rate"] * 0.5 +
            self.df["pick_rate"] * 0.3 +
            self.df["ban_rate"] * 0.2
        )
        return self.df.sort_values("meta_score", ascending=False)

    def counter_matrix(self, enemy_heroes):
        counters = self.df[self.df["counters"].apply(
            lambda x: any(e in x for e in enemy_heroes)
        )]
        return counters
