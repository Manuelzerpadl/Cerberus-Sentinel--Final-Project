import pickle
import os
import boto3
import io

import numpy as np
import pandas as pd

import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from imblearn.over_sampling import SMOTE

import warnings
warnings.filterwarnings('ignore')

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.client('s3', region_name='eu-central-1',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

response = s3.get_object(Bucket='source-bucket-fraud-manuel', Key='raw_fraud.csv')
contents = response['Body'].read().decode('utf-8')

df = pd.read_csv(io.StringIO(contents))
df.columns = [col.lower().replace(' ', '_') for col in df.columns]

le = LabelEncoder()
df['type'] = le.fit_transform(df['type'])
#df['namedest'] = le.fit_transform(df['namedest'])

X = df.drop(columns=['isfraud', 'namedest', 'nameorig'])
y = df['isfraud']

over_sample = SMOTE(random_state=0)
X,y = over_sample.fit_resample(X,y)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

xgb_model = xgb.XGBClassifier()
xgb_model.fit(X_train, y_train)

y_pred = xgb_model.predict(X_test)


bucket = 'source-bucket-fraud-manuel'

with open("xgb_weights.pkl", "wb") as f:
    pickle.dump(xgb_model, f)

try:
    s3.upload_file("xgb_weights.pkl", bucket, "xgb_weights.pkl")
    print(f'Successfully uploaded "xgb_weights.pkl" to S3 bucket "{bucket}".')
except Exception as e:
    print(f'Error uploading file to S3: {e}')


df.to_csv(r"Fraud.csv", index=False)
try:
    s3.upload_file("Fraud.csv", bucket, "Fraud.csv")
    print(f'Successfully uploaded "Fraud.csv" to S3 bucket "{bucket}".')
except Exception as e:
    print(f'Error uploading file to S3: {e}')
