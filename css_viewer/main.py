import json
import os
from unittest import result
from urllib import response
from bs4 import BeautifulSoup


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    html: str
    css_selector: str
    multi_selector: bool


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> Request:
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


@app.post("/run")
async def run_css_selector(data: Item):
    result = extract(data.html, data.css_selector, data.multi_selector)
    return {"response": str(result)}


def extract(html: str, selector: str, multi_selector: bool = False):
    soup = BeautifulSoup(html, "html.parser")
    result = soup.select(selector)
    if result:
        return result if multi_selector else result[0]
    
    return None
