class DraftEngine:

    def suggest_draft(self, allies, enemies, hero_df):
        available = hero_df[~hero_df["hero"].isin(allies + enemies)]

        available["draft_value"] = (
            available["win_rate"] +
            available["synergy_score"] -
            available["countered_by_enemy_score"]
        )

        return available.sort_values("draft_value", ascending=False).head(5)
