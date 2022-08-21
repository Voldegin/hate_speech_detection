# Public Imports
import os
import pickle
from transformers import AutoTokenizer, TFRobertaForSequenceClassification

model_path = os.path.join(os.path.dirname(os.getcwd()), "models")


def load_xgb_model():
    xgb_path = os.path.join(model_path, "uniform_best_xgb.pkl")
    xgb_model = pickle.load(open(xgb_path, "rb"))
    return {"name": "XGB", "model": xgb_model}


def load_roberta_model():
    roberta_path = os.path.join(model_path, "uniform-roberta")
    roberta_model = TFRobertaForSequenceClassification.from_pretrained(
        roberta_path)
    roberta_tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    return {"name": "Roberta", "model": roberta_model,
            "tokenizer": roberta_tokenizer}


def load_models():
    model_list = [load_roberta_model(), load_xgb_model()]
    return model_list
