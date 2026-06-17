import pandas as pd
import io

RAW_CSV = """StudentID,Name,Gender,Age,Subject,Score,Grade,City
1,Alice,Female,20,Math,88,B,Mumbai
2,Bob,Male,22,Science,75,C,Delhi
3,Carol,Female,21,Math,92,A,Mumbai
4,David,Male,23,English,60,D,Chennai
5,Eve,Female,20,Science,95,A,Mumbai
6,Frank,Male,24,Math,,B,Delhi
7,Grace,Female,22,English,78,C,
8,Henry,Male,21,Science,82,B,Chennai
9,Ivy,Female,23,Math,55,F,Delhi
10,Jack,Male,20,English,90,A,Mumbai
11,Karen,Female,22,Science,NaN,C,Chennai
12,Leo,Male,21,Math,70,C,Delhi
13,Mia,Female,24,English,85,B,Mumbai
14,Nick,Male,20,Science,65,D,
15,Olivia,Female,23,Math,98,A,Chennai
16,Paul,Male,22,English,72,C,Delhi
17,Quinn,Female,21,Science,88,B,Mumbai
18,Ray,Male,24,Math,45,F,Chennai
19,Sara,Female,20,English,91,A,Delhi
20,Tom,Male,23,Science,77,C,Mumbai
"""

if __name__ == "__main__":

    # io.StringIO lets us read the string like a file
    try:
        df = pd.read_csv(io.StringIO(RAW_CSV))
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        raise SystemExit(1)

    print("=== Dataset Overview ===")
    print(f"Shape: {df.shape}")
    print(f"\nFirst 5 rows:\n{df.head().to_string(index=False)}")
    print(f"\nMissing values:\n{df.isnull().sum().to_string()}")

    print("\n=== Cleaning ===")
    median_score = df["Score"].median()
    # fill missing scores with median to avoid skewing the average
    df["Score"] = df["Score"].fillna(median_score)
    # ensure the column is treated as numeric
    df["Score"] = pd.to_numeric(df["Score"])
    print(f"Filled missing scores with median: {median_score}")

    # replace missing city names with a placeholder
    df["City"] = df["City"].fillna("Unknown")
    print("Filled missing cities with Unknown")

    df = df.drop_duplicates()

    print("\n=== Filtering ===")

    # boolean indexing selects rows where the condition is True
    high = df[df["Score"] > 85]
    print(f"\nStudents scoring above 85 ({len(high)} found):")
    print(high[["Name", "Subject", "Score"]].to_string(index=False))

    # multiple conditions combined with & must each be in parentheses
    female_math = df[(df["Gender"] == "Female") & (df["Subject"] == "Math")]
    print(f"\nFemale students in Math ({len(female_math)} found):")
    print(female_math[["Name", "Score", "City"]].to_string(index=False))

    failed = df[df["Score"] < 60]
    print(f"\nStudents who failed ({len(failed)} found):")
    print(failed[["Name", "Subject", "Score"]].to_string(index=False))

    print("\n=== Grouping & Aggregation ===")

    subject_stats = (
        df.groupby("Subject")["Score"]
        .agg(Average="mean", Highest="max", Lowest="min", Count="count")
        .round(2)
        .sort_values("Average", ascending=False)
    )
    print(f"\nAverage Score by Subject:\n{subject_stats.to_string()}")

    city_avg = df.groupby("City")["Score"].mean().round(2).sort_values(ascending=False)
    print(f"\nAverage Score by City:\n{city_avg.to_string()}")

    gender_stats = df.groupby("Gender")["Score"].agg(Average="mean", Count="count").round(2)
    print(f"\nScore by Gender:\n{gender_stats.to_string()}")

    print(f"\nGrade Distribution:\n{df['Grade'].value_counts().sort_index().to_string()}")

    print("\n=== Key Insights ===")
    print(f"\nDescriptive Stats:\n{df['Score'].describe().round(2).to_string()}")

    # idxmax/idxmin return the index of the highest/lowest value
    top = df.loc[df["Score"].idxmax()]
    bottom = df.loc[df["Score"].idxmin()]
    pass_rate = (df["Score"] >= 60).mean() * 100

    print(f"\nTop scorer: {top['Name']} - {top['Score']:.0f} in {top['Subject']}")
    print(f"Lowest score: {bottom['Name']} - {bottom['Score']:.0f} in {bottom['Subject']}")
    print(f"Pass rate: {pass_rate:.1f}%")
    print(f"Best subject: {df.groupby('Subject')['Score'].mean().idxmax()}")
    print(f"Best city: {df.groupby('City')['Score'].mean().idxmax()}")

    # index=False prevents writing row numbers as an extra column
    try:
        df.to_csv("cleaned_students.csv", index=False)
        print("\nCleaned data saved to cleaned_students.csv")
    except IOError as e:
        print(f"Failed to save: {e}")
