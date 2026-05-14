import pandas as pd


URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"


def extract_airports():
    df = pd.read_csv(URL)
    df.to_csv("data/raw/airports.csv", index=False)
    print(f"Extracted {len(df)} rows")
    return df


if __name__ == "__main__":
    extract_airports()