import boto3
import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def create_ec2(instance_type, iam_role_arn, key_name, security_group_name):
    ec2 = boto3.resource('ec2', region_name='eu-central-1')
    # Check if key pair exists
    existing_key_pairs = ec2.key_pairs.filter(Filters=[{'Name': 'key-name', 'Values': [key_pair_name]}])
    if list(existing_key_pairs):
        # Use the existing key pair
        key_pair = ec2.KeyPair(key_pair_name)
    else:
        # Create a new key pair
        key_pair = ec2.create_key_pair(KeyName=key_pair_name)
        # Save the private key to a file
        with open(f"{key_pair_name}.pem", "w") as file:
            file.write(key_pair.key_material)

    # Create the IAM instance profile object
    iam = boto3.resource('iam')
    instance_profile = iam.InstanceProfile(iam_role_arn)

    sgs = list(ec2.security_groups.filter(GroupNames=[security_group_name]))
    security_group_id = sgs[0].id

    block_device_mappings = [
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'VolumeSize': 30,
                'VolumeType': 'gp2'
            }
        }
    ]

    instances = ec2.create_instances(
        ImageId='ami-06616b7884ac98cdd', # Amazon Linux 2 AMI ID
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        KeyName=key_name,  # <--- Add this line
        UserData=user_data_script,
        IamInstanceProfile={
            'Arn': instance_profile.arn
        },
        BlockDeviceMappings=block_device_mappings,
        SecurityGroupIds=[security_group_id]
    )
    instance = instances[0]
    return instance.id

user_data_script = """#!/bin/bash
sudo yum update -y
sudo yum install -y python3
sudo yum install -y python3-pip
sudo yum install -y git
pip3 install boto3
pip3 install pandas
git clone https://github.com/Manuelzerpadl/Final-Project.git 
python3 Final-Project/code/ec2_python_script.py
"""

instance_type = 't2.large'
iam_role_arn = 'ec2_para_s3'
key_pair_name = 'ec2-fraud-keypair'
security_group_name = 'ssh-access-ec2'

instance_id = create_ec2(instance_type, iam_role_arn, key_pair_name, security_group_name)
print(instance_id)
