from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score
import pickle

data = pd.read_csv('cardio_train.csv')

data.dropna(subset = ['id', 'age', 'gender', 'height' ,"weight" ,"ap_hi" ,"ap_lo","cholesterol","gluc","smoke" ,"alco" ,"active", 'cardio'], inplace=True)



X = data.drop(columns=['cardio', 'id', 'ap_hi', 'ap_lo'])
y = data['cardio']



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


dtc = DecisionTreeClassifier()

dtc.fit(X_train, y_train)

pickle.dump(dtc, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb')) 