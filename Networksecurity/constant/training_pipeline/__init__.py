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


DATA_INGESTION_COLLECTION_NAME:str = "Network_phishingData"
DATA_INGESTION_DATABASE_NAME:str ="MMMdatabase"
DATA_INGESTION_DIR_NAME:str = "Networksecurity/data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str= "feature_store"
DATA_INGESTION_INGESTED_DIR:str= "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2