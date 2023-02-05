import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier,_tree
# this package is used to change raw feature vectors into a representation that is more suitable for some uses.
from sklearn import preprocessing as preprocess
# used to split the dataset into training and testing arrays
from sklearn.model_selection import train_test_split as tts
from sklearn.model_selection import cross_val_score as cvs
from sklearn.svm import SVC
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


# training and testing the data read from the csv files
train = pd.read_csv('../data/test1.csv') 
test = pd.read_csv('../data/test1.csv') # TODO update with test file when it's done
#reading = pd.read_csv('../data/test.csv')
columns = train.columns
columns = columns[:-1]
x = train[columns]
y = train['injury']

# transforming non-numerical labels to numerical labels
label_encoder = preprocess.LabelEncoder()
label_encoder.fit(y)
y = label_encoder.transform(y)
print("y is ", y)

# splitting 33 percent of the data for testing and the rest is used for training
xTrain, xTest, yTrain, yTest = tts(x, y, test_size = 0.33)
testingX = test[columns]
testingY = test['injury']
# transform into numerical labels
testingY = label_encoder.transform(testingY)


classification  = DecisionTreeClassifier()
classification1 = classification.fit(xTrain,yTrain)
scores = cvs(classification1, xTest, yTest, cv=3)
print(classification1.predict(xTest))

print ("Mean", scores.mean())

model1 = SVC()
model1.fit(xTrain,yTrain)
print("svm model: ")
print(model1.score(xTest,yTest))

featureImp = classification1.feature_importances_
indices = np.argsort(featureImp)[::-1]
attributes = columns

symptomsDict = {}

for i, s in enumerate(x):
       symptomsDict[s] = i
       
def prediction(explainedSymptom):
    df = pd.read_csv('../data/test1.csv')
    x = df.iloc[:, :-1]
    y = df['injury']
    x_train, x_test, y_train, y_test = tts(x, y, test_size=0.3, random_state=20)
    tree_clf = DecisionTreeClassifier()
    tree_clf.fit(x_train, y_train)

    symptomsDict = {s: i for index, symptom in enumerate(x)}
    
    input_vector = np.zeros(len(symptomsDict))
    for item in explainedSymptom:
      input_vector[[symptomsDict[item]]] = 1

    return tree_clf.predict([input_vector])
#print(reading)
#print(xTest)
#print(model1.predict(xTest))
#print(yTest)