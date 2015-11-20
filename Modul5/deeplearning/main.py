import time
import numpy as np
import theano.tensor as T
from Modul5.basics import mnist_basics as mnist
from Modul5.deeplearning.ann import ANN


def scale(images):
    for image in range(len(images)):
        for value in range(len(images[image])):
            images[image][value] /= 255.0


def activation_map(x):
    return {
        0: T.tanh,
        1: T.nnet.sigmoid,
        2: lambda k: T.switch(k > 0, k, 0),  # Equivalent to T.nnet.relu (rectified linear unit)
        3: T.nnet.softmax,
    }.get(x, T.tanh)  # T.tanh is default if x is not found


def train_model(epochs, minibatch_size):
    for epoch in range(epochs):
        print("Training epoch number {}...".format(epoch))
        error = 0
        j = minibatch_size

        for i in range(0, len(train_set_x), minibatch_size):
            image_batch = train_set_x[i:j]
            label_batch = np.zeros((minibatch_size, 10), dtype=np.int)
            for k in range(minibatch_size):
                label_batch[k][train_set_y[i + k]] = 1
            j += minibatch_size
            error += ann.train(image_batch, label_batch)

        print("Average error per image in epoch {}: {:.3%}".format(epoch, error / j))


def test_model():
    correct = 0
    total = len(test_set_x)

    for i in range(total):
        prediction = ann.predict([test_set_x[i]])
        if prediction == test_set_y[i]:
            correct += 1

    print("Correct: {}".format(correct))
    print("Wrong: {}".format(total - correct))
    print("Total: {}".format(total))
    print("Percentage: {:.2%}".format(correct / total))

    f = open('statistics', 'a')
    f.write("Configuration:\n"
            "Hidden layers and nodes: {!r} \n"
            "Activation functions: {!r} \n"
            "Learning rate: {} \n"
            "Epochs: {} \n"
            "Minibatch size: {} \n"
            "Error percentage: {:.2%} \n"
            "Time trained: {:.2f} \n\n"
            .format(hidden, activations, lr, epochs, minibatch_size, correct / total, total_time))

    f.close()


print("Loading training set...")
train_set_x, train_set_y = mnist.gen_flat_cases(type="training")
scale(train_set_x)
print("Finished loading training set! \n")


hidden = [x for x in map(int, input("Please specify a topology description on the form 40,20,60: ").strip().split(","))]
print("\n0: hyperbolic tangent, 1: sigmoid, 2: rectified linear unit, 3: softmax")
activations = [activation_map(x) for x in list(map(int, input("Please specify activation functions for each layer on the form 0,2,1: ").strip().split(",")))]
lr = float(input("What learning rate do you want to use?: "))
print("Building model...")
ann = ANN(28*28, hidden, activations, 10, lr)
print("Finished building model!\n")


epochs = int(input("How many epochs to you want to train?: "))
minibatch_size = int(input("And what minibatch size do you want to use?: \n"))
print("Training for {} epochs with minibatch size {}...".format(epochs, minibatch_size))
start = time.time()
train_model(epochs, minibatch_size)
total_time = time.time() - start
print("Finished training! Total time used: {:.2f} seconds. \n".format(total_time))

if input("Blind test? y/n: ") == "y":
    mnist.minor_demo(ann)
else:
    print("Loading test set...")
    test_set_x, test_set_y = mnist.gen_flat_cases(type="testing")
    scale(test_set_x)
    print("Finished! Statistics:")
    test_model()