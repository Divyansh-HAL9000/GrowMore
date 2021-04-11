import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Activation, Dense, Conv2D, MaxPool2D, Input, Layer, Flatten


class InceptionBlock(Layer):
    def __init__(self,
                 n1x1o=0, n3x3i=0, n3x3o=0,
                 n5x5i=0, n5x5o=0, n7x7i=0, 
                 n7x7o=0, nmpo=0, **kwargs):
        nmpi = nmpo
        super(InceptionBlock, self).__init__()
        
        if n1x1o:
            self.layer_1x1 = Conv2D(n1x1o, (1, 1), padding='same', activation='relu')
        
        if n3x3i:
            self.layer_3x3i = Conv2D(n3x3i, (1, 1), padding='same', activation='relu')
            self.layer_3x3o = Conv2D(n3x3o, (3, 3), padding='same', activation='relu')

        if n5x5i:
            self.layer_5x5i = Conv2D(n5x5i, (1, 1), padding='same', activation='relu')
            self.layer_5x5o = Conv2D(n5x5o, (5, 5), padding='same', activation='relu')
        
        if n7x7i:
            self.layer_7x7i = Conv2D(n7x7i, (1, 1), padding='same', activation='relu')
            self.layer_7x7o = Conv2D(n7x7o, (7, 7), padding='same', activation='relu')
        
        if nmpi:
            self.layer_nmpi = Conv2D(nmpo, (1, 1), padding='same', activation='relu')
            self.layer_nmpo = MaxPool2D(pool_size=(2, 2), strides=(1, 1), padding='same')

        self.n1x1 = n1x1o
        self.n3x3 = (n3x3i, n3x3o)
        self.n5x5 = (n5x5i, n5x5o)
        self.n7x7 = (n7x7i, n7x7o)
        self.nmp = (nmpo, nmpo)

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'n1x1': self.n1x1,
            'n3x3': self.n3x3,
            'n5x5': self.n5x5,
            'n7x7': self.n7x7,
            'nmp': self.nmp
        })
        return config
        
    def call(self, input_tensor, training=False):
        outputs = []
        if self.n1x1:
            op_1x1 = input_tensor
            op_1x1 = self.layer_1x1(op_1x1, training=training)
            outputs.append(op_1x1)
        
        if self.n3x3[0]:
            op_3x3 = input_tensor
            op_3x3 = self.layer_3x3i(op_3x3, training=training)
            op_3x3 = self.layer_3x3o(op_3x3, training=training)
            outputs.append(op_3x3)
        
        if self.n5x5[0]:
            op_5x5 = input_tensor
            op_5x5 = self.layer_5x5i(op_5x5, training=training)
            op_5x5 = self.layer_5x5o(op_5x5, training=training)
            outputs.append(op_5x5)
        
        if self.n7x7[0]:
            op_7x7 = input_tensor
            op_7x7 = self.layer_7x7i(op_7x7, training=training)
            op_7x7 = self.layer_7x7o(op_7x7, training=training)
            outputs.append(op_7x7)
        
        if self.nmp[0]:
            op_mp = input_tensor
            op_mp = self.layer_nmpi(op_mp, training=training)
            op_mp = self.layer_nmpo(op_mp)
            outputs.append(op_mp)
        
        return tf.keras.layers.concatenate(outputs, axis=-1)
    
    def compute_output_shape(self, input_shape):
        return (input_shape[0:-1] + (self.n1x1+self.n3x3[1]+self.n5x5[1]+self.n7x7[1]+self.nmp[1]))

Inception_1 = InceptionBlock(n1x1o=32, n3x3i=32, n3x3o=64,
                            n5x5i=32, n5x5o=64, nmpo=64)
Inception_2 = InceptionBlock(n1x1o=64, n5x5i=32, n5x5o=64,
                            n7x7i=64, n7x7o=32, nmpo=32)

CNN_model = Sequential()
print('input size = (1, 299, 299, 3)')
CNN_model.add(Conv2D(32, (3, 3), activation='relu')) # 299x299 -> 297x297
CNN_model.add(MaxPool2D((2, 2))) # 297x297 -> 148x148
CNN_model.add(Conv2D(64, (5, 5), activation='relu')) # 148x148 -> 144x144
CNN_model.add(MaxPool2D(2, 2)) # 144x144 -> 72x72
CNN_model.add(Inception_1)
CNN_model.add(tf.keras.layers.Activation(tf.keras.activations.relu))
CNN_model.add(MaxPool2D(2, 2))
CNN_model.add(Inception_2)
CNN_model.add(Conv2D(36, (1, 1), padding='same', activation='relu'))
CNN_model.add(MaxPool2D(2, 2))
CNN_model.add(Conv2D(10, (1, 1), padding='same', activation='relu'))
CNN_model.add(Flatten())
CNN_model.add(tf.keras.layers.Activation(tf.keras.activations.relu))
print('Flattened the layer.. adding the dense layer')
CNN_model.add(Dense(512, activation='tanh'))
CNN_model.build(input_shape=(1, 299, 299, 3))
CNN_model.summary()