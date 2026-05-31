class CounterDraftAI:

    def generate_counter_draft(self, enemy_draft, hero_df):

        available = hero_df[~hero_df["hero"].isin(enemy_draft)]

        available["counter_value"] = (
            available["win_rate"] +
            available["against_meta_strength"] +
            available["team_synergy"]
        )

        return available.sort_values("counter_value", ascending=False).head(5)
