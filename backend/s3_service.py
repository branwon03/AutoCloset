import os
import uuid
import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

# Initialize S3 client using credentials automatically read from .env
s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    config=Config(signature_version="s3v4"),
)

def generate_presigned_upload_url(file_type: str) -> dict:
    """
    Generates a secure, temporary pre-signed URL allowing the
    client to PUT an image directly into S3.
    """
    file_extension = file_type.split("/")[-1]
    unique_key = f"clothing-uploads/{uuid.uuid4()}.{file_extension}"

    presigned_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": os.getenv("S3_BUCKET_NAME"),
            "Key": unique_key,
            "ContentType": file_type,
        },
        ExpiresIn=300,  # 5 minutes
    )

    return {
        "upload_url": presigned_url,
        "s3_key": unique_key,
        "public_url": f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{unique_key}",
    }