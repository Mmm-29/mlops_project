from Networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score, precision_score, recall_score
def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        """
        Calculate classification metrics such as F1 score, precision, and recall.

        Args:
            y_true (list or np.array): True labels.
            y_pred (list or np.array): Predicted labels.

        Returns:
            ClassificationMetricArtifact: An object containing the calculated metrics.
        """
        model_f1_score = f1_score(y_true, y_pred,)
        model_precision_score = precision_score(y_true, y_pred,)
        model_recall_score = recall_score(y_true, y_pred,)
        classification_metric = ClassificationMetricArtifact(
            f1_score=model_f1_score, precision_score=model_precision_score, recall_score=model_recall_score)
        

        return classification_metric
    except Exception as e:
        raise Exception(f"Error in calculating classification metrics: {str(e)}") from e
        
