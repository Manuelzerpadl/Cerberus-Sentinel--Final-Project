import boto3
import pandas as pd
import pickle
import datetime
import io
from io import BytesIO

def read_pickle_model(bucket:str, key:str):
    # Set up S3 client
    s3 = boto3.client('s3', region_name = 'eu-central-1')
    # Load the file object from S3 bucket
    file_obj = s3.get_object(Bucket=bucket, Key=key)['Body'].read()

    # Load the pickle file using pickle
    data = pickle.load(BytesIO(file_obj))
    return data

def read_csv_from_bucket(bucket:str, key:str):
    s3 = boto3.client('s3', region_name = 'eu-central-1')
    response = s3.get_object(Bucket=bucket, Key=key)
    contents = response['Body'].read().decode('utf-8')
    df = pd.read_csv(io.StringIO(contents))
    return df

def evaluate_records(df:object, model:object):
    # Make predictions on the test dataset using the trained model
    y_pred = model.predict(df.drop(columns = ['namedest', 'nameorig']))
    df['isfraud'] = y_pred
    return df

def upload_to_bucket(dataframe, bucket, key):
    # Convert dataframe to CSV format
    csv_buffer = io.StringIO()
    dataframe.to_csv(csv_buffer, index=False)
    
    # Connect to S3 bucket
    s3 = boto3.resource('s3')
    s3_object = s3.Object(bucket, key)
    
    # Upload CSV to S3
    s3_object.put(Body=csv_buffer.getvalue())
    
    print(f'Successfully uploaded {key} to S3 bucket {bucket}')


def main():
    today = datetime.datetime.today()
    date_str = today.strftime('%Y-%m-%d')

    model_bucket = 'source-bucket-fraud-manuel'
    model_file_key = 'xgb_weights.pkl'

    daily_bucket = 'daily-bucket-fraud-manuel'
    daily_key = f'transaction_{date_str}_fraud.csv'

    predicted_bucket = 'daily-bucket-fraud-predicted-manuel'
    predicted_csv_key = f'transaction_{date_str}_fraud.csv'
    
    df = evaluate_records(read_csv_from_bucket(daily_bucket, daily_key), read_pickle_model(model_bucket, model_file_key))
    upload_to_bucket(df, predicted_bucket, predicted_csv_key)

main()