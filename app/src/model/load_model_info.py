# Public Imports
import os
import pickle
from transformers import AutoTokenizer, TFRobertaForSequenceClassification, \
    TFDistilBertForSequenceClassification

# Private Imports
from src.model.xgb_prediction import xgb_prediction
from src.model.roberta_prediction import roberta_prediction
from src.model.distilbert_prediction import distilbert_prediction

model_path = os.path.join(os.path.dirname(os.getcwd()), "models")


def load_xgb_model():
    xgb_path = os.path.join(model_path, "uniform_best_xgb.pkl")
    xgb_model = pickle.load(open(xgb_path, "rb"))

    clf_tfidf_path = os.path.join(model_path, "clf_tfidf_xgb.pkl")
    clf, tfidf = pickle.load(open(clf_tfidf_path, "rb"))

    return {"name": "XGBoost",
            "config": {"model": xgb_model, "clf": clf, "tfidf": tfidf},
            "function": xgb_prediction}


def load_roberta_model():
    roberta_path = os.path.join(model_path, "uniform-roberta")
    roberta_model = TFRobertaForSequenceClassification.from_pretrained(
        roberta_path)
    roberta_tokenizer = AutoTokenizer.from_pretrained("roberta-base")

    return {"name": "Roberta", "config": {"model": roberta_model,
                                          "tokenizer": roberta_tokenizer},
            "function": roberta_prediction}


def load_distilbert_model():
    distilbert_path = os.path.join(model_path, "uniform-distilbert")
    distilbert_model = TFDistilBertForSequenceClassification.from_pretrained(
        distilbert_path)
    distilbert_tokenizer = AutoTokenizer.from_pretrained(
        "distilbert-base-uncased")

    return {"name": "Distilbert", "config": {"model": distilbert_model,
                                             "tokenizer": distilbert_tokenizer},
            "function": distilbert_prediction}


def load_models():
    model_list = [load_roberta_model(), load_xgb_model(),
                  load_distilbert_model()]
    return model_list
