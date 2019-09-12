import json
import boto3
from PIL import Image
from PIL.Image import core as _imaging
from io import BytesIO
import os


def lambda_handler(event, context):

    # Handle Amazon S3 event
    key = event["Records"][0]["s3"]["object"]["key"]
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    try:
        result = resize_image(bucket, key)
        return result
    except:
        raise


def resize_image(s3bucket, s3key):

    # Initialize boto3
    s3 = boto3.resource("s3")

    # Get Amazon S3 Object and stream it
    response = s3.Object(bucket_name=s3bucket, key=s3key)
    size = (200, 200)
    img_body = response.get()["Body"].read()
    img = Image.open(BytesIO(img_body))

    # Resize and save
    img = img.resize(size)
    buffer = BytesIO()
    img.save(buffer, "JPEG")
    buffer.seek(0)
    resized_key = "{x}_{y}_{key}".format(x=size[0], y=size[1], key=s3key)

    # Put resized imaged to destionation Amazon S3 Bucket
    obj = s3.Object(bucket_name=os.environ["DEST_S3_BUCKET"], key=resized_key)
    return obj.put(Body=buffer, ContentType="image/jpeg")

