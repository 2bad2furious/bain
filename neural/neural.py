import tensorflow as tf
import numpy as np

(train_images, train_img_labels), (test_images, test_img_labels) = tf.keras.datasets.mnist.load_data()
(train_texts, train_labels), (test_texts, test_labels) = tf.keras.datasets.imdb.load_data()

train_texts = np.array(train_texts)
train_labels = np.array(train_labels)
test_texts = np.array(test_texts)
test_labels = np.array(test_labels)


model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='sigmoid'),
    tf.keras.layers.Dense(2)
])
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
model.fit(train_texts, train_labels, epochs=10)
test_loss, test_acc = model.evaluate(test_texts,  test_labels, verbose=2)
pr_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()]) # přidání softmax vrstvy
predictions = pr_model.predict(test_texts)


# shows sample s and its class c
def show_sample(s, c):
    pass

# zobrazí predikci vzorku číslo i
def sample_predict(i, test_data, test_labels, predictions, class_names):
    s = test_data[i]
    c = class_names[test_labels[i]]
    show_sample(s, c)

    print("Probabilities")
    print("------------")
    for j in range(len(class_names)):
        print(class_names[j], ":", np.round(predictions[i, j], 2))

    ind = np.argmax(predictions[i])

    print("------------")
    print("true class:", c, ", predicted class:", class_names[ind])
