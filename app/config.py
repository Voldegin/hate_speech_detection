from src.model.load_model_info import load_models
from src.db.initialise_db import initialize_db

# Load Models for processing
MODEL_LIST = load_models()

MODEL_PREDICTIONS = {0: "Not bullying", 1: "Bullying"}

# Initialise Database
DB_ENGINE = initialize_db()

# Start live scraping based on database entries
from src.twitter.live_scraping import initialise_live_scraping
initialise_live_scraping()
