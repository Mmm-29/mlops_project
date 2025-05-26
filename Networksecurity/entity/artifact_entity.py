from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """
    Data class for storing the artifacts produced by the data ingestion process.
    """
    trained_file_path: str
    test_file_path: str
    