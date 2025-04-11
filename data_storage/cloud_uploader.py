import argparse
import boto3
from google.cloud import storage


def upload_to_aws(input_file, bucket_name):
    try:
        s3 = boto3.client('s3')
        s3.upload_file(input_file, bucket_name, input_file.split('/')[-1])
        print(f"文件 {input_file} 已成功上传到 AWS S3 存储桶 {bucket_name}")
    except Exception as e:
        print(f"上传到 AWS S3 时出现错误: {e}")


def upload_to_gcp(input_file, bucket_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(input_file.split('/')[-1])
        blob.upload_from_filename(input_file)
        print(f"文件 {input_file} 已成功上传到 Google Cloud Storage 存储桶 {bucket_name}")
    except Exception as e:
        print(f"上传到 Google Cloud Storage 时出现错误: {e}")


def upload_to_cloud(input_file, cloud_provider, bucket_name):
    if cloud_provider == 'aws':
        upload_to_aws(input_file, bucket_name)
    elif cloud_provider == 'gcp':
        upload_to_gcp(input_file, bucket_name)
    else:
        print("不支持的云存储提供商，请使用 'aws' 或 'gcp'。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='数据上传到云存储脚本')
    parser.add_argument('--input_file', required=True, help='要上传的数据文件路径。')
    parser.add_argument('--cloud_provider', required=True, help='云存储提供商（如 aws、gcp 等）。')
    parser.add_argument('--bucket_name', required=True, help='云存储桶名称。')
    args = parser.parse_args()

    input_file = args.input_file
    cloud_provider = args.cloud_provider
    bucket_name = args.bucket_name

    upload_to_cloud(input_file, cloud_provider, bucket_name)
