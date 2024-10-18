import pandas as pd
from sklearn.metrics import cohen_kappa_score
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns

# List of raters
RATERS = [
    "rater_1",
    "rater_2",
    "rater_3",
    "rater_4",
    "rater_5"
]


# 1. Function to show QWK between rater pairs
def show_qwk(df):
    qwk_scores = []
    for rater_1, rater_2 in combinations(RATERS, 2):
        scores_rater_1 = df[rater_1].values
        scores_rater_2 = df[rater_2].values
        qwk_score = cohen_kappa_score(scores_rater_1, scores_rater_2, weights='quadratic')
        qwk_scores.append(qwk_score)
        print(f"QWK between {rater_1} and {rater_2}: {qwk_score:.4f}")
    average_qwk = sum(qwk_scores) / len(qwk_scores)
    print(f"\nAverage QWK across all raters: {average_qwk:.4f}")


# 2. Function to show score distribution per rater
def show_score_distribution(df):
    for rater in RATERS:
        print(f"\nScore distribution for {rater}:")
        print(df[rater].describe())  # Show basic statistics like mean, std, etc.


# 3. Function to show variance per question (agreement between raters)
def show_variance_per_question(df):
    question_variances = df[RATERS].var(axis=1)
    print("\nVariance per question (higher variance = less agreement):")
    print(question_variances)


# 4. Function to find outliers (answers where max-min difference is large)
def find_outliers(df, threshold=2):
    outliers = df.apply(lambda row: row[RATERS].max() - row[RATERS].min(), axis=1)
    print(f"\nOutliers (Max-Min Difference > {threshold}) per answer:")
    print(outliers[outliers > threshold])


# 5. Function to show correlation matrix between raters
def show_rater_correlation(df):
    print("\nCorrelation matrix between raters:")
    print(df[RATERS].corr())


# 6. Plot score distribution (Histogram)
def plot_score_distribution(df):
    plt.figure(figsize=(10, 6))
    for rater in RATERS:
        sns.histplot(df[rater], kde=True, label=rater, bins=10, element="step")
    plt.title('Score Distribution Per Rater')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()


# 7. Plot variance per question (Bar plot)
def plot_variance_per_question(df):
    question_variances = df[RATERS].var(axis=1)
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(question_variances)), question_variances)
    plt.title('Variance Per Question')
    plt.xlabel('Question Index')
    plt.ylabel('Variance')
    plt.show()


# 8. Plot outliers (Boxplot)
def plot_outliers(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df[RATERS])
    plt.title('Outliers in Rater Scores')
    plt.xlabel('Raters')
    plt.ylabel('Score')
    plt.show()


# 9. Plot correlation matrix (Heatmap)
def plot_rater_correlation(df):
    correlation_matrix = df[RATERS].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=0, vmax=1)
    plt.title('Correlation Matrix Between Raters')
    plt.show()


# Main code to execute all analyses and visualizations
if __name__ == '__main__':
    # Load the dataset
    df_answers = pd.read_csv("data/answers.csv")

    # 1. Show Quadratic Weighted Kappa (QWK) between rater pairs
    print("=== QWK Between Raters ===")
    show_qwk(df_answers)

    # 2. Show score distribution per rater
    print("\n=== Score Distribution Per Rater ===")
    show_score_distribution(df_answers)
    plot_score_distribution(df_answers)  # Visualize score distribution

    # 3. Show variance per question (agreement between raters)
    print("\n=== Variance Per Question ===")
    show_variance_per_question(df_answers)
    plot_variance_per_question(df_answers)  # Visualize variance per question

    # 4. Find outliers (large differences between rater scores for the same answer)
    print("\n=== Outliers in Scoring ===")
    find_outliers(df_answers, threshold=2)
    plot_outliers(df_answers)  # Visualize outliers

    # 5. Show correlation matrix between raters
    print("\n=== Correlation Between Raters ===")
    show_rater_correlation(df_answers)
    plot_rater_correlation(df_answers)  # Visualize correlation between raters
