from Networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Networksecurity.entity.config_entity import DataValidationConfig
from Networksecurity.exception.exception import securityException
from Networksecurity.logging.logger import logger
from Networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import os, sys
from Networksecurity.utils.main_utils.util import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            logger.info("Schema config loaded successfully.")
        except Exception as e:
            raise securityException(e, sys)

    

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Reads a CSV file and returns a DataFrame.
        """
        try:
            logger.info(f"Reading data from file: {file_path}") 
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise securityException(e, sys)
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            expected_columns = len(self._schema_config['columns'])  
            actual_columns = len(dataframe.columns)
            logger.info(f"Expected number of columns: {expected_columns}") 
            logger.info(f"Actual number of columns in dataframe: {actual_columns}") 
            return expected_columns == actual_columns
        except Exception as e:
            raise securityException(e, sys)
    
    def check_if_numeric_column_exist(self, dataframe: pd.DataFrame) -> bool:
        """
        Check if all expected numeric columns exist and have correct types.
        """
        try:
            expected_columns = self._schema_config['columns']
            for column_dict in expected_columns:
                for column_name, column_type in column_dict.items():
                    if column_type in ["int", "float", "int64", "float64"]:  
                        if column_name not in dataframe.columns:
                            logger.error(f"Missing numeric column: {column_name}")
                            return False
                        if not pd.api.types.is_numeric_dtype(dataframe[column_name]):
                            logger.error(f"Column {column_name} is not numeric")
                            return False
            return True
        except Exception as e:
            raise securityException(e, sys)
   

        


    def detect_dataset_drift(self, base_df, current_df,threshold=0.05) -> bool:
        """
        Detects dataset drift using the Kolmogorov-Smirnov test.

        """
        try:
            logger.info("Starting dataset drift detection using KS test.")

            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                drift_found = is_same_dist.pvalue < threshold
                if drift_found:
                    status=False
                    logger.warning(f"Drift detected in column: {column}")
                report[column] = {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": drift_found
                }
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            logger.info(f"Drift report written to: {drift_report_file_path}")

        except Exception as e:
            raise securityException(e,sys)



        
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logger.info("Starting data validation process...")
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            #read the data from train and test
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            #Validate Number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain all columns.\n"
                raise securityException(error_message, sys)
            
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contain all columns.\n"
                raise securityException(error_message, sys)
            
            
            #Check if numeric columns exist
            if not self.check_if_numeric_column_exist(train_dataframe):
                raise securityException("Train DataFrame missing numeric columns.", sys)
            if not self.check_if_numeric_column_exist(test_dataframe):
                raise securityException("Test DataFrame missing numeric columns.", sys)
            

              ## lets check datadrift
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True

            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            logger.info("Validated datasets saved.")

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            logger.info("Data validation completed successfully.")
            return data_validation_artifact


        except Exception as e:
            raise securityException(e, sys)