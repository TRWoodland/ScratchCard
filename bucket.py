import boto3
import os
from exceptions import *
import logging

class Bucket:
    def __init__(self, file, bucket, target):
        self.file = file
        self.bucket = bucket
        self.target_file = target

        self.s3 = boto3.resource('s3')
        self.bucketUrl = str()

        if len(logging.getLogger().handlers) > 0:
            # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
            # `.basicConfig` does not execute. Thus we set the level directly.
            logging.getLogger().setLevel(logging.INFO)
        else:
            logging.basicConfig(level=logging.INFO)

    @staticmethod
    def log(cls, string):
        logging.error(string)
        print(string)

    def to_bucket(self):
        # Copy to S3 and return link
        try:
            # write file to S3             source, bucket, target
            self.s3.meta.client.upload_file(self.file, self.bucket, self.target_file)  # strips path from newFile
        except Exception as e:
            self.log(self, "Upload error: " + str(self.file) + " " + str(self.bucket) + " " + str(self.target_file) +
                     " " + str(e))
            raise InternalServerError(str(e))
            

    def create_presigned_url(self, expiration=3600):
        """Generate a preassigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Preassigned URL as string. If error, returns None.
        """

        # Generate a preassigned URL for the S3 object
        try:
            s3_client = boto3.client('s3')
            self.bucketUrl = s3_client.generate_presigned_url('get_object',
                                                              Params={'Bucket': self.bucket,
                                                                      'Key': self.file},
                                                              ExpiresIn=expiration)
            if not isinstance(self.bucketUrl, str):
                raise Exception('link is not a string')
            if self.bucketUrl is None:
                raise Exception('link is none')
        except Exception as e:
            self.log(self, "Upload error: " + str(self.file) + " " + str(self.bucket) + " " + str(self.target_file) +
                     str(e))
            raise InternalServerError(str(e))

        # The response contains the preassigned URL
        return self.bucketUrl
