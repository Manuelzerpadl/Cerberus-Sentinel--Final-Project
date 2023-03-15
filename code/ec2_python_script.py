import pandas as pd
import boto3
import io
import datetime

s3 = boto3.client('s3', region_name='eu-central-1')

def create_sample_data(s3_uri:str):
    bucket = s3_uri.split('/')[2]
    key = '/'.join(s3_uri.split('/')[3:])

    response = s3.get_object(Bucket=bucket, Key=key)
    contents = response['Body'].read().decode('utf-8')

    df = pd.read_csv(io.StringIO(contents))
    return df

def upload_sample_data(df, bucket:str):
    
    df = df.sample(n=200, replace=True)
    df.drop(columns='isFraud', inplace=True)

    today = datetime.datetime.today()
    date_str = today.strftime('%Y-%m-%d')
    
    csv_string = df.to_csv(index=False)
    object_key = f'transaction_{date_str}_fraud.csv'
    content_type = "text/csv"
    s3.put_object(Bucket=bucket, Key=object_key, Body=csv_string, ContentType=content_type)
    
df = create_sample_data('s3://fraud-manuel/Fraud.csv')
upload_sample_data(df, 'fraud-manuel')