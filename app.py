from fastapi import FastAPI,File,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from networksecurity.pipeline.training_pipeline import Pipeline
from networksecurity.config.configuration import Configuration
from networksecurity.exception.exception import NetworkSecurityException
from uvicorn import run as app_run
import dagshub
import pandas as pd
import sys
from networksecurity.utils import *

import certifi
ca = certifi.where()

from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/',tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train_route():
    config=Configuration()
    pipeline=Pipeline(config=config)
    pipeline.run()
    return Response(content='Training is successfull')

@app.post('/predict')
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        model=load_object(file_path=r'D:\Oracle Projects\Python\project\networksecurity\networksecurity\artifact\model_pusher\saved_models\model.pkl')
        y_pred=model.predict(df)
        df['result']=y_pred
        df.to_csv(os.path.join('prediction_output','output.csv'),index=False,header=True)
        table_html=df.to_html(open(os.path.join('prediction_output','output.html'), 'w'),classes='table table-striped')        
        return templates.TemplateResponse('table.html',{"request":request,"table":table_html})
    except Exception as e:
        raise NetworkSecurityException(e,sys)


if __name__=='__main__':
    # dagshub.init(repo_owner='ETAMILSELVAN47', repo_name='NetworkSecurity', mlflow=True)
    app_run(app,host="0.0.0.0",port=8080)
