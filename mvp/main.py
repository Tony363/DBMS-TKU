import os
import sqlite3
import pandas as pd
import numpy as np

from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from deta import Deta
from dotenv import load_dotenv

from enum import Enum
from collections import ChainMap
from pydantic import BaseModel
from typing import Optional

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/dist", StaticFiles(directory="dist"), name="dist")

templates = Jinja2Templates("templates")

deta = Deta(os.environ.get('key'))


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


class dropdownChoices(str, Enum):
    att_tb = 'att_tb'
    deal_tb = 'deal_tb'


class aggregations(str, Enum):
    default = 'None'
    sort = 'sort_values'
    # mean = 'mean'
    # median = 'median'
    # max = 'max'
    # min = 'min'
    # sum = 'sum'
    # count = 'count'
    # std = 'std'
    # var = 'var'


@app.get('/form')
async def upload(request: Request):
    return templates.TemplateResponse(
        'form.html', context={
            'request': request,
            'choices': tuple(e.value for e in dropdownChoices),
            'aggs': tuple(e.value for e in aggregations),
            'frame': None,
            'columns': None,
            'rows': None})


@app.post("/form")
async def handle_form(request: Request,
                      dropdown_choices: dropdownChoices = Form(None),
                      columns: str = Form(None),
                      rows: str = Form(None),
                      aggs: str = Form(None),):
    print(f"col row {columns} {rows}")
    print(f"AGG {aggs}")
    conn = sqlite3.connect('mvp.db')
    info = pd.read_sql("Pragma table_info(%s)" % dropdown_choices.value, conn)
    df = pd.read_sql("select * from %s" %
                     dropdown_choices.value, conn)
    conn.close()

    if columns != 'None' and rows != 'None':
        if aggs == 'sort_values':
            df = df.agg(aggs, by=columns)
            return templates.TemplateResponse("form.html", context={
                'request': request,
                'choices': dropdown_choices.value,
                'aggs': tuple(e.value for e in aggregations),
                'frame': df.to_html(),
                'columns': df.columns.to_list(),
                'rows': df.index.to_list()})
        return templates.TemplateResponse('form.html', context={
            'request': request,
            'choices': dropdown_choices.value,
            'aggs': tuple(e.value for e in aggregations),
            'frame': df[columns].head(int(rows)).to_frame().to_html(),
            'columns': df.columns.to_list(),
            'rows': df.index.to_list()})
    return templates.TemplateResponse('form.html', context={'request': request,
                                                            'choices': dropdown_choices.value,
                                                            'aggs': tuple(e.value for e in aggregations),
                                                            'info': info.to_html(),
                                                            'columns': df.columns.to_list(),
                                                            'rows': df.index.to_list()})


if __name__ == '__main__':
    """
    # set header no cache to inidicate dynamic  hidden page, don't load from cache, completely different html file
    #  fuzzy matching,
    """
    pass
