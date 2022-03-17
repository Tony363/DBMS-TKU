import os
import codecs
import pandas as pd
import numpy as np
from deta import Deta
from dotenv import load_dotenv


def parse(entry):
    if isinstance(entry, float) and np.isnan(entry):
        return "Nan"
    elif isinstance(entry, float):
        return entry
    elif isinstance(entry, str):
        return entry.replace(" ", "_")
    return entry


def load_data(db, df):
    for col in df.columns:
        print("Column:", col)
        print("Contemts", df[col].apply(parse).tolist())
        db.put({col: df[col].apply(parse).tolist()}, key=col)


if __name__ == '__main__':
    load_dotenv()
    deta = Deta(os.environ.get('key'))
    att_tb = deta.Base("att_tb")
    deal_tb = deta.Base("deal_tb")
    with codecs.open("deal.csv", "r", encoding="utf-8", errors='ignore') as f:
        deal = pd.read_csv(f)
    att = pd.read_csv("companyatt.csv")
    load_data(att_tb, att)
    load_data(deal_tb, deal)
