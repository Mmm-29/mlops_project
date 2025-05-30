import os
import sys
import numpy as np
import pandas as pd

TARGET_COLUMN="Result"
PIPELINE_NAME:str="MLOPS_project"
Artifact_DIR:str = "Artifact"
FILE_NAME:str = "phishingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
SCHEMA_FILE_PATH =os.path.join("data_schema","schema.yaml")
SAVED_MODEL_DIR:str = os.path.join("saved_model")
MODEL_FILE_NAME:str = "model.pkl"



"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME:str = "Network_phishingData"
DATA_INGESTION_DATABASE_NAME:str ="MMMdatabase"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str= "feature_store"
DATA_INGESTION_INGESTED_DIR:str= "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2





"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "valid"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"



"""
Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME

"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed_data"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

##knn imputer params to replace nan value
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict={
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}



"""
Model Training related constant start with MODEL_TRAINING VAR NAME
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05

TRAINING_BUCKET_NAME: str = "mlops-project-bucket-1234"
