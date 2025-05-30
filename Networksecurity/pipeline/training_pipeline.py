import os,sys
from Networksecurity.exception.exception import securityException
from Networksecurity.logging.logger import logger
from Networksecurity.components.data_transformation import DataTransformation
from Networksecurity.components.model_trainer import ModelTrainer
from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.components.data_validation import DataValidation   
from Networksecurity.entity.config_entity import (
    TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig)

from Networksecurity.entity.artifact_entity import (
    DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
)   
from Networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME
from Networksecurity.cloud.s3_syncer import s3sync


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()
        self.s3_sync=s3sync()
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            
            self.data_ingestion_config= DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Starting data ingestion process")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            logger.info("Data ingestion process initialized")
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logger.info("Data ingestion process completed successfully and artifact: {}".format(data_ingestion_artifact))
            return data_ingestion_artifact
        except Exception as e:
            logger.error("Error occurred during data ingestion")
            raise securityException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Starting data validation process")
            data_validation = DataValidation(data_ingestion_artifact, self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logger.info("Data validation completed successfully.")
            return data_validation_artifact
        except Exception as e:
            logger.error("Error occurred during data validation")
            raise securityException(e, sys) from e

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Starting data transformation process")
            data_transformation = DataTransformation(data_validation_artifact, self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logger.info("Data transformation completed successfully.")
            return data_transformation_artifact
        except Exception as e:
            logger.error("Error occurred during data transformation")
            raise securityException(e, sys) from e

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Starting model training process")
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config, data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logger.info("Model training completed successfully.")
            return model_trainer_artifact
        except Exception as e:
            logger.error("Error occurred during model training")
            raise securityException(e, sys) from e
        
    
    # local artifact directory to s3 bucket
    def sync_artifact_dir_to_s3(self):
        try:

            logger.info("Syncing artifact directory to S3")
            aws_bucket_url="s3://{}/artifact/{}".format(TRAINING_BUCKET_NAME, self.training_pipeline_config.timestamp)
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            logger.error("Error occurred while syncing artifact directory to S3")       
            raise securityException(e, sys) from e
            
          
        
        

    #local final saved model directory to s3 bucket
    def sync_saved_model_dir_to_s3(self):
        try:
            logger.info("Syncing final_model directory to S3")
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)

        except Exception as e:
            logger.error("Error occurred while syncing saved model directory to S3")
            raise securityException(e, sys) from e

        
    def run_pipeline(self):
        try:
            ingestion_artifact = self.start_data_ingestion()
            validation_artifact = self.start_data_validation(ingestion_artifact)
            transformation_artifact = self.start_data_transformation(validation_artifact)
            model_trainer_artifact = self.start_model_trainer(transformation_artifact)

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return model_trainer_artifact
        except Exception as e:
            logger.error("Pipeline execution failed")
            raise securityException(e, sys) from e

