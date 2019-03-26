# Importing all required libraries
try:    
    import sys
    import os
    from model import create_model
    import numpy as np
    import pandas as  pd
    import os.path
    import shutil
    import pickle
    from os import listdir
    import cv2
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import f1_score, accuracy_score
    from align import AlignDlib
    from datetime import datetime
    import warnings
    warnings.filterwarnings('ignore')
except:
    print("Error in importing libraries. Kindly check whether libraries are properly installed!")
    sys.exit()
dir = os.getcwd()    
sub = sys.argv[1] # Reading the user input of subject
fac = sys.argv[2] # Reading the user input 
period = sys.argv[3]
nn4_small2_pretrained = create_model()
nn4_small2_pretrained.load_weights('./weights/nn4.small2.v1.h5')


image_folder = os.getcwd() + "/" + 'group_images/'
detected_images = os.getcwd() + "/" + 'test_images/'

faceCascade = cv2.CascadeClassifier(os.getcwd()+"\\haarcascades\\haarcascade_frontalface_default.xml")


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
# capturing group images


# Unpickling Train images and labels
pickling_out = open("Train.pickle","rb")
Trained = pickle.load(pickling_out)
X_train = Trained[0]
y_train = Trained[1]
# Reading student Details CSV

times = 0
try:
    st = pd.read_csv(filname)
except:
    st = pd.read_csv('Student_List.csv')
student_att = st[['Roll_Number','Student_Name']]
for j in listdir(image_folder):
    try:
        os.mkdir(detected_images)
    except:
        print()
    print(image_folder + j)
    image = cv2.imread(image_folder + j, 1)
    faces = faceCascade.detectMultiScale(image,scaleFactor=1.3,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
    print ("Found {0} faces!".format(len(faces)))
    
# # Draw a rectangle around the faces
    for f,(x, y, w, h) in enumerate(faces):
        cv2.imwrite(detected_images + 'Face' + j + "_" + str(f) + ".jpg", image[y:y+h,x:x+w])

    try:
        metadata_test = load_metadata(dir+'\\test_images')
    except:
        os.mkdir('test_images')

    embedded_test = np.zeros((metadata_test.shape[0], 128))
    for i, m in enumerate(metadata_test):
        img = load_image(m.image_path())
        try:
            img = align_image(img)
            #       scale RGB values to interval [0,1]
            img = (img / 255. ).astype(np.float)
            #      obtain embedding vector for image
            embedded_test[i] = nn4_small2_pretrained.predict(np.expand_dims(img, axis=0))[0]
            
        except:
            print("Image cannot be aligned!")
            os.remove(m.image_path())
            continue
    X_test = embedded_test


    knn = KNeighborsClassifier(n_neighbors=2, metric='euclidean')
    knn.fit(X_train, y_train)
    example_idx = 0
    filname = "Attendance_Tracker\\Attendance_" + str(sub) + ".csv"
    
    
    student_att['Run_'+str(times)] = 0
    for k in listdir(detected_images):
        test_idx = np.arange(metadata_test.shape[0])
        try:
            example_image = load_image(metadata_test[test_idx][example_idx].image_path())
        except:
            continue
        example_prediction = knn.predict([embedded_test[test_idx][example_idx]])
        print("EXAM_pred", example_prediction)
        roll_nbr = int(example_prediction[0])
        print(roll_nbr)
        student_att['Run_' + str(times)] = student_att.apply( lambda x:1 if ((x.Roll_Number==roll_nbr) | (x['Run_'+str(times)]==1)) else 0,axis=1)
        os.remove(detected_images+'\\'+k)
        example_idx += 1
    times+=1
dte = str(datetime.now().strftime("%d-%m-%Y"))
cols  = student_att.columns[2:]
student_att[dte]=student_att.apply(lambda x: 'P' if (sum(x[cols])/len(cols))>.5 else 'A' ,axis=1)
Student_Attendance = student_att.iloc[:,[0,1,-1]]
tab_name =  dte + "|" + fac + "|" + sub + "|" + "period " + period
st[tab_name] = Student_Attendance[dte]
columns = list(st.columns)
columns = list(filter(lambda x: not x.startswith('Unnamed'),columns))
st=  st[columns]
st.to_csv('Attendance_Tracker\Attendance' + "_" + str(sub)+'.csv')
#student_att.to_csv("C:\\Users\\Mirra\\Desktop\\Capstone\\temp\\" + "_" + str(sub) + '.csv')


