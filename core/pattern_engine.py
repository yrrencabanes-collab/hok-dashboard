class PatternEngine:

    def __init__(self, df):
        self.df = df

    def detect_playstyle(self, team):
        data = self.df[self.df["team"] == team]

        early_game = data["first_10min_gold_diff"].mean()
        aggression = data["kills_per_game"].mean()

        if aggression > 15:
            style = "Aggressive Snowball"
        elif early_game < 0:
            style = "Late Game Scaling"
        else:
            style = "Balanced Control"

        return style
