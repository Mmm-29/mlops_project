from Networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from Networksecurity.exception.exception import securityException
from Networksecurity.logging.logger import logger
import os,sys

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise securityException(e, sys) from e
    
    def predict(self, X):
        """
        Predicts the target variable using the preprocessor and model.
        
        Args:
            X: Input features for prediction.
        
        Returns:
            Predicted values.
        """
        try:
            X_transformed = self.preprocessor.transform(X)
            y_hat=self.model.predict(X_transformed)
            return y_hat 
        except Exception as e:
            raise securityException(e, sys) from e