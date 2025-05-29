import os,sys
from Networksecurity.exception.exception import securityException
from Networksecurity.logging.logger import logger
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from Networksecurity.constant.training_pipeline import TARGET_COLUMN
from Networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from Networksecurity.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact,DataValidationArtifact
from Networksecurity.entity.config_entity import DataTransformationConfig
from Networksecurity.utils.main_utils.util import save_numpy_array_data, save_object, read_yaml_file, write_yaml_file


class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact,data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise securityException(e, sys) from e
        
    @staticmethod 
    def read_data(file_path) -> pd.DataFrame:
        """
        Reads a CSV file and returns a DataFrame.
        """
        try:
            logger.info(f"Reading data from file: {file_path}") 
            df = pd.read_csv(file_path)
            logger.info(f"Data read successfully with shape: {df.shape}") 
            return df
        except Exception as e:
            raise securityException(e, sys) from e 
        
    
    def get_data_transformer_object(cls) -> Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """

        logger.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logger.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            processor: Pipeline = Pipeline(steps=[("imputer", imputer)])
            logger.info("Created preprocessing pipeline with KNNImputer")
            return processor
        except Exception as e:
            raise securityException(e, sys) from e
        


        """
        Here i perform only one transformation that is imputation of missing values using KNNImputer.
        You can add more transformations as per your requirement.
        1. 
          Let's say  u want to add RobustScaler to scale the data,then
        try:
        imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
        scaler = RobustScaler()
        processor = Pipeline(steps=[
            ("imputer", imputer),
            ("scaler", scaler)
        ])

        2.
          If you want to add OneHotEncoder to encode categorical variables, then
        try:
        logging.info("Entered get_data_transformer_object method of DataTransformation class")

        # Numeric pipeline: impute missing values and scale
        numeric_pipeline = Pipeline(steps=[
            ("imputer", KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)),
            ("scaler", RobustScaler())
        ])

        # Categorical pipeline: one-hot encode categorical variables
        categorical_pipeline = Pipeline(steps=[
            ("onehot", OneHotEncoder(drop='first', sparse=False))
        ])

        # Combine numeric and categorical pipelines with ColumnTransformer
        preprocessor = ColumnTransformer(transformers=[
            ("num", numeric_pipeline, numeric_cols),
            ("cat", categorical_pipeline, categorical_cols)
        ])

        # Wrap the ColumnTransformer in a Pipeline and return
        full_pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor)
        ])

        """





                                                   
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logger.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logger.info("Starting data transformation....")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            logger.info(f"Train DataFrame shape: {train_df.shape}") 
            logger.info(f"Test DataFrame shape: {test_df.shape}")  


            ## training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis="columns")
            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1, 0)

              #testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1, 0)

            logger.info("Fitting and transforming the training data...")
            preprocessor= self.get_data_transformer_object()
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            logger.info("Transforming the testing data...")  
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            logger.info("Combining input and target features and converting the data into NumPy arrays...")

            train_arr=np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
            


             #save numpy array data
            logger.info("Saving transformed arrays and preprocessor object...")
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object,)
            logger.info(f"Transformed train data saved to '{self.data_transformation_config.transformed_train_file_path}' in the form of a NumPy array.")  # ✅ UPDATED
            logger.info(f"Transformed test data saved to '{self.data_transformation_config.transformed_test_file_path}' in the form of a NumPy array.")    # ✅ UPDATED
            logger.info(f"Preprocessor object (including KNNImputer) saved to '{self.data_transformation_config.transformed_object_file_path}'.")          # ✅ UPDATED



            #preparing artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact



        except Exception as e:  
            raise securityException(e, sys) from e
