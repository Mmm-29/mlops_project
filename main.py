from Networksecurity.components.data_validation import DataValidation
from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.components.model_trainer import ModelTrainer
from Networksecurity.exception.exception import securityException
from Networksecurity.logging.logger import logger
from Networksecurity.entity.config_entity import (
    DataValidationConfig,
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from Networksecurity.components.data_transformation import DataTransformation
import os,sys
if __name__=='__main__':

    try:
        trainingpipelineconfig= TrainingPipelineConfig()
        dataingestionconfig= DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logger.info("Initiating data ingestion component.")
        dataingestionartifact= data_ingestion.initiate_data_ingestion()
        logger.info("Data ingestion completed successfully.")
        #print(dataingestionartifact)
        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,datavalidationconfig)
        logger.info("Initiating data validation component.")
        datavalidationartifact = data_validation.initiate_data_validation()
        logger.info("Data validation completed successfully.")
        #print(datavalidationartifact)
        datatransformationconfig=DataTransformationConfig( trainingpipelineconfig)
        
        data_transformation= DataTransformation(datavalidationartifact,datatransformationconfig)
        logger.info("Initiating data transformation component.")
        datatransformationartifact=data_transformation.initiate_data_transformation()
        #print(datatransformationartifact)
        logger.info("Data transformation completed successfully.")


        logger.info("Model training started.")
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)   
        model_trainer= ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=datatransformationartifact)
        modeltrainerartifact=model_trainer.initiate_model_trainer()
        logger.info("Model training completed successfully.")
        

    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise securityException(e, sys) from e
