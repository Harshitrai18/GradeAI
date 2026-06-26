from scipy.stats import percentileofscore
import pandas as pd

def calculate_performance(df):

    quiz_cols=[
        c for c in df.columns
        if "Quiz_" in c
    ]

    df["Total Marks"]=df[quiz_cols].sum(axis=1)

    max_marks = len(quiz_cols) * 25

    df["Percentage"]=(
        df["Total Marks"]/max_marks
    )*100

    percentiles=[]

    for score in df["Total Marks"]:

        p=percentileofscore(
            df["Total Marks"],
            score
        )

        percentiles.append(round(p,2))

    df["Percentile"]=percentiles

    df["Rank"]=(
        df["Total Marks"]
        .rank(
            ascending=False,
            method="dense"
        )
        .astype(int)
    )

    return df