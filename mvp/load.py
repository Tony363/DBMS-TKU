import codecs
import pandas as pd
import numpy as np
from deta import Deta


def load_data(db, df):
    for col in df.columns:
        print("Column:", col)
        print("Entry", type(df[col][0]), df[col][0])
        for idx, entry in enumerate(df[col]):
            if isinstance(entry, float) and np.isnan(entry):
                db.put({col: None}, key=col+"_"+str(idx))
            elif isinstance(entry, float):
                db.put({col: entry}, key=col+"_"+str(idx))
            elif isinstance(entry, str):
                db.put({col: entry.replace(" ", "_")}, key=col+"_"+str(idx))


if __name__ == '__main__':
    deta = Deta("c0crlho4_sW8nwjtvQEHsY2k5HS9B3iHTvA6PQ8c7")
    att_tb = deta.Base("att_tb")
    deal_tb = deta.Base("deal_tb")
    with codecs.open("deal.csv", "r", encoding="utf-8", errors='ignore') as f:
        deal = pd.read_csv(f)
    att = pd.read_csv("companyatt.csv")
    load_data(att_tb, att)
    # load_data(deal_tb, deal)
