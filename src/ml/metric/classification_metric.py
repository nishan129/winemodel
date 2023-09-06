from src.entity.artifact_entity import ClassificationMetricArtifact
from src.exception import ModelException
import sys
import pandas as pd


def f1_score(model_precision_score:float,model_recall_score:float):
    try:
        first = (2 * model_precision_score * model_recall_score)
        second = (model_precision_score + model_recall_score)
        model_f1_score = first/second
        return model_f1_score
    except Exception as e:
        raise ModelException(e,sys)


def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        confusion = pd.crosstab(y_true,y_pred)
        TP = confusion.iloc[0,0]
        FP = confusion.iloc[0,:].sum() - TP
        FN = confusion.iloc[:,0].sum() - TP
        TN = confusion.sum().sum() - TP-FP-FN
        model_precision_score = TP/(TP+FP)
        model_recall_score = TP/(TP+FN)
        model_f1_score = f1_score(model_precision_score=model_precision_score,model_recall_score=model_recall_score)
        return ClassificationMetricArtifact(f1_score=model_f1_score,
                                            precision_score=model_precision_score,
                                            recall_score=model_recall_score)
    except Exception as e:
        raise ModelException(e,sys)