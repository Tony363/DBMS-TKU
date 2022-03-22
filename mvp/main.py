import os
import io
import pandas as pd
import numpy as np
from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from deta import Deta
from dotenv import load_dotenv
from collections import ChainMap
from pydantic import BaseModel
from typing import Optional

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/dist", StaticFiles(directory="dist"), name="dist")

templates = Jinja2Templates("templates")

deta = Deta(os.environ.get('key'))


class data(BaseModel):
    table: Optional[str] = None
    aggregration: Optional[str] = None


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.get("/form")
async def form_get(request: Request,
                   tables=("att_tb", "deal_tb"),
                   aggs=('info', 'value_counts', 'describe', 'sort_values'),
                   ):
    return templates.TemplateResponse('form.html', context={'request': request, 'tables': tables, 'aggs': aggs})

# set header no cache to inidicate dynamic  hidden page, don't load from cache, completely different html file
# sort_values, fuzzy matching, drop down


@app.post("/form", response_class=HTMLResponse)
async def form_post(
    request: Request,
    table: str = Form(None),
    agg: str = Form(None),
    tables=("att_tb", "deal_tb"),
    aggs=('info', 'value_counts', 'describe', 'sort_values')
):
    db, df = None, "Invalid Query"
    if table in tables:
        db = deta.Base(table)
        result = db.fetch()
        df = pd.DataFrame(dict(ChainMap(*result.items)))
    if not isinstance(df, str):
        return heuristics(request, agg, table, df)
    return templates.TemplateResponse('form.html', context={'request': request, 'tables': tables, 'aggs': aggs})


@app.post("/form/indexing")
async def row_cols(
    request: Request,
    cols: str = Form(None),
    rows: str = Form(None),
    agg: str = Form(None),
    table: str = Form(None),
    tables=("att_tb", "deal_tb"),
    aggs=('info', 'value_counts', 'describe', 'sort_values')
):
    db, df = None, "Invalid Query"
    if table not in tables:
        return templates.TemplateResponse('form.html', context={'request': request, 'tables': tables, 'aggs': aggs})
    db = deta.Base(table)
    if db and cols:
        df = pd.DataFrame(db.get(cols))[:int(
            rows) if isinstance(rows, str) and rows.isdigit() else None]
    elif db and rows:
        df = pd.DataFrame(dict(ChainMap(*db.fetch().items)))[:int(rows)]
    if isinstance(df, str) or df.empty:
        result = db.fetch()
        df = pd.DataFrame(dict(ChainMap(*result.items)))
        return heuristics(request, agg, table, df)
    return heuristics(request, agg, table, df, col=cols)


@app.get("/form/?tables={table}&aggs={agg}")
async def parse_input(request: Request, table: str, agg: str):
    if table in ('att_tb', 'deal_tb'):
        db = deta.Base(table)
    else:
        return templates.TemplateResponse('form1.html', context={'request': request, 'result': "Table not found"})
    result = db.fetch()
    df = pd.DataFrame(dict(ChainMap(*result.items)))
    return heuristics(request, df, agg)


def heuristics(request, agg, table, df,
               buf=io.StringIO(),
               aggs=('info', 'value_counts', 'describe', 'sort_values'),
               tables=("att_tb", "deal_tb"),
               col=None):
    context = {
        'request': request,
        'agged': None,
        'columns': df.columns,
        'rows': df.shape[0],
        'table': table,
        'agg': agg,
    }
    if agg in aggs:
        if agg == 'sort_values' and col is not None:  # TO DO check col in columns
            h = df.agg('sort_values', by=col)
            context['agged'] = h.to_html()
            return templates.TemplateResponse('form1.html', context=context)
        else:
            h = df.agg(agg)

        if isinstance(h, pd.Series):
            context['agged'] = h.to_frame().to_html()
            return templates.TemplateResponse('form1.html', context=context)
        elif h is None:
            df.info(buf=buf)
            s = buf.getvalue()
            context['agged'] = s
            return templates.TemplateResponse('form1.html', context=context)
        else:
            context['agged'] = h.to_html()
            return templates.TemplateResponse('form1.html', context=context)
    context['agged'] = df.to_html()
    return templates.TemplateResponse('form.html', context=context)


if __name__ == '__main__':
    pass
