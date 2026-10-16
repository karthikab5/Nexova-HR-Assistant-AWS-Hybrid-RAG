
import os, json
from pathlib import Path
from dotenv import load_dotenv
import boto3

load_dotenv()

BUCKET = os.getenv("AWS_S3_BUCKET")
PREFIX = os.getenv("AWS_S3_PREFIX", "docs/")
REGION = os.getenv("AWS_REGION", "us-east-1")
DOCS_DIR = Path(__file__).parent  # same folder as this script

if not BUCKET:
    raise ValueError("Set AWS_S3_BUCKET in your .env file")

s3 = boto3.client("s3", region_name=REGION)

def upload_file(local_path: Path, s3_key: str):
    content_type = "application/json" if local_path.suffix == ".json" else "text/plain"
    s3.upload_file(
        str(local_path),
        BUCKET,
        s3_key,
        ExtraArgs={"ContentType": content_type}
    )
    print(f"  Uploaded: {s3_key}")

# Upload all .txt and .json docs (skip this script itself)
uploaded = 0
for f in sorted(DOCS_DIR.glob("*.txt")) + sorted(DOCS_DIR.glob("*.json")):
    if f.name == "upload_to_s3.py":
        continue
    s3_key = PREFIX + f.name
    upload_file(f, s3_key)
    uploaded += 1

print(f"\nDone. {uploaded} files uploaded to s3://{BUCKET}/{PREFIX}")
print(f"\nSet in your .env:")
print(f"  AWS_S3_BUCKET={BUCKET}")
print(f"  AWS_S3_PREFIX={PREFIX}")
