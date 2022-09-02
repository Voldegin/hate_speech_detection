from src.model.load_model_info import load_models
from src.db.initialise_db import initialize_db

MODEL_LIST = load_models()

MODEL_PREDICTIONS = {0: "Not bullying", 1: "Bullying"}

initialize_db()
