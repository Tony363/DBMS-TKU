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
async def home(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.get("/form")
async def form_post(request: Request):
    # tables = ['att_tb', 'deal_tb']
    # aggs = ['info', 'value_counts', 'describe', 'sort_values']
    tables = "Available tables: att_tb,deal_tb"
    aggs = "Available aggregations: info,value_counts,describe,sort_values"
    return templates.TemplateResponse('form1.html', context={'request': request, 'tables': tables, 'aggs': aggs})


@app.get("/form/rowscols")
async def row_cols(request: Request, table: str):
    db = deta.Base(table)
    result = db.fetch()
    df = pd.DataFrame(dict(ChainMap(*result.items)))
    shape = df.shape
    return templates.TemplateResponse('form1.html', context={'request': request, 'columns': shape[1], 'rows': shape[0]})


@app.post("/form")
async def read(
    request: Request,
    table: str = Form("deal_tb"),
    col: str = Form("deal_id"),
    row: str = Form("1"),
    aggs: str = Form("agg")
):
    # add sorting, groupby, fuzzymatching, html drop down
    tables = ("att_tb", "deal_tb")
    db, df = None, "Invalid Query"
    if table in tables:
        db = deta.Base(table)

    if db and col and row.isdigit():
        q = db.get(key=col)
        if q and int(row) < len(q[col]):
            df = pd.DataFrame(q)[:int(row)]
            return heuristics(request, df, aggs, col=col)

    if db and db.get(key=col):
        df = pd.DataFrame(db.get(key=col))
        return heuristics(request, df, aggs, col=col)

    if db and row.isdigit():
        result = db.fetch()
        df = pd.DataFrame(dict(ChainMap(*result.items)))
        if int(row) < df.shape[0]:
            return heuristics(request, df[:int(row)], aggs, col=col)

    if db:
        result = db.fetch()
        df = pd.DataFrame(dict(ChainMap(*result.items)))
        return heuristics(request, df, aggs)

    return templates.TemplateResponse('form.html', context={'request': request, 'result': df})


def heuristics(request, df, agg, buf=io.StringIO(), aggs=('info', 'value_counts', 'describe', 'sort_values'), col=None):
    if agg in aggs:
        print(col)
        if agg == 'sort_values' and col is not None:
            h = df.agg('sort_values', by=col)
            return templates.TemplateResponse('form.html', context={'request': request, 'result': h.to_html()})
        else:
            h = df.agg(agg)
        if isinstance(h, pd.Series):
            return templates.TemplateResponse('form.html', context={'request': request, 'result': h.to_frame().to_html()})
        elif h is None:
            df.info(buf=buf)
            s = buf.getvalue()
            return templates.TemplateResponse('form.html', context={'request': request, 'result': s})
        else:
            return templates.TemplateResponse('form.html', context={'request': request, 'result': h.to_html()})

    return templates.TemplateResponse('form.html', context={'request': request, 'result': df.to_html()})


if __name__ == '__main__':
    pass
