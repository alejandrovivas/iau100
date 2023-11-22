import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def download_images(html_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Try different encodings to read the HTML file
    encodings = ['utf-8', 'latin-1']  # Add more encodings if needed

    for encoding in encodings:
        try:
            with open(html_path, 'r', encoding=encoding) as file:
                html_content = file.read()
            break
        except UnicodeDecodeError:
            continue
    else:
        raise Exception(f"Unable to decode HTML file {html_path} with available encodings")

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find wow-image tags
    wow_images = soup.find_all('wow-image')

    # Download and save each image
    for wow_image in wow_images:

        # Get the source URL of the image
        image_uri = json.loads(wow_image.attrs['data-image-info'])['imageData']['uri']

        # Domain url
        domain = 'https://static.wixstatic.com/media/'

        # Create an absolute URL if the source is relative
        img_url = urljoin(domain, image_uri)

        # Make a request to download the image
        response = requests.get(img_url)

        # Extract the filename from the URL
        img_filename = os.path.join(output_folder, os.path.basename(img_url))

        # Save the image to the output folder
        with open(img_filename, 'wb') as img_file:
            img_file.write(response.content)

if __name__ == "__main__":
    # Specify the folder containing HTML files
    html_folder = 'html'

    # Specify the folder where images will be saved
    media_folder = 'media'

    # Iterate through HTML files in the specified folder
    for filename in os.listdir(html_folder):
        if filename.endswith('.html'):
            html_path = os.path.join(html_folder, filename)

            # Download images from the HTML file
            download_images(html_path, media_folder)

    print("Image download complete.")
