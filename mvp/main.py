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
async def form_get(request: Request):
    tables = ['att_tb', 'deal_tb']
    aggs = ['info', 'value_counts', 'describe', 'sort_values']
    return templates.TemplateResponse('form1.html', context={'request': request, 'tables': tables, 'aggs': aggs})


@app.post("/form", response_class=HTMLResponse)
async def form_post(request: Request):
    r = await request.json()
    print(r)
    tables = ("att_tb", "deal_tb")
    col = None
    buf = io.StringIO()
    db, df = None, "Invalid Query"
    if r['tables'] in tables:
        db = deta.Base(r['tables'])
        result = db.fetch()
        df = pd.DataFrame(dict(ChainMap(*result.items)))
    if not isinstance(df, str):
        aggs = ('info', 'value_counts', 'describe', 'sort_values')
        if r['aggs'] in aggs:
            if r['aggs'] == 'sort_values' and col is not None:
                h = df.agg('sort_values', by=col)
                return templates.TemplateResponse('form1.html', {'request': request, 'agged': h.to_html()})
            else:
                h = df.agg(r['aggs'])

            if isinstance(h, pd.Series):
                return templates.TemplateResponse('form1.html', {'request': request, 'agged': h.to_frame().to_html()})
            elif h is None:
                df.info(buf=buf)
                s = buf.getvalue()
                return templates.TemplateResponse('form1.html', {'request': request, 'agged': s})
            else:
                return templates.TemplateResponse('form1.html', {'request': request, 'agged': "FUCK YOU"})
    return templates.TemplateResponse('form1.html', context={'request': request, 'agged': df})


@app.get("/form/rowscols")
async def row_cols(request: Request, table: str):
    db = deta.Base(table)
    result = db.fetch()
    df = pd.DataFrame(dict(ChainMap(*result.items)))
    shape = df.shape
    return templates.TemplateResponse('form1.html', context={'request': request, 'columns': shape[1], 'rows': shape[0]})


@app.get("/form/?tables={table}&aggs={agg}")
async def parse_input(request: Request, table: str, agg: str):
    if table in ('att_tb', 'deal_tb'):
        db = deta.Base(table)
    else:
        return templates.TemplateResponse('form1.html', context={'request': request, 'result': "Table not found"})
    result = db.fetch()
    df = pd.DataFrame(dict(ChainMap(*result.items)))
    return heuristics(request, df, agg)


def heuristics(request, r, df, buf=io.StringIO(), aggs=('info', 'value_counts', 'describe', 'sort_values'), col=None):
    if r['aggs'] in aggs:
        if r['aggs'] == 'sort_values' and col is not None:
            h = df.agg('sort_values', by=col)
            return templates.TemplateResponse('form1.html', {'request': request, 'result': h.to_html()})
        else:
            h = df.agg(r['aggs'])

        if isinstance(h, pd.Series):
            return templates.TemplateResponse('form1.html', {'request': request, 'result': h.to_frame().to_html()})
        elif h is None:
            df.info(buf=buf)
            s = buf.getvalue()
            return templates.TemplateResponse('form1.html', {'request': request, 'result': s})
        else:
            return templates.TemplateResponse('form1.html', {'request': request, 'result': h.to_html()})

    return templates.TemplateResponse('form1.html', {'request': request, 'result': df.to_html()})


if __name__ == '__main__':
    pass
