import boto3
import pandas as pd
import datetime
import io
import psycopg2
import csv

def read_csv_from_s3(bucket, key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    rows = response['Body'].read().decode('utf-8').split('\n')
    csv_reader = csv.reader(rows)
    next(csv_reader)  # skip header row if there is one
    return [tuple(row) for row in csv_reader if row]


def upload_data(data):
    # Set up the database connection
    conn = psycopg2.connect(
        host='fraud-database-instance.cb1ukleqvlql.eu-central-1.rds.amazonaws.com',
        port=5432,
        user='postgres',
        password='fraudproject',
        database='fraud_database'
    )
    
    # Create a cursor for executing SQL queries
    cursor = conn.cursor()
    
    # Create the table in the database (if it doesn't already exist)
    cursor.execute("""CREATE TABLE IF NOT EXISTS fraud_records_historic (
                    step                INTEGER,
                    type                INTEGER,
                    amount              FLOAT,
                    nameorig            VARCHAR(255),
                    oldbalanceorg       FLOAT,
                    newbalanceorig      FLOAT,
                    namedest            VARCHAR(255),
                    oldbalancedest      FLOAT,
                    newbalancedest      FLOAT,
                    isfraud             INTEGER,
                    isflaggedfraud      INTEGER,
                    date                TIMESTAMP
    )""")
    
    # Insert the data into the table
    count = 0
    for row in data:
        cursor.execute("""INSERT INTO fraud_records_historic (
                       step, 
                       type, 
                       amount, 
                       nameorig, 
                       oldbalanceorg, 
                       newbalanceorig, 
                       namedest, 
                       oldbalancedest, 
                       newbalancedest, 
                       isfraud, 
                       isflaggedfraud,
                       date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (row.step, 
                                                                                                row.type, 
                                                                                                row.amount, 
                                                                                                row.nameorig, 
                                                                                                row.oldbalanceorg, 
                                                                                                row.newbalanceorig, 
                                                                                                row.namedest, 
                                                                                                row.oldbalancedest, 
                                                                                                row.newbalancedest, 
                                                                                                row.isfraud, 
                                                                                                row.isflaggedfraud,
                                                                                                row.date))
        count += 1
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Inserted {count} records into the database")

def insert_records(bucket, key):
    today = datetime.datetime.today()
    date_str = today.strftime('%Y-%m-%d')
    key = f'transaction_{date_str}_fraud.csv'

    data = read_csv_from_s3(bucket, key)
    upload_data(data)

def lambda_handler(event, context):
    print(f"Processing event: {event}")    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        insert_records(bucket, key)
