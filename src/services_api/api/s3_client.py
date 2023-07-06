import json

import boto3
import requests
from app.settings import S3_SERVICE_NAME, S3_URL, S3_REGION, S3_ACCESS_KEY, \
    S3_SECRET_ACCESS_KEY, S3_BUCKET, PATH_TO_RESULT_REPORTS, AWS_QUEUE_URL, YANDEX_SECRET_KEY, YANDEX_ACCESS_KEY


class S3Client:
    def __init__(self, queue=None):
        if queue is None:
            self.s3 = boto3.session.Session().client(
                service_name=S3_SERVICE_NAME,
                endpoint_url=S3_URL,
                region_name=S3_REGION,
                aws_access_key_id=S3_ACCESS_KEY,
                aws_secret_access_key=S3_SECRET_ACCESS_KEY
            )
        else:
            self.queue = queue
            self.client = boto3.client(
                service_name='sqs',
                endpoint_url=AWS_QUEUE_URL,
                region_name=S3_REGION,
                aws_access_key_id=YANDEX_ACCESS_KEY,
                aws_secret_access_key=YANDEX_SECRET_KEY
            )
        self.bucket = S3_BUCKET

    def get_zones_data(self):
        name = requests.get('https://functions.yandexcloud.net/d4efk2i3jsjuk1qg0fqc?&need_return=1').text
        result = self.s3.get_object(Bucket=self.bucket, Key='zone/Зоны' + name)['Body'].read().decode('utf8')
        self.delete(name)
        return json.loads(result)

    def delete(self, name):
        self.s3.delete_object(Bucket=self.bucket, Key='zone/Зоны' + name)

    def push_file(self, file_name, folder_name, upload_file_name):
        self.s3.upload_file(f'{PATH_TO_RESULT_REPORTS}{file_name}.xlsx',Bucket=S3_BUCKET, Key=f'parser/{folder_name}/{upload_file_name}.xlsx')

    def list_objects(self, folder_name):
        return self.s3.list_objects(Bucket=S3_BUCKET, Prefix=f'parser/{folder_name}/')

    def send(self, msg, delay=0):
        self.client.send_message(
            QueueUrl=self.queue,
            MessageBody=json.dumps(msg),
            DelaySeconds=delay,
        )
