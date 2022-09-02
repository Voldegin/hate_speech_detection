# Public Imports
import pandas as pd


def format_predictions(input_data, predictions):
    result_df = pd.DataFrame(input_data)
    result_df.rename(columns={'tweet': 'text'}, inplace=True)
    result_df['prediction'] = predictions
    return result_df
