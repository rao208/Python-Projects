from __future__ import print_function

import argparse
import gzip
import json
from json import encoder
import os
import pickle
import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt

def one_hot(labels):
    """this creates a one hot encoding from a flat vector:
    i.e. given y = [0,2,1]
     it creates y_one_hot = [[1,0,0], [0,0,1], [0,1,0]]
    """
    classes = np.unique(labels)
    n_classes = classes.size
    one_hot_labels = np.zeros(labels.shape + (n_classes,))
    for c in classes:
        one_hot_labels[labels == c, c] = 1
    return one_hot_labels


def mnist(datasets_dir='./data'):
    
    if not os.path.exists(datasets_dir):
        os.mkdir(datasets_dir)
    data_file = os.path.join(datasets_dir, 'mnist.pkl.gz')
    if not os.path.exists(data_file):
        print('... downloading MNIST from the web')
        try:
            import urllib
            urllib.urlretrieve('http://google.com')
        except AttributeError:
            import urllib.request as urllib
        url = 'http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz'
        urllib.urlretrieve(url, data_file)

    print('... loading data')
    
    # Load the dataset
    
    f = gzip.open(data_file, 'rb')
    try:
        train_set, valid_set, test_set = pickle.load(f, encoding="latin1")
    except TypeError:
        train_set, valid_set, test_set = pickle.load(f)
    f.close()

    test_x, test_y = test_set
    test_x = test_x.astype('float32')
    test_x = test_x.astype('float32').reshape(test_x.shape[0], 28, 28, 1)
    test_y = test_y.astype('int32')
    valid_x, valid_y = valid_set
    valid_x = valid_x.astype('float32')
    valid_x = valid_x.astype('float32').reshape(valid_x.shape[0], 28, 28, 1)
    valid_y = valid_y.astype('int32')
    train_x, train_y = train_set
    train_x = train_x.astype('float32').reshape(train_x.shape[0], 28, 28, 1)
    train_y = train_y.astype('int32')
    print('... done loading data')
    return train_x, one_hot(train_y), valid_x, one_hot(valid_y), test_x, one_hot(test_y)


def train_and_validate(x_train, y_train, x_valid, y_valid, num_epochs, lr, num_filters, batch_size, filter_size):
    

    # Place holders

    x = tf.placeholder(tf.float32, shape=([None, 28, 28, 1]), name='x')
    y_ = tf.placeholder(tf.int32, shape=([None, 10]), name='y_')

    # Convolutional Layer #1

    conv1 = tf.layers.conv2d(inputs=x, filters=num_filters, kernel_size= filter_size, padding="same", activation=tf.nn.relu)

    print("The shape of conv1", conv1.shape)

    # Pooling Layer #1

    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=2, strides=1)
    print("The shape of pool1", pool1.shape)

    # Convolutional Layer #2

    conv2 = tf.layers.conv2d(inputs=pool1, filters=num_filters, kernel_size= filter_size, padding="same", activation=tf.nn.relu)
    print("The shape of conv2", conv2.shape)

    #Pooling Layer #2

    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=2, strides=1)
    print("The shape of pool2", pool2.shape)
    print(type(pool2))

    pool_dim1 = pool2.shape[1]        
    pool_dim2 = pool2.shape[2]


    print(pool2.shape[1], pool2.shape[2])

    # Dense Layer

    #pool2_flat = tf.reshape(pool2, [-1, pool_dim1 * pool_dim2 * num_filters])

    pool2_flat = tf.reshape(pool2, [-1, 26 * 26 * num_filters])
    
    print("The shape of pool2_flat", pool2_flat.shape)

    dense = tf.layers.dense(inputs=pool2_flat, units=128, activation=tf.nn.relu)
    logits = tf.layers.dense(inputs=dense, units=10)   # y_predict
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=logits), name='cost')

    # Gradient Descent

    optimizer =  tf.train.GradientDescentOptimizer(lr).minimize(cost)
    
    # Evaluate model

    correct = tf.equal(tf.argmax(logits, 1), tf.argmax(y_, 1))

    # Accuracy calculation
    
    accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name='acc')

    model = tf.train.Saver()
    
    init = tf.global_variables_initializer()
    
    with tf.Session() as sess:
        
        sess.run(init)

        n_batches = len(x_train) // batch_size
        validation_accuracy = []
        
        for epoch in range(num_epochs):
            val_acc = 0
            acc = 0
            
            for b in range(n_batches):

                X_batch = x_train[b:b + batch_size]
                Y_batch = y_train[b:b + batch_size]
                
                opt, loss, train_accuracy = sess.run([optimizer, cost, accuracy] , feed_dict={x:X_batch, y_:Y_batch})
                acc += train_accuracy


                X_val = x_valid[b:b + batch_size]
                Y_val = y_valid[b:b + batch_size]

                val_acc += sess.run(accuracy, feed_dict={x:X_val, y_:Y_val})
                
            print('Epoch ' +str(epoch), ' Training Accuracy=', '{:.3f}'.format((acc/ n_batches)*100), ' Loss=', '{:.4f}'.format(loss))
            print("The Validation accuracy for Epoch " +str(epoch), "is" , (val_acc/ n_batches)*100)
            
            validation_accuracy.append(val_acc / n_batches)
            
        model.save(sess, 'final_model')
        print('Final Model Saved')
        print('Optimization Done :)')
             
    return validation_accuracy, model, ((acc*n_batches)*100)

def test(x_test, y_test, batch_size):
    
    n_batches = len(x_test) // batch_size
    
    with tf.Session() as sess:
        new_model = tf.train.import_meta_graph('final_model.meta')
        print('Model Restored')
        new_model.restore(sess, tf.train.latest_checkpoint('./'))
        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name('x:0')
        y_ = graph.get_tensor_by_name('y_:0')
        
        te = 0
        accur = 0
        
        for b in range(n_batches):

            X_test = x_test[b:b + batch_size]
            Y_test = y_test[b:b + batch_size]
            feed_dict = {x: X_test, y_: Y_test}

            cost = graph.get_tensor_by_name('cost:0')
            acc = graph.get_tensor_by_name('acc:0')

            test_error, accuracy = sess.run([cost, acc], feed_dict)
            te += test_error
            accur += accuracy
            
    
    return (te / n_batches), ((accur / n_batches)*100)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_path", default="./", type=str, nargs="?",
                        help="Path where the results will be stored")
    parser.add_argument("--input_path", default="./", type=str, nargs="?",
                        help="Path where the data is located. If the data is not available it will be downloaded first")
    parser.add_argument("--learning_rate", default=1e-3, type=float, nargs="?", help="Learning rate for SGD")
    parser.add_argument("--num_filters", default=16, type=int, nargs="?",
                        help="The number of filters for each convolution layer")
    parser.add_argument("--batch_size", default=128, type=int, nargs="?", help="Batch size for SGD")
    parser.add_argument("--epochs", default=12, type=int, nargs="?",
                        help="Determines how many epochs the network will be trained")
    parser.add_argument("--run_id", default=0, type=int, nargs="?",
                        help="Helps to identify different runs of an experiments")

    args = parser.parse_args()

 #hyperparameters
    
    lr = args.learning_rate
    num_filters = args.num_filters
    batch_size = args.batch_size
    epochs = args.epochs

    # train and test convolutional neural network

    x_train, y_train, x_valid, y_valid, x_test, y_test = mnist(args.input_path)


    filter_size = 1
     
    validation_accuracy, model, training_accuracy=train_and_validate(x_train , y_train, x_valid, y_valid, epochs, lr, num_filters, batch_size, filter_size)

    print("The Validation Accuracy is", validation_accuracy)

    test_error, accuracy = test(x_test, y_test, batch_size)
    print('Testing Error is=', test_error)
    print('Testing Accuracy is=', accuracy)

    
    # save results in a dictionary and write them into a .json file
    
    results = dict()
    results["lr"] = lr
    results["num_filters"] = num_filters
    results["batch_size"] = batch_size
    #results["learning_curve"] = learning_curve
    results["test_error"] = test_error.tolist()

    path = os.path.join(args.output_path, "results")
    os.makedirs(path, exist_ok=True)

    fname = os.path.join(path, "results_run_%d.json" % args.run_id)
    with open(fname, 'w') as fh:
        json.dump(results, fh)
    fh.close()
