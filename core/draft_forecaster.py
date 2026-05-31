import numpy as np

class DraftForecaster:

    def __init__(self, scouting_ai, hero_pool_df):
        self.scouting_ai = scouting_ai
        self.hero_pool = hero_pool_df

    def simulate_enemy_draft(self, enemy_team):
        predicted = self.scouting_ai.predict_next_heroes(enemy_team)

        draft_order = []
        for i, hero in enumerate(predicted):

            # simulate ban/pick probability decay
            probability = hero["pick_probability"] * (1 - i * 0.1)

            draft_order.append({
                "hero": hero["hero"],
                "pick_likelihood": round(probability, 2)
            })

        return draft_order

    def predict_full_draft(self, enemy_team):
        draft = self.simulate_enemy_draft(enemy_team)

        return {
            "expected_bans": draft[:3],
            "expected_picks": draft[3:8]
        }
