import requests
import os
import gzip
import shutil
import argparse

def main(download_url, compressed_file_name):
    # Filename to be downloaded and uncompressed filename
    uncompressed_file_name = compressed_file_name.replace(".gz", "")  # Remove the ".gz" to get the uncompressed file name

    # Complete URL
    full_url = f"{download_url}/{compressed_file_name}"

    # Make GET request to download the file
    response = requests.get(full_url, stream=True)

    if response.status_code == 200:
        # Create a file to save the compressed content
        with open(compressed_file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File downloaded successfully: {compressed_file_name}")

        # Decompress the file
        with gzip.open(compressed_file_name, "rb") as f_in:
            with open(uncompressed_file_name, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"File decompressed successfully: {uncompressed_file_name}")

        # Delete the compressed file
        os.remove(compressed_file_name)
        print(f"Compressed file deleted: {compressed_file_name}")

    elif response.status_code == 404:
        print("File not found on the server.")
    else:
        print(f"Failed to download file: {response.content}")

if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Download and decompress a gzipped file.")
    parser.add_argument("download_url", type=str, help="The URL of the server where the file is to be downloaded.")
    parser.add_argument("compressed_file_name", type=str, help="The name of the compressed file to be downloaded.")

    # Parse command-line arguments
    args = parser.parse_args()

    # Server URL for downloading
    download_url = args.download_url  # URL taken from command-line arguments
    compressed_file_name = args.compressed_file_name  # Filename taken from command-line arguments

    main(download_url, compressed_file_name)
