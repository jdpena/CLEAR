import requests
import os
import gzip
import shutil
import argparse

def main(upload_url, file_path):
    # Server URL for uploading
    # File to be uploaded
    compressed_file_path = f"{file_path}.gz"

    # Compress the file using gzip
    with open(file_path, "rb") as f_in:
        with gzip.open(compressed_file_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    # POST request to upload the compressed file
    with open(compressed_file_path, "rb") as f:
        response = requests.post(upload_url, files={"file": (compressed_file_path, f, "application/gzip")})

        if response.status_code == 200:
            print(f"File uploaded successfully: {compressed_file_path}")
        else:
            print(f"Failed to upload file: {response.content}")

    # Optionally, remove the compressed file after upload if you want
    os.remove(compressed_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload a file to a server.')
    parser.add_argument('upload_url', type=str, help='The URL to which the file should be uploaded.')
    parser.add_argument('file_path', type=str, help='The path to the file that should be uploaded.')
    args = parser.parse_args()

    main(args.upload_url, args.file_path)
