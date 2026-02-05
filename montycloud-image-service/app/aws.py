import boto3, os

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localhost:4566")
REGION = "us-east-1"

s3 = boto3.client(
    "s3",
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name=REGION
)

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name=REGION
)

table = dynamodb.Table("montycloud_images_metadata")
