import json
import boto3
from PIL import Image
from PIL.Image import core as _imaging
from io import BytesIO
import os

def lambda_handler(event, context):
    key = event["Records"][0]["s3"]["object"]["key"]
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    try:
        result = resize_image(bucket, key)
        return result
    except:
        raise

def resize_image(s3bucket, s3key):
    s3 = boto3.resource('s3')
    response = s3.Object(
        bucket_name=s3bucket,
        key=s3key
    )
    size = (200,200)
    img_body = response.get()['Body'].read()
    img = Image.open(BytesIO(img_body))
    img = img.resize(size)
    buffer = BytesIO()
    img.save(buffer, 'JPEG')
    buffer.seek(0)
    resized_key="{x}_{y}_{key}".format(x=size[0], y=size[1], key=s3key)
    obj = s3.Object(
        bucket_name=os.environ['DEST_S3_BUCKET'],
        key=resized_key,
    )
    obj.put(Body=buffer, ContentType='image/jpeg')