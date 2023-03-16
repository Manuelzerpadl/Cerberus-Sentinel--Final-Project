import boto3
import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def destroy_ec2(instance_id, key_pair_name):
    ec2 = boto3.resource('ec2', region_name='eu-central-1')
    
    # # Terminate the EC2 instance
    instance = ec2.Instance(instance_id)
    instance.terminate()
    instance.wait_until_terminated()

    # Delete the key pair
    key_pair = ec2.KeyPair(key_pair_name)
    key_pair.delete()

    print(f"EC2 instance {instance_id}, and key pair {key_pair_name} have been destroyed.")


instance_id = 'i-01a1deab0965fdc3d'
key_pair_name = 'ec2-fraud-keypair'

destroy_ec2(instance_id, key_pair_name)
