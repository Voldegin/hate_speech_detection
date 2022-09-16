# Public Imports
import pandas as pd
import tensorflow_datasets as tfds
import tensorflow as tf

# Private Imports
from src.utils.predict_utils import clean_text

max_length = 128
batch_size = 64


def convert_example_to_feature(text, tokenizer):
    return tokenizer.encode_plus(text, add_special_tokens=True,
                                 max_length=max_length,
                                 pad_to_max_length=True,
                                 return_attention_mask=True,
                                 )


def map_example_to_dict(input_ids, attention_masks, label):
    return {
               "input_ids": input_ids,
               "attention_mask": attention_masks,
           }, label


def encode_examples(ds, tokenizer, limit=-1):
    input_ids_list = []
    attention_mask_list = []
    label_list = []
    
    if limit > 0:
        ds = ds.take(limit)
    for text, label in tfds.as_numpy(ds):
        bert_input = convert_example_to_feature(text.decode(), tokenizer)
        input_ids_list.append(bert_input['input_ids'])
        attention_mask_list.append(bert_input['attention_mask'])
        label_list.append([label])
    return tf.data.Dataset.from_tensor_slices((input_ids_list,
                                               attention_mask_list,
                                               label_list)).map(
        map_example_to_dict)


def roberta_prediction(input_text, model_config, preprocess=True,
                       return_one=True):
    model = model_config["model"]
    tokenizer = model_config["tokenizer"]

    if type(input_text) is not list:
        input_text = [input_text]

    if preprocess:
        new_list = []
        for each_text in input_text:
            new_list.append(clean_text(each_text, stem=False))
    else:
        new_list = input_text

    df = pd.DataFrame(new_list, columns=['text'])
    df['label'] = 0
    sentences_modified = tf.data.Dataset.from_tensor_slices(
        (df['text'], df['label']))
    ds_encoded = encode_examples(sentences_modified, tokenizer).batch(
        batch_size)

    predictions = model.predict(ds_encoded).logits

    res = tf.nn.softmax(predictions, axis=1).numpy()

    if return_one:
        return res.argmax(axis=1)

    return res
