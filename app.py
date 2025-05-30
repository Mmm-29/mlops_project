import sys, os
import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print("MongoDB URL:", mongo_db_url)

import pymongo
from Networksecurity.exception.exception import securityException
from Networksecurity.logging.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
import uvicorn
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
import pandas as pd
from Networksecurity.pipeline.training_pipeline import TrainingPipeline
from Networksecurity.utils.main_utils.util import load_object
from Networksecurity.constant.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME
)
from Networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    """
    Redirects to the documentation page.
    """
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return JSONResponse(content={"message": "Training pipeline executed successfully."}, status_code=200)
    except Exception as e:
        raise securityException(e, sys) from e


@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    """
    Handles file upload and renders the prediction page.
    """
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        df.to_csv('prediction_output/output.csv', index=False)

        table_html = df.to_html(classes='table table-striped', index=False)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        logger.error(f"Error in predict_route: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
