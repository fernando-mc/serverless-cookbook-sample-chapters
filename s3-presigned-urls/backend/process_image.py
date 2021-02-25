import boto3
import json
import os

from colorthief import ColorThief

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
s3 = boto3.resource('s3')
s3_photos_bucket = os.environ['PHOTOS_BUCKET']


def generate_color_scheme(filename):
    color_thief = ColorThief(filename)
    dominant_color = 'rgb' + str(color_thief.get_color(quality=1))
    colors = color_thief.get_palette(color_count=6)
    rgb_color_palette = []
    for color in colors:
        rgb_color_palette.append('rgb' + str(color))
    result = json.dumps({
        "dominant": dominant_color,
        "palette": rgb_color_palette
    })
    return result


def handler(event, context):
    # Process the S3 Upload
    s3_key = event['Records'][0]['s3']['object']['key']
    local_file_name = '/tmp/' + s3_key
    s3.Bucket(s3_photos_bucket).download_file(s3_key, local_file_name)
    color_scheme = generate_color_scheme(local_file_name)
    # Remove the object from tmp space
    if os.path.exists(local_file_name):
        os.remove(local_file_name)
    # Write the color scheme to the database
    item = {
        'pk': s3_key,
        'rgb': color_scheme,
    }
    table.put_item(Item=item)
