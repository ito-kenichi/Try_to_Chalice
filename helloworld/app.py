from chalice import Chalice
import json
import boto3
from botocore.exceptions import ClientError
from chalice import NotFoundError

app = Chalice(app_name='helloworld')
app.debug = True

@app.route('/', methods=['POST'], cors=True)
def index():
    return {'hello': 'world'}

S3 = boto3.client('s3', region_name='us-west-2')
BUCKET = 'chalice-test-myapp-bucket'


@app.route('/objects/{key}', methods=['GET', 'PUT', 'POST'], cors=True)
def s3objects(key):
    request = app.current_request
    if request.method == 'PUT' or request.method == 'POST':
        S3.put_object(Bucket=BUCKET, Key=key,
                      Body=json.dumps(request.json_body))
    elif request.method == 'GET':
        try:
            response = S3.get_object(Bucket=BUCKET, Key=key)
            return json.loads(response['Body'].read())
        except ClientError as e:
            raise NotFoundError(key)