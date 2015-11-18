__author__ = 'keithd'
import theano
import numpy as np
import theano.tensor.nnet as Tann
import theano.tensor as T
from Modul5.basics.mnist_basics import *
import random




class autoencoder():

    def __init__(self, nb=784,nh=15,lr=.1):

        self.cases = load_all_flat_cases()
        self.images, self.labels = self.cases
        self.lrate = lr
        self.build_ann(nb,nh,lr)
        self.images = self.preprocess(self.images)

    def preprocess(self,images):
        images = images
        for i in range(len(images)):
            for j in range(len(images[i])):
                images[i][j] /= 255
        return images

    def build_ann(self,nb,nh,lr):
        w1 = theano.shared(np.random.uniform(-.1,.1,size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(-.1,.1,size=(nh,10)))
        input = T.dvector('input')
        label = T.dscalar('label')

        x1 = Tann.sigmoid(T.dot(input,w1))
        x2 = Tann.sigmoid(T.dot(x1,w2))
        error = T.sum((label - np.argmax(x2,0))**2)
        params = [w1, w2]
        gradients = T.grad(error,params)
        backprop_acts = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]
        self.predictor = theano.function([input], outputs=[x2])
        self.trainer = theano.function([input,label], error, updates=backprop_acts)

    def do_training(self,epochs=100):
        errors = []
        for i in range(epochs):
            error = 0
            num = random.randint(0, 59750)
            for c in range(num,num+250):
                error += self.trainer(self.images[c], self.labels[c])
            errors.append(error)

        return errors


    def do_testing(self,scatter=True):
        hidden_activations = []
        for c in self.cases:
            end = self.predictor(c)
            hidden_activations.append(end)
        return hidden_activations



def autotest(nb=784, nh=15,lr=.1, epochs=1000):
    ac = autoencoder(nb,nh,lr)
    ac.do_training(epochs)
    return ac.do_testing()


ac = autoencoder()
ac.do_training(10000)

print(ac.predictor(ac.images[3]),"\n",ac.labels[3])