import json
import os
import pandas as pd
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from deta import Deta
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates("templates")

deta = Deta(os.environ.get('key'))
db = deta.Base("mvpDB")


# TO DO finish loading template
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/read/{table}/{col}")
async def read(table: str, col: str):
    db = deta.Base(table)
    r = db.read(col)
    return r if r else json.dumps({'error': 'No data'})


if __name__ == '__main__':
    pass
