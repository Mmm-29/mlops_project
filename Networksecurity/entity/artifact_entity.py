from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """
    Data class for storing the artifacts produced by the data ingestion process.
    """
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    """
    Data class for storing the artifacts produced by the data validation process.
    """
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
    

@dataclass
class DataTransformationArtifact:
    """
    Data class for storing the artifacts produced by the data transformation process.
    """
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ClassificationMetricArtifact:
    """
    Data class for storing the classification metrics.
    """
    f1_score: float
    precision_score: float
    recall_score: float

    

@dataclass
class ModelTrainerArtifact:
    """
    Data class for storing the artifacts produced by the model training process.
    """
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact