"""
In this problem, you will need to read the JSON file from problem one and
analyze and visualize the data. Code and output should be in code/problem2 and
output/problem2.

1. Find the min, max, mean and std of each numerical variable (not nominal
or ordinal).
2. Visualize the distribution of “DaysToGo” using a histogram.
3. Use lmplot or joinplot and visualize the distribution of DollarsPledged
with DollarsGoal, and DollarsPledged with NumBackers.
"""

import os
import json
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns

DEBUG = False
DIVIDER = '*' * 100
INPUT_FILE = "../../output/problem1/data.json"  # dummy.json / data.json
OUTPUT_DIR = "../../output/problem2"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_problem1_json_to_dataframe(input_file) -> DataFrame:
    """
    Loads the JSON data from the input file
    @param input_file: The path to the input file
    @return: The JSON data loaded from the input file
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    records = data["records"]["record"]
    data = pd.DataFrame(records)  # in case required to normalize the data,
    # replace with the following: data = normalize_data(records)

    if DEBUG:
        print(DIVIDER)
        pd.set_option('display.width', None)
        print(data.head(10))
        print(data.shape)

    return data


def normalize_data(json_data) -> DataFrame:
    """
    Uses pandas' json_normalize function to convert the JSON data into a
    DataFrame. It then identifies unique columns across all records, ensures
    all records have these columns, and fills any missing values with
    default values.
    @param json_data: The JSON data to be normalized
    @return: The normalized JSON data
    """
    df = pd.json_normalize(json_data)

    # Identify unique columns
    all_columns = set()
    for record in json_data:
        all_columns.update(record.keys())

    # Ensure all records have the same columns and fill blanks
    df = df.reindex(columns=all_columns)
    df = df.fillna({'id': '-1',
                    'url': 'Unknown',
                    'Creators': 'Unknown',
                    'Title': 'Unknown',
                    'Text': 'Unknown',
                    'DollarsPledged': 0,
                    'DollarsGoal': 0,
                    'NumBackers': 0,
                    'DaysToGo': 0,
                    'FlexibleGoal': False})

    return df


def problem_2_a(df: DataFrame):
    """
    Calculates and stores the minimum, maximum, mean,
    and standard deviation of numerical variables in the provided DataFrame.
    The results are then saved to a JSON file.
    @param df: The DataFrame loaded from the input file
    """
    numerical_vars = ['DollarsPledged', 'DollarsGoal', 'NumBackers',
                      'DaysToGo']
    stats = {}

    # Ensure numerical columns are of correct data type
    for var in numerical_vars:
        df[var] = df[var].astype(int)

    for var in numerical_vars:
        stats[var] = {
            'min': int(df[var].min()),
            'max': int(df[var].max()),
            'mean': float(df[var].mean()),
            'std': float(df[var].std())
        }

    if DEBUG:
        print(DIVIDER)
        print(json.dumps(stats, indent=2))

    # Save the statistics to a JSON file
    stats_output_file = os.path.join(OUTPUT_DIR, "stats.json")
    with open(stats_output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)


def problem_2_b_1(df: DataFrame, dpi: int = 100):
    """
    Visualizes the distribution of "DaysToGo" using a histogram.
    @param df: The DataFrame loaded from the input file
    @param dpi: The resolution of the uesr's screen
    """
    plt.figure(figsize=(1280 / dpi, 720 / dpi))
    sns.histplot(df['DaysToGo'], bins=int(df['DaysToGo'].max()))
    plt.title('Distribution of `DaysToGo`')
    plt.xlabel('DaysToGo')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(OUTPUT_DIR, '1_DaysToGo_histplot.png'))

    if DEBUG:
        plt.show()

    plt.close()


def problem_2_b_2(df: DataFrame):
    """
    Visualizes the distribution of DollarsPledged with DollarsGoal,
    and DollarsPledged with NumBackers.
    @param df: The DataFrame loaded from the input file
    """
    # Distribution of `DollarsPledged` with `DollarsGoal`
    sns.lmplot(x='DollarsGoal', y='DollarsPledged', data=df, aspect=2)
    plt.savefig(
        os.path.join(OUTPUT_DIR,
                     '2.1_DollarsPledged_DollarsGoal_Dist_lmplot.png'))

    if DEBUG:
        plt.show()

    plt.close()

    # Distribution of `DollarsPledged` with `NumBackers`
    sns.lmplot(x='NumBackers', y='DollarsPledged', data=df, aspect=2)
    plt.savefig(
        os.path.join(OUTPUT_DIR,
                     '2.2_DollarsPledged_NumBackers_Dist_lmplot.png'))

    if DEBUG:
        plt.show()

    plt.close()


def main():
    raw_data = load_problem1_json_to_dataframe(INPUT_FILE)
    problem_2_a(raw_data)
    problem_2_b_1(raw_data)
    problem_2_b_2(raw_data)

    print(f"Statistics and visualizations saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
