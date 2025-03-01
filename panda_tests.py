import pandas as pd


def read_parquet_file(file_path: str) -> pd.DataFrame:
    """
    Reads a Parquet file and returns its contents as a DataFrame.

    Args:
        file_path (str): Path to the Parquet file.

    Returns:
        pd.DataFrame: The data in the Parquet file as a DataFrame.
    """
    try:
        df = pd.read_parquet(file_path)
        print(df.info(verbose=True))
        return df
    except Exception as e:
        raise RuntimeError(f"Error reading Parquet file: {e}")


df = read_parquet_file("../data/textual_tailoring_all_annotations_filtred.parquet")

df = df[df["validated"] == True]
print(df.head(100).to_string())

