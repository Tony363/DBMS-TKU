import os
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
templates = Jinja2Templates("templates")

deta = Deta(os.environ.get('key'))
db = deta.Base("mvpDB")


@app.get("/")
def home():
    return "Hello World"


@app.get("/form")
def form_post(request: Request):
    result = "Please query att_tb | deal_tb"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post("/form")
async def read(
    request: Request,
    table: str = Form("deal_tb"),
    col: str = Form("deal_id"),
    row: str = Form("1"),
    agg: str = Form("agg")
):
    tables = ("att_tb", "deal_tb")
    aggs = ('value_counts', 'describe')
    df = "Invalid Query"

    if table in tables:
        db = deta.Base(table)

    if db and col == "all" and row == "all":
        result = db.fetch()
        df = pd.DataFrame(dict(ChainMap(*result.items)))
        if agg in aggs:
            return templates.TemplateResponse('form.html', context={'request': request, 'result': df.agg(agg).to_html()})
        return templates.TemplateResponse('form.html', context={'request': request, 'result': df.to_html()})

    if db and col and row.isdigit():
        q = db.get(key=col)
        if q and int(row) < len(q[col]):
            df = pd.DataFrame(q)[:int(row)]
            if agg in aggs:
                return templates.TemplateResponse('form.html', context={'request': request, 'result': df.agg(agg).to_html()})
            return templates.TemplateResponse('form.html', context={'request': request, 'result': df.to_html()})

    if db and db.get(key=col):
        df = pd.DataFrame(db.get(key=col))
        return templates.TemplateResponse('form.html', context={'request': request, 'result': df.to_html()})

    return templates.TemplateResponse('form.html', context={'request': request, 'result': df})


if __name__ == '__main__':
    pass
