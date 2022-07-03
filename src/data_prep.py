import pandas as pd

def transform_data(out: dict):

    out_df = pd.DataFrame(out["data"])
    out_df["created_date"] = pd.to_datetime(out_df["created_at"])
    out_df["text_modified"] = out_df["text"].str.lower()

    out_df["tokens"] = out_df["text_modified"].str.split()
    flat_ls = [item for sublist in out_df["tokens"].values for item in sublist]

    return out_df, flat_ls