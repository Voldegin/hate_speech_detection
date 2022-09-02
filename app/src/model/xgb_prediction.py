# Public Imports
import pandas as pd

# Private Imports
from src.utils.predict_utils import clean_text


def xgb_prediction(input_text, model_config, preprocess=True):
    model = model_config["model"]
    clf = model_config["clf"]
    tfidf = model_config["tfidf"]

    df = pd.Series(input_text)
    if preprocess:
        df = df.apply(clean_text)
    test_cv = clf.transform(df)
    test_tf = tfidf.transform(test_cv)
    predictions = model.predict(test_tf)
    return predictions
