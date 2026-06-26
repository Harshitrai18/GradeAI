import pandas as pd
import os

def merge_quizzes():

    folder = "data/quizzes"

    files = sorted([
        f for f in os.listdir(folder)
        if f.endswith(".csv")
    ])

    master = None

    for i, file in enumerate(files):

        path = os.path.join(folder, file)

        df = pd.read_csv(path)

        print(f"Processing {file}")

        # Keep only Email and Total score
        df = df[["Email", "Total score"]]

        # Convert values like "18.00 / 25" into 18
        df["Total score"] = (
            df["Total score"]
            .astype(str)
            .str.split("/")
            .str[0]
            .str.strip()
            .astype(float)
        )

        df.rename(
            columns={
                "Total score": f"Quiz_{i+1}"
            },
            inplace=True
        )

        if master is None:
            master = df

        else:
            master = pd.merge(
                master,
                df,
                on="Email",
                how="outer"
            )

    quiz_cols = [col for col in master.columns if col.startswith("Quiz_")]

    master[quiz_cols] = master[quiz_cols].fillna(0)

    return master