import os


class Leaderboard:

    def __init__(self):

        self.file = "leaderboard.txt"

        self.scores = []

        self.load()



    # Load saved scores

    def load(self):

        if os.path.exists(self.file):

            with open(self.file, "r") as file:

                for line in file:

                    data = line.strip().split(",")

                    if len(data) == 2:

                        name = data[0]

                        score = int(data[1])

                        self.scores.append(
                            (name, score)
                        )




    # Add new score

    def add_score(self, name, score):

        self.scores.append(
            (name, score)
        )


        # Sort highest first

        self.scores.sort(
            key=lambda x: x[1],
            reverse=True
        )


        # Keep top 5

        self.scores = self.scores[:5]


        self.save()




    # Save scores

    def save(self):

        with open(self.file, "w") as file:

            for name, score in self.scores:

                file.write(
                    f"{name},{score}\n"
                )




    # Get scores

    def get_scores(self):

        return self.scores