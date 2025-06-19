import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from fastapi import FastAPI , Request, Form 
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn
import requests

from dash_app import app as app_dash

app = FastAPI()

#obtenir le chemin absolu vers le repertoire des modeles
templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"templates"))

#obtenir le chemin absolu vers le repertoire statique
static_dir  = os.path.abspath(os.path.join(os.path.dirname(__file__),"static"))

# Servir des fichiers statique
app.mount("/static", StaticFiles(directory=static_dir))

# configurer le modele Jinja2 pour le rendu des fichires HTML
templates = Jinja2Templates(directory=templates_dir)

# Montez l'application Dash sous le chemin /dashboard
app.mount("/dashboard", WSGIMiddleware(app_dash.server))

user = {"admin": "123"}
EXTERNAL_API_URL = 'http://localhost:8000/info'


#Definir les routes

def get_external_info():
    try:
        response = requests.get(EXTERNAL_API_URL)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print ("error from weather api: ", e)
        return{
            'city':'N/A',
            'time':'N/A',
            'weather': {
                'city':'N/A',
                'temperature':'N/A',
                'description': 'N/A',
            }
        }

@app.get('/')
async def home_page(request : Request):
    info = get_external_info()
    return templates.TemplateResponse("home.html",{"request":request, "info":info})


@app.get('/login')
async def login_page(request : Request):
    return templates.TemplateResponse("login.html",{"request":request})


@app.post('/login')
async def login(request:Request , username : str = Form(...),password : str = Form(...)):
        if username in user and user[username]  == password:
            response = RedirectResponse(url = '/dashboard' , status_code=302)
            return response
        return templates.TemplateResponse("login.html" , {"request": request , "error":"Inavalid username and password"})
            