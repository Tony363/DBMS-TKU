import codecs
import pandas as pd
from sqlalchemy import create_engine

if __name__ == '__main__':
    deal_df = None
    with codecs.open("deal.csv", "r", encoding="utf-8", errors='ignore') as f:
        deal_df = pd.read_csv(f)
    att_df = pd.read_csv("companyatt.csv")
    engine = create_engine('sqlite:///mvp.db', echo=False)

    deal_df.to_sql(name='deal_tb', con=engine,
                   if_exists='replace', index=False)
    att_df.to_sql(name='att_tb', con=engine, if_exists='replace', index=False)
