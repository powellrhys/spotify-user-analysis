import pandas as pd

def read_csv(path):

    # Read csv data path specified
    df = pd.read_csv(path)

    return df