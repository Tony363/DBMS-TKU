import os
import io
import pandas as pd
import numpy as np
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from deta import Deta
from dotenv import load_dotenv
from collections import ChainMap

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/dist", StaticFiles(directory="dist"), name="dist")

templates = Jinja2Templates("templates")

deta = Deta(os.environ.get('key'))


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.get("/form")
def form_post(request: Request):
    result1 = "Current Tables: (att_tb, deal_tb)"
    result2 = "Available aggregations: (desc|info|value_count)"
    return templates.TemplateResponse('form.html', context={'request': request, 'result1': result1, 'result2': result2})


@app.post("/form")
async def read(
    request: Request,
    table: str = Form("deal_tb"),
    col: str = Form("deal_id"),
    row: str = Form("1"),
    agg: str = Form("agg")
):
    tables = ("att_tb", "deal_tb")
    aggs = ('info', 'value_counts', 'describe')
    db, df = None, "Invalid Query"

    if table in tables:
        db = deta.Base(table)

    if db and col and row.isdigit():
        q = db.get(key=col)
        if q and int(row) < len(q[col]):
            df = pd.DataFrame(q)[:int(row)]
            return heuristics(request, df, agg, aggs)

    if db and db.get(key=col):
        df = pd.DataFrame(db.get(key=col))
        return templates.TemplateResponse('form.html', context={'request': request, 'result': df.to_html()})

    if db and row.isdigit():
        result = db.fetch()
        df = pd.DataFrame(dict(ChainMap(*result.items)))
        if int(row) < df.shape[0]:
            return templates.TemplateResponse('form.html', context={'request': request, 'result': df[:int(row)].to_html()})

    if db:
        result = db.fetch()
        df = pd.DataFrame(dict(ChainMap(*result.items)))
        return heuristics(request, df, agg, aggs)

    return templates.TemplateResponse('form.html', context={'request': request, 'result': df})


def heuristics(request, df, agg, aggs, buf=io.StringIO()):
    if agg in aggs:
        h = df.agg(agg)
        if isinstance(h, pd.Series):
            return templates.TemplateResponse('form.html', context={'request': request, 'result': h.to_frame().to_html()})
        elif h is None:
            df.info(buf=buf)
            s = buf.getvalue()
            print(s)
            return templates.TemplateResponse('form.html', context={'request': request, 'result': s})
        else:
            return templates.TemplateResponse('form.html', context={'request': request, 'result': h.to_html()})

    return templates.TemplateResponse('form.html', context={'request': request, 'result': df.to_html()})


if __name__ == '__main__':
    pass
