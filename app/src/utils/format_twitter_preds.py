import pandas as pd


def format_predictions(input_data, predictions):
    result_df = pd.DataFrame(input_data)
    result_df['prediction'] = predictions
    return result_df.to_dict('records')
