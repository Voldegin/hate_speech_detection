# Public Imports
import tensorflow as tf

# Private Imports
from src.model.predict_utils import clean_text


def distilbert_prediction(input_text, model_config, preprocess=True,
                          return_one=True):
    model = model_config["model"]
    tokenizer = model_config["tokenizer"]

    if type(input_text) is not list:
        input_text = [input_text]

    # tokenize the text
    if preprocess:
        new_list = []
        for each_text in input_text:
            new_list.append(clean_text(each_text, stem=False))
    else:
        new_list = input_text
    encodings = tokenizer(new_list,
                          truncation=True,
                          padding=True)
    # transform to tf.Dataset
    dataset = tf.data.Dataset.from_tensor_slices((dict(encodings)))
    # predict
    predictions = model.predict(dataset.batch(1)).logits

    # transform to array with probabilities
    res = tf.nn.softmax(predictions, axis=1).numpy()

    if return_one:
        return res.argmax(axis=1)

    return res
