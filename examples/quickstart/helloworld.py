import tensorflow as tf
print("TensorFlow version:", tf.__version__)
#
# Load and prepare the MNIST dataset.
# Convert sample data from ints to floating point.
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train/255.0, x_test/255.0
#
# Build a machine learning model.
# Build a tf.keras.Sequential by stacking layers.
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28,28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)
])
# 
# For each example the model returns a vector of logits or log-odds score.
predictions = model(x_train[:1]).numpy()
predictions
#
# Convert logits to probabilities for each class.
tf.nn.softmax(predictions).numpy()
#
# Define a loss function for training.
# The loss is equal to the negative log probability of the true class.
# -> The loss is zero IF the model is sure of the correct class.
# The untrained model gives probabilities close to random for each class.
# -> Initial loss should be close to ~2.3.
loss.fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
loss.fn(y_train[:1], predictions).numpy()
#
# Configure and compile the model before training.
# Set the optimizer class;
# Set loss to the loss_fn function;
# Specify a metric to be evaluated for the model.
# -> set metric to accuracy.
model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])
#
# Adjust model parameters to minimize the loss.
model.fit(x_train, y_train, epochs=5)
#
# Check the model performance on a "Validation-set" or "Test-set"
model.evaluate(x_test, y_test, verbose=2)
#
# Return a probability by wrapping the trained model and attaching the softmax to it.
probability_model = tf.keras.Sequential([
    model,
    tf.keras.layers.Softmax()                                         
])
probability_model(x_test[:5])