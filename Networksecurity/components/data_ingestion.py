
import sys
import os
import pandas as pd
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Networksecurity.exception.exception import securityException
from Networksecurity.logging.logger import logger
from Networksecurity.entity.config_entity import DataIngestionConfig
from Networksecurity.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()
Mongo_db_URL=os.getenv("MONGODB_URL")
import pymongo


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
           
        except Exception as e:
            raise securityException(e, sys)
        

    def export_collection_as_dataframe(self):

        """Export and  Read data from MongoDB collection as a DataFrame.
        """
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            logger.info(f"Exporting collection {collection_name} from database {database_name} as DataFrame.")
            self.mongo_client = pymongo.MongoClient(Mongo_db_URL)
            collection= self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.tolist():
                logger.info("Dropping '_id' column from DataFrame.")
                df=df.drop(columns=["_id"],axis="columns")
            df.replace({"na":np.nan}, inplace=True)
            logger.info(f"DataFrame shape after export: {df.shape}")
            return df
        except Exception as e:
            raise securityException(e, sys)
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        """Export DataFrame( collected from Mongodb)to feature store directory.

        """
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
             #Creating the feature store directory
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logger.info(f"Created feature store directory at: {dir_path}")
            # Saving the DataFrame to a CSV file
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logger.info(f"Exported DataFrame to feature store at: {feature_store_file_path}")
            logger.info(f"Shape of exported DataFrame: {dataframe.shape}")
            return dataframe
        except Exception as e:
            raise securityException(e, sys)

    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        """
        Splits the DataFrame into train and test sets and saves them to the specified file paths.
           """
        try:
            logger.info("Starting train-test split operation.")
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logger.info("Performed train test split on the dataframe")
            logger.info(f"Train set shape: {train_set.shape}, Test set shape: {test_set.shape}")

            logger.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            # Creating the directory for saving the split data
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logger.info(f"Created directory for train/test data at: {dir_path}")
            # Saving train and test sets to CSV files
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path
            train_set.to_csv(train_file_path, index=False, header=True)
            logger.info(f"Train data saved to: {train_file_path}")

            test_set.to_csv(test_file_path, index=False, header=True)
            logger.info(f"Test data saved to: {test_file_path}")

            
            logger.info("Completed train-test split and data export successfully.")

            
        except Exception as e:
            raise securityException(e,sys)
        

    def initiate_data_ingestion(self):
        try:
            logger.info("Data Ingestion process started.")
            logger.info("Exporting data from MongoDB collection to DataFrame.")
            dataframe= self.export_collection_as_dataframe()
            logger.info("Data export completed. Shape: %s", dataframe.shape)
            logger.info("Saving exported data to feature store.")
            dataframe=self.export_data_into_feature_store(dataframe)
            logger.info("Data saved to feature store at: %s", self.data_ingestion_config.feature_store_file_path)
            logger.info("Splitting data into train and test sets.")
            self.split_data_as_train_test(dataframe)
            logger.info("Data split completed. Train path: %s | Test path: %s",
                    self.data_ingestion_config.training_file_path,
                    self.data_ingestion_config.testing_file_path)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path)
            logger.info("Data Ingestion process completed successfully.")
            return dataingestionartifact

        except Exception as e:
            logger.exception("Error occurred during data ingestion.")
            raise securityException(e, sys)