import json
import numpy as np
import boto3
import urllib
from PIL import Image

# Initialize AWS XRAY
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
patch_all()

# Initialize and long running objects...
s3 = boto3.resource('s3')
dynamo = boto3.resource('dynamodb')
table = dynamo.Table('YelpPhotos')

def lambda_handler(event, context): 
  """
  Entry point that Lambda will invoke
  """

  # Debug print... 
  #print(json.dumps(event))
  
  # Fetch the requeseted object
  task = event['tasks'][0]
  process_task(task)
  
  return {
    "invocationSchemaVersion": "1.0",
    "treatMissingKeysAs" : "Succeeded",
    "invocationId" : event["invocationId"],
    "results": [
      {
        "taskId": task['taskId'],
        "resultCode": "Succeeded",
        "resultString": "taco"
      }
    ]
  }

@xray_recorder.capture('process_task')
def process_task(task):
  """
  Processes an individual task from the S3 BatchJob
  """
  # Extract the requested file information...
  bucket = task['s3BucketArn'].split(':')[-1]
  key = urllib.parse.unquote(task['s3Key'])
  #print('Task requested s3://{b}/{k}'.format(b=bucket, k=key))
  xray_recorder.put_annotation('bucket',bucket)
  xray_recorder.put_annotation('key',key)
  
  # Attempt to download the file and process it
  # Transformation includes:
  #  - Resize to 64x64
  #  - Convert to Grey Scale
  #  - Flatten into 4096x1 array
  s3.Object(bucket,key).download_file('/tmp/file.jpg')
    
  im = Image.open('/tmp/file.jpg')
  im = im.resize((64,64), Image.ANTIALIAS)
  grey = im.convert('L')
  pixels = np.array(grey).flatten()
  save_image(key=key, pixels=pixels)

@xray_recorder.capture('save_image')
def save_image(key, pixels):
  """
  Writes the resized image into Dynamo
  """    
  photo_id = key.split('/')[-1]
  xray_recorder.put_annotation('photo_id',photo_id)
  #print('Saving {id} of {shape} to dynamo'.format(id=photo_id,shape=pixels.shape))

  table.put_item(
    Item={
      'photo_id': photo_id,
      'sort_key': 'train::64x64',
      'pixels': pixels.tolist()
    })
