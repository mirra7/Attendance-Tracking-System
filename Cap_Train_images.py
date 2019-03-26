# Import all required libraries
try:
    import sys
    import os
    from model import create_model
    import numpy as np
    import os.path
    import pickle
    import cv2
    from align import AlignDlib
    import warnings
    warnings.filterwarnings('ignore')
except:
    print("Error in importing libraries. Kindly check whether libraries are properly installed!")
    sys.exit()

# Initialising the pretrained model
dir = os.getcwd()
if len(os.listdir(dir+'\\train_images'))>0:
    nn4_small2_pretrained = create_model()
    nn4_small2_pretrained.load_weights('./weights/nn4.small2.v1.h5')


    class IdentityMetadata():
        def __init__(self, base, file):
            # dataset base directory
            self.base = base
            # image file name
            self.file = file

        def __repr__(self):
            return self.image_path()

        def image_path(self):
            return os.path.join(self.base, self.file) 

    def load_metadata(path):
        metadata = []
        for i in os.listdir(path):
            ext = os.path.splitext(i)[1]
            if ext == '.jpg' or ext == '.jpeg':
                metadata.append(IdentityMetadata(path, i))
        return np.array(metadata)

    def load_image(path):
        img = cv2.imread(path, 1)
        # OpenCV loads images with color channels
        # in BGR order. So we need to reverse them
        return img[...,::-1]

    # Initialize the OpenFace face alignment utility
    alignment = AlignDlib('./models/landmarks.dat')
    def align_image(img):
        return alignment.align(96, img, alignment.getLargestFaceBoundingBox(img), 
                               landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)

    metadata_train = load_metadata(dir+'\\train_images')
    embedded_train = np.zeros((metadata_train.shape[0], 128))
    for i, m in enumerate(metadata_train):
        img = load_image(m.image_path())
        try:
            img = align_image(img)
            #     # scale RGB values to interval [0,1]
            img = (img / 255. ).astype(np.float)
            #     # obtain embedding vector for image
            embedded_train[i] = nn4_small2_pretrained.predict(np.expand_dims(img, axis=0))[0]
        except:
            continue


    y_train = np.array([m.file.split('.')[1] for m in metadata_train])
    X_train = embedded_train
    trained = (X_train,y_train)
    # Saving the values to be used later
    pickling_on = open("Train.pickle","wb")
    pickle.dump(trained, pickling_on)
    pickling_on.close()
else:
    print("No Images to train. Kindly capture images and try again.")


