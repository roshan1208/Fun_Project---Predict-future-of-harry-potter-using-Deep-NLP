# -*- coding: utf-8 -*-
"""NLP_harry.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iuvlwbPV-llW8iWxj8rVPSJ-OOHtcDI7
"""

import numpy as np

import pandas as pd

# Commented out IPython magic to ensure Python compatibility.
import tensorflow as tf
# %tensorflow_version 2.x

text = open('harry_potter.txt',mode='r',encoding='latin1').read()

print(text[:200])

len(text)

vocab = sorted(set(text))

len(vocab)

char_to_ind = {char:ind for ind,char in enumerate(vocab)}

char_to_ind[':']

ind_to_char = np.array(vocab)

ind_to_char[21]

encoded_text = np.array([char_to_ind[c] for c in text])

encoded_text[:200]

encoded_text.shape

print(text[200000:200500])

lines = """
Last call for Hogsmeade!

Come on, now!

Guys, let me go.

Clever, Harry.

But not clever enough.

We've got a better way.

"""

len(lines)

seq_len = 130

total_num_len = len(text)//(seq_len+1)

total_num_len

char_dataset = tf.data.Dataset.from_tensor_slices(encoded_text)

sequences = char_dataset.batch(seq_len+1, drop_remainder=True)

def create_seq_targets(seq):
  input_txt = seq[:-1]
  target_txt = seq[1:]
  return input_txt, target_txt

dataset = sequences.map(create_seq_targets)

batch_size = 128
buffer_size = 10000

dataset = dataset.shuffle(buffer_size).batch(batch_size, drop_remainder = True)

vocab_size = len(vocab)
embed_dim = 68
rnn_neurons=1026

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import Dense, Embedding, GRU

from tensorflow.keras.losses import sparse_categorical_crossentropy

def sparse_cat_loss(y_true, y_pred):
  return sparse_categorical_crossentropy(y_true, y_pred, from_logits=True)

def create_model(vocab_size, embed_dim, rnn_neurons, batch_size):
  model = Sequential()
  model.add(Embedding(vocab_size, embed_dim, batch_input_shape = [batch_size, None]))
  model.add(GRU(rnn_neurons, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'))
  model.add(Dense(vocab_size))
  model.compile(optimizer = 'adam', loss = sparse_cat_loss)
  return model

model = create_model(vocab_size=vocab_size,
                     embed_dim=embed_dim,
                     rnn_neurons=rnn_neurons,
                     batch_size=batch_size)

model.summary()

#epochs = 60
#model.fit(dataset, epochs=epochs)

#model.save('harry_potter_updated.h5')

from tensorflow.keras.models import load_model

model = create_model(vocab_size, embed_dim, rnn_neurons, batch_size=1)
model.load_weights('harry_potter_updated.h5')
model.build(tf.TensorShape([1, None]))

def generate_text(model, start_seed,gen_size=100,temp=1.0):
  '''
  model: Trained Model to Generate Text
  start_seed: Intial Seed text in string form
  gen_size: Number of characters to generate

  Basic idea behind this function is to take in some seed text, format it so
  that it is in the correct shape for our network, then loop the sequence as
  we keep adding our own predicted characters. Similar to our work in the RNN
  time series problems.
  '''

  # Number of characters to generate
  num_generate = gen_size

  # Vecotrizing starting seed text
  input_eval = [char_to_ind[s] for s in start_seed]

  # Expand to match batch format shape
  input_eval = tf.expand_dims(input_eval, 0)

  # Empty list to hold resulting generated text
  text_generated = []

  # Temperature effects randomness in our resulting text
  # The term is derived from entropy/thermodynamics.
  # The temperature is used to effect probability of next characters.
  # Higher probability == lesss surprising/ more expected
  # Lower temperature == more surprising / less expected
 
  temperature = temp

  # Here batch size == 1
  model.reset_states()

  for i in range(num_generate):

      # Generate Predictions
      predictions = model(input_eval)

      # Remove the batch shape dimension
      predictions = tf.squeeze(predictions, 0)

      # Use a cateogircal disitribution to select the next character
      predictions = predictions / temperature
      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

      # Pass the predicted charracter for the next input
      input_eval = tf.expand_dims([predicted_id], 0)

      # Transform back to character letter
      text_generated.append(ind_to_char[predicted_id])

  return (start_seed + ''.join(text_generated))

print(generate_text(model,"Harry Potter",gen_size=500))

print(generate_text(model,"Harry",gen_size=500))

print(generate_text(model," Ron Weasley",gen_size=500))

print(generate_text(model,"Ron",gen_size=500))

print(generate_text(model,"Hermione Granger",gen_size=500))

print(generate_text(model,"Hermione",gen_size=500))

print(generate_text(model,"Draco Malfoy",gen_size=500))

print(generate_text(model,"Draco",gen_size=500))

print(generate_text(model,"Albus Dumbledore",gen_size=500))

print(generate_text(model,"Dumbledore",gen_size=500))

print(generate_text(model,"lord voldemort",gen_size=500))

print(generate_text(model,"voldemort",gen_size=500))

