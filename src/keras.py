import encoded_utils

import tensorflow as tf
from tensorflow.keras import applications
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import metrics
from tensorflow.keras import Model
from tensorflow.keras import optimizers
from tensorflow.keras.applications import resnet


encoded_genotype_file = '/home/sdp/genotype-encoding/data/genotype.txt'
encoded_positive_file = '/home/sdp/genotype-encoding/data/positive.txt'
encoded_negative_file = '/home/sdp/genotype-encoding/data/negative.txt'

def main():
    # loading vectors (anchor, positive, and negative)
    genotype_vectors = encoded_utils.read_encoded_file(encoded_genotype_file)
    positive_vectors = encoded_utils.read_encoded_file(encoded_positive_file)
    negative_vectors = encoded_utils.read_encoded_file(encoded_negative_file)

    # counting variants and samples for dimesions of dataset
    # ValueError: Input size must be at least 32x32
    num_variants = encoded_utils.count_variants(encoded_genotype_file)
    print(type(num_variants), num_variants)
    num_samples = len(genotype_vectors)
    print(type(num_samples), num_samples)
    target_shape = (num_variants, 32) 
    print(type(target_shape), target_shape)
    
    # making dataset objects from lists
    genotype_dataset = tf.data.Dataset.from_tensor_slices(genotype_vectors)
    print("genotype dataset", genotype_dataset)
    positive_dataset = tf.data.Dataset.from_tensor_slices(positive_vectors)
    negative_dataset = tf.data.Dataset.from_tensor_slices(positive_vectors)


    #DEBUG
    #print('Genotype vectors\n')
    #for i in genotype_dataset: print(i)
    #for i in positive_dataset: print(i)
    #for i in negative_dataset: print(i)

    dataset = tf.data.Dataset.zip((genotype_dataset, positive_dataset, negative_dataset))
    #dataset = dataset.shuffle(buffer_size=1024)
    #dataset = dataset.map(preprocess_triplets)
    print("dataset", dataset)

    # split dataseet into train and validation
    train_dataset = dataset.take(round(num_samples * 0.8))
    val_dataset = dataset.skip(round(num_samples * 0.8))

    train_dataset = train_dataset.batch(32, drop_remainder=False)
    train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)

    val_dataset = val_dataset.batch(32, drop_remainder=False)
    val_dataset = val_dataset.prefetch(tf.data.AUTOTUNE)

    # generate layers and embedding
    base_cnn = resnet.ResNet50(
        weights='imagenet', input_shape=target_shape + (3,), include_top=False
    )
    
    flatten = layers.Flatten()(base_cnn.output)
    dense1 = layers.Dense(512, activation='relu')(flatten)
    dense1 = layers.BatchNormalization()(dense1) 
    dense2 = layers.Dense(256, activation='relu')(dense1)
    dense2 = layers.BatchNormalization()(dense2)
    output = layers.Dense(256)(dense2)

    embedding = Model(base_cnn.input, output, name="Embedding")


    trainable = False
    for layer in base_cnn.layers:
        layer.trainable = trainable
        

    # setting up Siamese Network Model
    class DistanceLayer(layers.Layer):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def call(self, genotype, positive, negative):
            gp_distance = tf.reduce_sum(tf.square(genotype - positive), -1)
            gn_distance = tf.reduce_sum(tf.square(genotype - negative), -1)
            return (gp_distance, gn_distance)

    print(target_shape)
    genotype_input = layers.Input(name='genotype', shape=target_shape + (3,))
    print("genotype input", genotype_input)
    positive_input = layers.Input(name='positive', shape=target_shape + (3,))
    negative_input = layers.Input(name='negative', shape=target_shape + (3,))

    distances = DistanceLayer()(
        embedding(resnet.preprocess_input(genotype_input)),
        embedding(resnet.preprocess_input(positive_input)),
        embedding(resnet.preprocess_input(negative_input)),
    )
    siamese_network = Model(
        inputs=[genotype_input, positive_input, negative_input], outputs=distances
    )

    # implement model with custom training loop
    class SiameseModel(Model):
        def __init__(self, siamese_network, margin=0.5):
            super(SiameseModel, self).__init__()
            self.siamese_network = siamese_network
            self.margin = margin
            self.loss_tracker = metrics.Mean(name="loss")
        
        def call(self, inputs):
            return self.siamese_network(inputs)

        def train_step(self, data):
            with tf.GradientTape() as tape:
                loss = self._compute_loss(data)
            
            gradients = tape.gradient(loss, self.siamese_network.trainable_weights)
            
            self.optimizer.apply_gradients(
                zip(gradients, self.siamese_network.trainable_weights)
            )
        

            self.loss_tracker.update_state(loss)
            return {"loss": self.loss_tracker.result()}



        def test_step(self, data):
            loss = self._compute_loss(data)

            self.loss_tracker.update_state(loss)
            return {"loss": self.loss_tracker.result()}


        def _compute_loss(self, data):
            ap_distance, an_distance = self.siamese_network(data)

            loss = ap_distance - an_distance
            loss = tf.maximum(loss + self.margin, 0.0)
            return loss

        @property
        def metrics(self):
            return[self.loss_tracker]

    # train model
    siamese_model = SiameseModel(siamese_network)
    siamese_model.compile(optimizer=optimizers.Adam(0.0001))
    siamese_model.fit(train_dataset, epochs=10, validation_data=val_dataset)
   
def preprocess_image(filename):
    """
    Load the specified file as a JPEG image, preprocess it and
    resize it to the target shape.
    """

    image_string = tf.io.read_file(filename)
    image = tf.image.decode_jpeg(image_string, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, target_shape)
    return image


def preprocess_triplets(anchor, positive, negative):
    """
    Given the filenames corresponding to the three images, load and
    preprocess them.
    """

    return (
        preprocess_image(anchor),
        preprocess_image(positive),
        preprocess_image(negative),
    )


if __name__ == '__main__':
    main()
