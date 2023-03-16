import boto3
import json

iam_client = boto3.client('iam', region_name = 'eu-central-1')

def create_iam_role(role_name, policies):
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Principal": {
                "Service": [
                "lambda.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
            }
        ]
    }

    response = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
    )

    role_arn = response['Role']['Arn']

    for policy in policies:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=f"arn:aws:iam::aws:policy/{policy}"
        )

    return role_arn

role_name = 'MyLambdaS3AndRDSFullAccessRole'
policies = ['AmazonS3FullAccess', 'AmazonRDSFullAccess', 'service-role/AWSLambdaBasicExecutionRole']
role_arn = create_iam_role(role_name, policies)

print(f"Created IAM role '{role_name}' with ARN: {role_arn}")
