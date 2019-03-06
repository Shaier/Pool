def cov_forward(X,W,b, stride=1,padding=1):
    pass
'''X: DxCxHxW dimension, input filter W: NFxCxHFxHW, and bias b: Fx1'''
'''
D is the number of inputs --> number of images

C is the number of image channel --> 3 RGB or 1 Grey
H is the height of image --> *
W is the width of the image --> *

***** F is the number of frames????

NF is the number of filter in the filter map W
HF is the height of the filter, and finally
HW is the width of the filter.
'''
'''Let’s say we have a single image of 1x1x10x10 size and a single filter of 1x1x3x3. We also use stride of 1 and padding of 1.
Then, naively, if we’re going to do convolution operation for our filter on the image, we will loop over the image, and take the dot
 product at each 3x3 location, because our filter size is 3x3. The result is a single 1x1x10x10 image.
-->SO THE SAME HxW. Which is what I need, just with another dimension for the frames
we will have 100 possible locations to do dot product
At every one of those 100 possible location, there exists the 3x3 patch, stretched to 9x1 column vector that we can do our 3x3 convolution on.
So, with im2col, our image dimension now is: 9x100
Basically, create a similar vector of len 9 to multiply each of the 100 locations (which is one filter)
 '''


 '''wh as weight matrix to the hidden layer
bh as bias matrix to the hidden layer
wout as weight matrix to the output layer
bout as bias matrix to the output layer'''

import numpy as np
#Input array
X=np.array([[1,0,1,0],[1,0,1,1],[0,1,0,1]])

#Output
y=np.array([[1],[1],[0]])

#Sigmoid Function
def sigmoid (x):
    return 1/(1 + np.exp(-x))

#Derivative of Sigmoid Function
def derivatives_sigmoid(x):
    return x * (1 - x)

#Variable initialization
epoch=5000 #Setting training iterations
lr=0.1 #Setting learning rate
inputlayer_neurons = X.shape[1] #number of features in data set
hiddenlayer_neurons = 3 #number of hidden layers neurons
output_neurons = 1 #number of neurons at output layer

#weight and bias initialization
wh=np.random.uniform(size=(inputlayer_neurons,hiddenlayer_neurons))
bh=np.random.uniform(size=(1,hiddenlayer_neurons))
wout=np.random.uniform(size=(hiddenlayer_neurons,output_neurons))
bout=np.random.uniform(size=(1,output_neurons))

for i in range(epoch):

    #Forward Propogation
    hidden_layer_input=np.dot(X,wh) +bh
    #hidden_layer_input=hidden_layer_input1 + bh
    hiddenlayer_activations = sigmoid(hidden_layer_input)
    output_layer_input=np.dot(hiddenlayer_activations,wout) +bout
    #output_layer_input= output_layer_input1+ bout
    output = sigmoid(output_layer_input)

    #Backpropagation
    E = y-output
    slope_output_layer = derivatives_sigmoid(output)
    slope_hidden_layer = derivatives_sigmoid(hiddenlayer_activations)
    d_output = E * slope_output_layer
    Error_at_hidden_layer = d_output.dot(wout.T)
    d_hiddenlayer = Error_at_hidden_layer * slope_hidden_layer
    wout += hiddenlayer_activations.T.dot(d_output) *lr
    bout += np.sum(d_output, axis=0,keepdims=True) *lr
    wh += X.T.dot(d_hiddenlayer) *lr
    bh += np.sum(d_hiddenlayer, axis=0,keepdims=True) *lr

    print (output)



#####################################################

# here we get rid of that added dimension and plot the image
def visualize_cat(model, cat):
    # Keras expects batches of images, so we have to add a dimension to trick it into being nice
    cat_batch = np.expand_dims(cat,axis=0)
    conv_cat = model.predict(cat_batch)
    conv_cat = np.squeeze(conv_cat, axis=0)
    plt.imshow(conv_cat)

# Note: matplot lib is pretty inconsistent with how it plots these weird cat arrays.
# Try running them a couple of times if the output doesn't quite match the blog post results.
def nice_cat_printer(model, cat):
    '''prints the cat as a 2d array'''
    cat_batch = np.expand_dims(cat,axis=0)
    conv_cat2 = model.predict(cat_batch)

    conv_cat2 = np.squeeze(conv_cat2, axis=0)
    conv_cat2 = conv_cat2.reshape(conv_cat2.shape[:2])

    plt.imshow(conv_cat2)


####################################################################################################################################
####################################################################################################################################
def convolution(image, filt, bias, s=1):
    '''
    Confolves `filt` over `image` using stride `s`
    '''
    (n_f, n_c_f, f, _) = filt.shape # filter dimensions
    n_c, in_dim, _ = image.shape # image dimensions

    out_dim = int((in_dim - f)/s)+1 # calculate output dimensions

    # ensure that the filter dimensions match the dimensions of the input image
    assert n_c == n_c_f, "Dimensions of filter must match dimensions of input image"

    out = np.zeros((n_f,out_dim,out_dim)) # create the matrix to hold the values of the convolution operation

    # convolve each filter over the image
    for curr_f in range(n_f):
        curr_y = out_y = 0
        # move filter vertically across the image
        while curr_y + f <= in_dim:
            curr_x = out_x = 0
            # move filter horizontally across the image
            while curr_x + f <= in_dim:
                # perform the convolution operation and add the bias
                out[curr_f, out_y, out_x] = np.sum(filt[curr_f] * image[:,curr_y:curr_y+f, curr_x:curr_x+f]) + bias[curr_f]
                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1

    return out
'''
The convolution function makes use of a for-loop to convolve all the filters over the image. Within each iteration of the for-loop,
two while-loops are used to pass the filter over the image. At each step, the filter is multipled element-wise(*) with a section of the input image.
The result of this element-wise multiplication is then summed to obtain a single value using NumPy’s sum method, and then added with a bias term.
The filt input is initialized using a standard normal distribution and bias is initialized to be a vector of zeros.
After one or two convolutional layers, it is common to reduce the size of the representation produced by the convolutional layer. This reduction in the representation’s size is known as downsampling.
'''
def maxpool(image, f=2, s=2):
    ```
    Downsample input `image` using a kernel size of `f` and a stride of `s`
    ```
    n_c, h_prev, w_prev = image.shape

    # calculate output dimensions after the maxpooling operation.
    h = int((h_prev - f)/s)+1
    w = int((w_prev - f)/s)+1

    # create a matrix to hold the values of the maxpooling operation.
    downsampled = np.zeros((n_c, h, w))

    # slide the window over every part of the image using stride s. Take the maximum value at each step.
    for i in range(n_c):
        curr_y = out_y = 0
        # slide the max pooling window vertically across the image
        while curr_y + f <= h_prev:
            curr_x = out_x = 0
            # slide the max pooling window horizontally across the image
            while curr_x + f <= w_prev:
                # choose the maximum value within the window at each step and store it to the output matrix
                downsampled[i, out_y, out_x] = np.max(image[i, curr_y:curr_y+f, curr_x:curr_x+f])
                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1
    return downsampled
'''
The max pooling operation boils down to a for loop and a couple of while loops. The for-loop is used pass through each layer of the input image, and
the while-loops slide the window over every part of the image. At each step, we use NumPy’s max method to obtain the maximum value:
After multiple convolutional layers and downsampling operations, the 3D image representation is converted into a feature vector that is passed into a
Multi-Layer Perceptron, which merely is a neural network with at least three layers. This is referred to as a Fully-Connected Layer.
'''

################################
'''HERE I NEED TO CONNECT ALL OF THE IMAGES INTO ONE VECTOR '''
#############################

'''Fully connected'''
(nf2, dim2, _) = pooled.shape
fc = pooled.reshape((nf2 * dim2 * dim2, 1)) # flatten pooled layer

'''In this code snippet, we gather the dimensions of the previous layer (number of channels and height/width) then use them to flatten the previous
layer into a fully connected layer. This fully connected layer is proceeded by multiple dense layers of neurons that eventually produce raw predictions:
'''
z = w3.dot(fc) + b3 # first dense layer
z[z<=0] = 0 # pass through ReLU non-linearity
out = w4.dot(z) + b4 # second dense layer

'''Output Layer'''
def softmax(raw_preds):
    '''
    pass raw predictions through softmax activation function
    '''
    out = np.exp(raw_preds) # exponentiate vector of raw predictions
    return out/np.sum(out) # divide the exponentiated vector by its sum. All values in the output sum to 1.

'''Calculating the Loss'''
def categoricalCrossEntropy(probs, label):
    '''
    calculate the categorical cross-entropy loss of the predictions
    '''
    return -np.sum(label * np.log(probs)) # Multiply the desired output label by the log of the prediction, then sum all values in the vector

'''This about wraps up the operations that compose a convolutional neural network. Let us join these operations to construct the CNN.'''


'''example'''
'''Step 1: Getting the Data'''

'''The MNIST handwritten digit training and test data can be obtained here. The files store image and label data as tensors, so the files must be read
 through their bytestream. We define two helper methods to perform the extraction:'''



def extract_data(filename, num_images, IMAGE_WIDTH):
    '''
    Extract images by reading the file bytestream. Reshape the read values into a 3D matrix of dimensions [m, h, w], where m
    is the number of training examples.
    '''
    print('Extracting', filename)
    with gzip.open(filename) as bytestream:
        bytestream.read(16)
        buf = bytestream.read(IMAGE_WIDTH * IMAGE_WIDTH * num_images)
        data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
        data = data.reshape(num_images, IMAGE_WIDTH*IMAGE_WIDTH)
        return data

def extract_labels(filename, num_images):
    '''
    Extract label into vector of integer values of dimensions [m, 1], where m is the number of images.
    '''
    print('Extracting', filename)
    with gzip.open(filename) as bytestream:
        bytestream.read(8)
        buf = bytestream.read(1 * num_images)
        labels = np.frombuffer(buf, dtype=np.uint8).astype(np.int64)
    return labels

'''Step 2: Initialize parameters'''
'''We first define methods to initialize both the filters for the convolutional layers and the weights for the dense layers.
To make for a smoother training process, we initialize each filter with a mean of 0 and a standard deviation of 1.
'''

def initializeFilter(size, scale = 1.0):
    '''
    Initialize filter using a normal distribution with and a
    standard deviation inversely proportional the square root of the number of units
    '''
    stddev = scale/np.sqrt(np.prod(size))
    return np.random.normal(loc = 0, scale = stddev, size = size)

def initializeWeight(size):
    '''
    Initialize weights with a random normal distribution
    '''
    return np.random.standard_normal(size=size) * 0.01


'''Step 3: Define the backpropagation operations'''

def convolutionBackward(dconv_prev, conv_in, filt, s):
    '''
    Backpropagation through a convolutional layer.
    '''
    (n_f, n_c, f, _) = filt.shape
    (_, orig_dim, _) = conv_in.shape
    ## initialize derivatives
    dout = np.zeros(conv_in.shape)
    dfilt = np.zeros(filt.shape)
    dbias = np.zeros((n_f,1))
    for curr_f in range(n_f):
        # loop through all filters
        curr_y = out_y = 0
        while curr_y + f <= orig_dim:
            curr_x = out_x = 0
            while curr_x + f <= orig_dim:
                # loss gradient of filter (used to update the filter)
                dfilt[curr_f] += dconv_prev[curr_f, out_y, out_x] * conv_in[:, curr_y:curr_y+f, curr_x:curr_x+f]
                # loss gradient of the input to the convolution operation (conv1 in the case of this network)
                dout[:, curr_y:curr_y+f, curr_x:curr_x+f] += dconv_prev[curr_f, out_y, out_x] * filt[curr_f]
                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1
        # loss gradient of the bias
        dbias[curr_f] = np.sum(dconv_prev[curr_f])

    return dout, dfilt, dbias

def nanargmax(arr):
    '''
    return index of the largest non-nan value in the array. Output is an ordered pair tuple
    '''
    idx = np.nanargmax(arr)
    idxs = np.unravel_index(idx, arr.shape)
    return idxs

def maxpoolBackward(dpool, orig, f, s):
    '''
    Backpropagation through a maxpooling layer. The gradients are passed through the indices of greatest value in the original maxpooling during the forward step.
    '''
    (n_c, orig_dim, _) = orig.shape

    dout = np.zeros(orig.shape)

    for curr_c in range(n_c):
        curr_y = out_y = 0
        while curr_y + f <= orig_dim:
            curr_x = out_x = 0
            while curr_x + f <= orig_dim:
                # obtain index of largest value in input for current window
                (a, b) = nanargmax(orig[curr_c, curr_y:curr_y+f, curr_x:curr_x+f])
                dout[curr_c, curr_y+a, curr_x+b] = dpool[curr_c, out_y, out_x]

                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1

    return dout

'''Step 4: Building the network'''
'''we now define a method that combines the forward and backward operations of a convolutional neural network. It takes the network’s parameters
 and hyperparameters as inputs and spits out the gradients:'''

def conv(image, label, params, conv_s, pool_f, pool_s):

    [f1, f2, w3, w4, b1, b2, b3, b4] = params

    ################################################
    ############## Forward Operation ###############
    ################################################
    conv1 = convolution(image, f1, b1, conv_s) # convolution operation
    conv1[conv1<=0] = 0 # pass through ReLU non-linearity

    conv2 = convolution(conv1, f2, b2, conv_s) # second convolution operation
    conv2[conv2<=0] = 0 # pass through ReLU non-linearity

    pooled = maxpool(conv2, pool_f, pool_s) # maxpooling operation

    (nf2, dim2, _) = pooled.shape
    fc = pooled.reshape((nf2 * dim2 * dim2, 1)) # flatten pooled layer

    z = w3.dot(fc) + b3 # first dense layer
    z[z<=0] = 0 # pass through ReLU non-linearity

    out = w4.dot(z) + b4 # second dense layer

    probs = softmax(out) # predict class probabilities with the softmax activation function

    ################################################
    #################### Loss ######################
    ################################################

    loss = categoricalCrossEntropy(probs, label) # categorical cross-entropy loss

    ################################################
    ############# Backward Operation ###############
    ################################################
    dout = probs - label # derivative of loss w.r.t. final dense layer output
    dw4 = dout.dot(z.T) # loss gradient of final dense layer weights
    db4 = np.sum(dout, axis = 1).reshape(b4.shape) # loss gradient of final dense layer biases

    dz = w4.T.dot(dout) # loss gradient of first dense layer outputs
    dz[z<=0] = 0 # backpropagate through ReLU
    dw3 = dz.dot(fc.T)
    db3 = np.sum(dz, axis = 1).reshape(b3.shape)

    dfc = w3.T.dot(dz) # loss gradients of fully-connected layer (pooling layer)
    dpool = dfc.reshape(pooled.shape) # reshape fully connected into dimensions of pooling layer

    dconv2 = maxpoolBackward(dpool, conv2, pool_f, pool_s) # backprop through the max-pooling layer(only neurons with highest activation in window get updated)
    dconv2[conv2<=0] = 0 # backpropagate through ReLU

    dconv1, df2, db2 = convolutionBackward(dconv2, conv1, f2, conv_s) # backpropagate previous gradient through second convolutional layer.
    dconv1[conv1<=0] = 0 # backpropagate through ReLU

    dimage, df1, db1 = convolutionBackward(dconv1, image, f1, conv_s) # backpropagate previous gradient through first convolutional layer.

    grads = [df1, df2, dw3, dw4, db1, db2, db3, db4]

    return grads, loss


'''Step 5: Training the network'''

def adamGD(batch, num_classes, lr, dim, n_c, beta1, beta2, params, cost):
    '''
    update the parameters through Adam gradient descnet.
    '''
    [f1, f2, w3, w4, b1, b2, b3, b4] = params

    X = batch[:,0:-1] # get batch inputs
    X = X.reshape(len(batch), n_c, dim, dim)
    Y = batch[:,-1] # get batch labels

    cost_ = 0
    batch_size = len(batch)

    # initialize gradients and momentum,RMS params
    df1 = np.zeros(f1.shape)
    df2 = np.zeros(f2.shape)
    dw3 = np.zeros(w3.shape)
    dw4 = np.zeros(w4.shape)
    db1 = np.zeros(b1.shape)
    db2 = np.zeros(b2.shape)
    db3 = np.zeros(b3.shape)
    db4 = np.zeros(b4.shape)

    v1 = np.zeros(f1.shape)
    v2 = np.zeros(f2.shape)
    v3 = np.zeros(w3.shape)
    v4 = np.zeros(w4.shape)
    bv1 = np.zeros(b1.shape)
    bv2 = np.zeros(b2.shape)
    bv3 = np.zeros(b3.shape)
    bv4 = np.zeros(b4.shape)

    s1 = np.zeros(f1.shape)
    s2 = np.zeros(f2.shape)
    s3 = np.zeros(w3.shape)
    s4 = np.zeros(w4.shape)
    bs1 = np.zeros(b1.shape)
    bs2 = np.zeros(b2.shape)
    bs3 = np.zeros(b3.shape)
    bs4 = np.zeros(b4.shape)

    for i in range(batch_size):

        x = X[i]
        y = np.eye(num_classes)[int(Y[i])].reshape(num_classes, 1) # convert label to one-hot

        # Collect Gradients for training example
        grads, loss = conv(x, y, params, 1, 2, 2)
        [df1_, df2_, dw3_, dw4_, db1_, db2_, db3_, db4_] = grads

        df1+=df1_
        db1+=db1_
        df2+=df2_
        db2+=db2_
        dw3+=dw3_
        db3+=db3_
        dw4+=dw4_
        db4+=db4_

        cost_+= loss

    # Parameter Update

    v1 = beta1*v1 + (1-beta1)*df1/batch_size # momentum update
    s1 = beta2*s1 + (1-beta2)*(df1/batch_size)**2 # RMSProp update
    f1 -= lr * v1/np.sqrt(s1+1e-7) # combine momentum and RMSProp to perform update with Adam

    bv1 = beta1*bv1 + (1-beta1)*db1/batch_size
    bs1 = beta2*bs1 + (1-beta2)*(db1/batch_size)**2
    b1 -= lr * bv1/np.sqrt(bs1+1e-7)

    v2 = beta1*v2 + (1-beta1)*df2/batch_size
    s2 = beta2*s2 + (1-beta2)*(df2/batch_size)**2
    f2 -= lr * v2/np.sqrt(s2+1e-7)

    bv2 = beta1*bv2 + (1-beta1) * db2/batch_size
    bs2 = beta2*bs2 + (1-beta2)*(db2/batch_size)**2
    b2 -= lr * bv2/np.sqrt(bs2+1e-7)

    v3 = beta1*v3 + (1-beta1) * dw3/batch_size
    s3 = beta2*s3 + (1-beta2)*(dw3/batch_size)**2
    w3 -= lr * v3/np.sqrt(s3+1e-7)

    bv3 = beta1*bv3 + (1-beta1) * db3/batch_size
    bs3 = beta2*bs3 + (1-beta2)*(db3/batch_size)**2
    b3 -= lr * bv3/np.sqrt(bs3+1e-7)

    v4 = beta1*v4 + (1-beta1) * dw4/batch_size
    s4 = beta2*s4 + (1-beta2)*(dw4/batch_size)**2
    w4 -= lr * v4 / np.sqrt(s4+1e-7)

    bv4 = beta1*bv4 + (1-beta1)*db4/batch_size
    bs4 = beta2*bs4 + (1-beta2)*(db4/batch_size)**2
    b4 -= lr * bv4 / np.sqrt(bs4+1e-7)


    cost_ = cost_/batch_size
    cost.append(cost_)

    params = [f1, f2, w3, w4, b1, b2, b3, b4]

    return params, cost

####################################################
##################### Training #####################
####################################################

def train(num_classes = 10, lr = 0.01, beta1 = 0.95, beta2 = 0.99, img_dim = 28, img_depth = 1, f = 5, num_filt1 = 8, num_filt2 = 8, batch_size = 32, num_epochs = 2, save_path = 'params.pkl'):

    # Get training data
    m =50000
    X = extract_data('train-images-idx3-ubyte.gz', m, img_dim)
    y_dash = extract_labels('train-labels-idx1-ubyte.gz', m).reshape(m,1)
    X-= int(np.mean(X))
    X/= int(np.std(X))
    train_data = np.hstack((X,y_dash))

    np.random.shuffle(train_data)

    ## Initializing all the parameters
    f1, f2, w3, w4 = (num_filt1 ,img_depth,f,f), (num_filt2 ,num_filt1,f,f), (128,800), (10, 128)
    f1 = initializeFilter(f1)
    f2 = initializeFilter(f2)
    w3 = initializeWeight(w3)
    w4 = initializeWeight(w4)

    b1 = np.zeros((f1.shape[0],1))
    b2 = np.zeros((f2.shape[0],1))
    b3 = np.zeros((w3.shape[0],1))
    b4 = np.zeros((w4.shape[0],1))

    params = [f1, f2, w3, w4, b1, b2, b3, b4]

    cost = []

    print("LR:"+str(lr)+", Batch Size:"+str(batch_size))

    for epoch in range(num_epochs):
        np.random.shuffle(train_data)
        batches = [train_data[k:k + batch_size] for k in range(0, train_data.shape[0], batch_size)]

        t = tqdm(batches)
        for x,batch in enumerate(t):
            params, cost = adamGD(batch, num_classes, lr, img_dim, img_depth, beta1, beta2, params, cost)
            t.set_description("Cost: %.2f" % (cost[-1]))


    with open(save_path, 'wb') as file:
        pickle.dump(params, file)

    return cost



############################
'''
Need to:
get features using cnn (can use pre trained model)
place image-net-image-net-...-output
calculate the error for every image to net
regions using mask?

Maybe just use Sequential()?

'''



'''suppose:
Flatten matrix a (frame a)
weights+biases
FC
'''


''''Loading VGG'''
from keras.applications.vgg16 import VGG16
model = VGG16(weights='imagenet', include_top=True)
model.summary()
#The VGG() class takes a few arguments that may only interest you if you are looking to use the model in your own project, e.g. for transfer learning.

'''include_top (True): Whether or not to include the output layers for the model. You don’t need these if you are fitting the model on your own problem.
weights (‘imagenet‘): What weights to load. You can specify None to not load pre-trained weights if you are interested in training the model yourself from scratch.
input_tensor (None): A new input layer if you intend to fit the model on new data of a different size.
input_shape (None): The size of images that the model is expected to take if you change the input layer.
pooling (None): The type of pooling to use when you are training a new set of output layers.
classes (1000): The number of classes (e.g. size of output vector) for the model.
'''

#to drop the last layers
from keras.models import Model
#Add a layer where input is the output of the  second last layer
x = Dense(1, activation='sigmoid', name='predictions')(model.layers[-2].output)


#Then create the corresponding model
my_model = Model(input=model.input, output=x)
my_model.summary()

IN_SHAPE = (256, 256, 3) # image dimensions and RGB channels

pretrained_model = VGG16(
  include_top=False,
  input_shape=IN_SHAPE,
  weights='imagenet'
)

#load the image and resize it

from keras.preprocessing.image import load_img
# load an image from file
image = load_img('cat.jpg', target_size=(224, 224))

#convert the pixels to a NumPy array

from keras.preprocessing.image import img_to_array
# convert the image pixels to a numpy array
image = img_to_array(image)

#The network expects one or more images as input; that means the input array will need to be 4-dimensional: samples, rows, columns, and channels.
#We only have one sample (one image). We can reshape the array by calling reshape() and adding the extra dimension.

# reshape data for the model
image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))


#Next, the image pixels need to be prepared in the same way as the ImageNet training data was prepared. Specifically, from the paper:
#The only preprocessing we do is subtracting the mean RGB value, computed on the training set, from each pixel.

from keras.applications.vgg16 import preprocess_input
# prepare the image for the VGG model
image = preprocess_input(image)

#make prediction
#prediction of the probability of the image belonging to each of the 1000 known object types.

# predict the probability across all output classes
yhat = model.predict(image)


#Interpret Prediction

# return a list of classes and their probabilities in case you would like to present the top 3 objects that may be in the photo.
#We will just report the first most likely object.

from keras.applications.vgg16 import decode_predictions
# convert the probabilities to class labels
label = decode_predictions(yhat)
# retrieve the most likely result, e.g. highest probability
#label = label[0][0]
# print the classification
#print('%s (%.2f%%)' % (label[1], label[2]*100))
label



#Extracting features from images
#The image features are a 1-dimensional 4,096 element vector.
#At the end of the run, you will have the extracted features stored in ‘features.pkl‘ for later use. This file will be about 127 Megabytes in size.

from os import listdir
from pickle import dump
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model

'''extract features from each photo in the directory'''
def extract_features(directory):
	# load the model
	model = VGG16()
	# re-structure the model
	model.layers.pop()
	model = Model(inputs=model.inputs, outputs=model.layers[-1].output)
	# summarize
	print(model.summary())
	# extract features from each photo
	features = dict()
	for name in listdir(directory):
		# load an image from file
		filename = directory + '/' + name
		image = load_img(filename, target_size=(224, 224))
		# convert the image pixels to a numpy array
		image = img_to_array(image)
		# reshape data for the model
		image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
		# prepare the image for the VGG model
		image = preprocess_input(image)
		# get features
		feature = model.predict(image, verbose=0)
		# get image id
		image_id = name.split('.')[0]
		# store feature
		features[image_id] = feature
		print('>%s' % name)
	return features

#call this function to prepare the photo data for testing our models, then save the resulting dictionary to a file named ‘features.pkl‘.


# extract features from all images
directory = 'cell_images/Uninfected'
features = extract_features(directory)
print('Extracted Features: %d' % len(features))
# save to file
dump(features, open('features.pkl', 'wb'))

import pickle

with open('features.pkl', 'rb') as f:
    data = pickle.load(f)


import matplotlib.cm as cm
import matplotlib.pyplot as plt

#plot images
plt.imshow(data['C100P61ThinF_IMG_20150918_145042_cell_5'].reshape((64, 64)), cmap=cm.Greys_r)
plt.show()

plt.imshow(data['C100P61ThinF_IMG_20150918_145042_cell_59'].reshape((64, 64)), cmap=cm.Greys_r)
plt.show()

for x in data:
  print('this is: ' + str(x))
  plt.imshow(data[x].reshape((64, 64)), cmap=cm.Greys_r)
  plt.show()


'''An Example of Merge Layer in Keras'''
                                               InputLayer (None, 6)
                                                    Dense (None, 6)
                                       BatchNormalization (None, 6)
                                                    Dense (None, 6)
        InputLayer (None, 4)           BatchNormalization (None, 6)
             Dense (None, 4)                        Dense (None, 6)
BatchNormalization (None, 4)           BatchNormalization (None, 6)
                   \____________________________________/
                                     |
                                Merge (None, 10)
                                Dense (None, 1)

from pandas import read_csv, DataFrame
from numpy.random import seed
from sklearn.preprocessing import scale
from keras.models import Sequential
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers import Dense, Merge
from keras.layers.normalization import BatchNormalization
from keras_diagram import ascii

df = read_csv("credit_count.txt")
Y = df[df.CARDHLDR == 1].DEFAULTS
X1 = scale(df[df.CARDHLDR == 1][["MAJORDRG", "MINORDRG", "OWNRENT", "SELFEMPL"]])
X2 = scale(df[df.CARDHLDR == 1][["AGE", "ACADMOS", "ADEPCNT", "INCPER", "EXP_INC", "INCOME"]])

branch1 = Sequential()
branch1.add(Dense(X1.shape[1], input_shape = (X1.shape[1],), init = 'normal', activation = 'relu'))
branch1.add(BatchNormalization())

branch2 = Sequential()
branch2.add(Dense(X2.shape[1], input_shape =  (X2.shape[1],), init = 'normal', activation = 'relu'))
branch2.add(BatchNormalization())
branch2.add(Dense(X2.shape[1], init = 'normal', activation = 'relu', W_constraint = maxnorm(5)))
branch2.add(BatchNormalization())
branch2.add(Dense(X2.shape[1], init = 'normal', activation = 'relu', W_constraint = maxnorm(5)))
branch2.add(BatchNormalization())

model = Sequential()
model.add(Merge([branch1, branch2], mode = 'concat')) ###########################################################################################
model.add(Dense(1, init = 'normal', activation = 'sigmoid'))
sgd = SGD(lr = 0.1, momentum = 0.9, decay = 0, nesterov = False)
model.compile(loss = 'binary_crossentropy', optimizer = sgd, metrics = ['accuracy'])
seed(2017)
model.fit([X1, X2], Y.values, batch_size = 2000, nb_epoch = 100, verbose = 1)

###########################################
''''Loading VGG'''
from keras.applications.vgg16 import VGG16
model = VGG16(weights='imagenet', include_top=True)

'''extract features from each photo in the directory'''
def extract_features(directory):
	# load the model
	model = VGG16()
	# re-structure the model
	model.layers.pop()
	model = Model(inputs=model.inputs, outputs=model.layers[-1].output)
	# summarize
	print(model.summary())
	# extract features from each photo
	features = dict()
	for name in listdir(directory):
		# load an image from file
		filename = directory + '/' + name
		image = load_img(filename, target_size=(224, 224))
		# convert the image pixels to a numpy array
		image = img_to_array(image)
		# reshape data for the model
		image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
		# prepare the image for the VGG model
		image = preprocess_input(image)
		# get features
		feature = model.predict(image, verbose=0)
		# get image id
		image_id = name.split('.')[0]
		# store feature
		features[image_id] = feature
		print('>%s' % name)
	return features



def frames(initial_frames, five_frames): '''initial_frames is the first seq, input 5 frames (lets say we get 5 frames per sec)'''
    matrix=[[x1],[x2],[x3],[x4],[x5],[x6],[x7],[x8],[x9],[x10]] #initial_frames


'''
every x_i is a sequence of frames.
First get the weights by training, then use the weights with the new output to check it.
so you need to send x1[0],x1[1]...x1[5] to train. then x1[1],x1[2]...x1[6]... and so on until you're done with x1 frame.
Then move to x2[0]...x2[5]... until you're done with x2
check how to split the data in LSTM (since it's a sequence as well)--> maybe just take a few x_i's (x6,x7) for validation and use the other ones for training
'''

def fc1(input,output,num_neurons): '''the input is a frame, output is the next frame, num_neurons is the number of neurons in the layer'''
    #flatten the matrix
    #create the num_neurons
    #
    pass

from keras.models import Sequential
from keras.layers import Dense
import numpy

'''
option 2: use Sequential model
have 10 frames at a time for 10 Sequential models.
what to do about the weights? every sequential will give me weights
can I change the output as I go?
perhaps split the datasets to x1,x2... where each x_i is a sequence of 10 frames
(whats difference here is that x1 and x2 can have similar frames)
ex:
x1 (f1-f10), x2 (f2-f11)...
so if i split my data before I dont have to worry about moving frames as I train.

'''

def fc2(input, output, num_neurons): '''lets say the input is already flat'''
    model = Sequential()
    model.add(Dense(num_neurons, input_dim=input, activation='relu'))
    model.add(Dense(output, activation='softmax'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, epochs=150, batch_size=10)

scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


'''Keras Functional model'''
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense

# Define the input
#   Unlike the Sequential model, you must create and define
#   a standalone "Input" layer that specifies the shape of input
#   data. The input layer takes a "shape" argument, which is a
#   tuple that indicates the dimensionality of the input data.
#   When input data is one-dimensional, such as the MLP, the shape
#   must explicitly leave room for the shape of the mini-batch size
#   used when splitting the data when training the network. Hence,
#   the shape tuple is always defined with a hanging last dimension.
#   For instance, "(2,)", as in the example below:
visible = Input(shape=(2,))

# Connecting layers
#   The layers in the model are connected pairwise.
#   This is done by specifying where the input comes from when
#   defining each new layer. A bracket notation is used, such that
#   after the layer is created, the layer from which the input to
#   the current layer comes from is specified.
#   Note how the "visible" layer connects to the "Dense" layer:
hidden = Dense(2)(visible)

# Create the model
#   After creating all of your model layers and connecting them
#   together, you must then define the model.
#   As with the Sequential API, the model is the thing that you can
#   summarize, fit, evaluate, and use to make predictions.
#   Keras provides a "Model" class that you can use to create a model
#   from your created layers. It requires that you only specify the
#   input and output layers. For example:
model = Model(inputs=visible, outputs=hidden)


'''new architecture'''
# Multiple Inputs
from keras.utils import plot_model
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate
# first input model
visible1 = Input(shape=(64,64,1))
conv11 = Conv2D(32, kernel_size=4, activation='relu')(visible1)
pool11 = MaxPooling2D(pool_size=(2, 2))(conv11)
conv12 = Conv2D(16, kernel_size=4, activation='relu')(pool11)
pool12 = MaxPooling2D(pool_size=(2, 2))(conv12)
flat1 = Flatten()(pool12)
# second input model
visible2 = Input(shape=(32,32,3))
conv21 = Conv2D(32, kernel_size=4, activation='relu')(visible2)
pool21 = MaxPooling2D(pool_size=(2, 2))(conv21)
conv22 = Conv2D(16, kernel_size=4, activation='relu')(pool21)
pool22 = MaxPooling2D(pool_size=(2, 2))(conv22)
flat2 = Flatten()(pool22)
# merge input models
merge = concatenate([flat1, flat2])
# interpretation model
hidden1 = Dense(10, activation='relu')(merge)
hidden2 = Dense(10, activation='relu')(hidden1)
output = Dense(1, activation='sigmoid')(hidden2)
model = Model(inputs=[visible1, visible2], outputs=output)
# summarize layers
print(model.summary())
# plot graph
plot_model(model, to_file='multiple_inputs.png')


'''perhaps for the inputs I need to put x[0], x[1]...'''
