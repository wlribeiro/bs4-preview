import json
import os
from unittest import result
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



app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> Request:
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

@app.post("/run")
async def run_css_selector(data: Item):
    soup = BeautifulSoup(data.html, "html.parser")
    result = soup.select_one(data.css_selector)
    return {"response": str(result)}

def coisa_complexa():
    os.system("sleep 10")
    return 1