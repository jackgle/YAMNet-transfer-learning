import os
import numpy as np
from random import shuffle
from tensorflow.python.keras.utils.data_utils import Sequence
os.sys.path.append('../models/research/audioset/yamnet')
import params


def get_files_and_labels(train_dir, typ='wav', train_split=0.9):
    
    classes = sorted(os.listdir(train_dir))
    class_dict = dict(zip(range(0,len(classes)),classes))
    files_train = list()
    labels_train = dict()
    files_val = list()
    labels_val = dict()
    for cnt, i in enumerate(classes): # loop over classes
        tmp = os.listdir(train_dir+i)
        shuffle(tmp)
        for j in tmp[:round(len(tmp)*train_split)]: # loop over training samples
            if j.split('.')[-1]==typ:
                files_train.append(train_dir + i +'/' + j)
                labels_train[i]=cnt
        for j in tmp[round(len(tmp)*train_split):]: # loop over validation samples
            if j.split('.')[-1]==typ:
                files_val.append(train_dir + i +'/' + j)
                labels_val[i]=cnt
                
    return files_train, labels_train, files_val, labels_val, class_dict

    
    
class DataGenerator(Sequence):
    
    'Generates YAMNet patches'
    def __init__(self, 
                 list_IDs, 
                 labels, 
                 dim = (96, 64),
                 batch_size=1, 
                 n_classes=2,
                 shuffle=True,
                 class_weights=None):
        'Initialization'
        self.batch_size = batch_size
        self.labels = labels
        self.dim = dim
        self.list_IDs = list_IDs
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.class_weights = class_weights
        self.on_epoch_end()
        

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        if self.class_weights:
            X, y, sample_weights = self.__data_generation(list_IDs_temp)
            return X, y, sample_weights
        else:    
            X, y = self.__data_generation(list_IDs_temp)
            return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization   

        X = np.empty((self.batch_size, *self.dim))
        y = np.empty((self.batch_size, self.n_classes))
        sample_weights = np.empty((self.batch_size, ))
        
        y[:] = 0
        
        # Generate data
        for i, ID in enumerate(list_IDs_temp):
                               
            class_id = ID.split('/')[-2]
            y[i,self.labels[class_id]] = 1
                        
            X[i,] = np.load(ID)
            
            if self.class_weights:
                sample_weights[i] = self.class_weights[self.labels[species_id]]
          
        
        if self.class_weights is not None:
            return X, y, sample_weights
        else:
            return X, y
    
    
    
    
    