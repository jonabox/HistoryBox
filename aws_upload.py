import os
import boto3, botocore

S3_BUCKET = 'greenboxprofiles'
S3_KEY = 'AKIAJ6L7AZIEIUL52BDQ'
S3_SECRET =  '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'
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET) #'US East'

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:

        print("Something Happened: ", e)
        return e

    return "{}{}".format(S3_LOCATION, file.filename)
