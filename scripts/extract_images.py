'''
Extract images from single pages.
'''

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import shutil

# Config
directory = "pages/shiori_kubo"
IMAGES_SUBFOLDER = 'images'
BASE_URL = 'https://www.nogizaka46.com/'

import os

def list_folders_in_directory(directory_path):
    """
    Lists and prints the names of folders within a given directory.

    Args:
        directory_path (str): The path to the directory to scan.
    """
    try:
        # Ensure the directory exists
        if not os.path.exists(directory_path):
            print(f"Error: Directory '{directory_path}' not found.")
            return

        # Ensure it's a directory
        if not os.path.isdir(directory_path):
            print(f"Error: '{directory_path}' is not a directory.")
            return

        '''
        # List all items in the directory
        items = os.listdir(directory_path)

        # Filter for directories
        folders = [os.path.join(directory_path, item) for item in items if os.path.isdir(os.path.join(directory_path, item))]

        # Print the folder names
        for folder in folders:
            print(f'The current folder is: {folder}')
        '''
        download_images_from_blogposts(directory_path)


    except Exception as e:
        print(f"An error occurred: {e}")



def download_images_from_blogposts(base_directory):
    """
    Downloads images from blogpost.html files within subfolders of a given directory.

    Args:
        base_directory (str): The path to the directory containing subfolders.
    """
    try:
        if not os.path.exists(base_directory) or not os.path.isdir(base_directory):
            print(f"Error: Invalid directory path: {base_directory}")
            return

        for folder_name in os.listdir(base_directory):
            folder_path = os.path.join(base_directory, folder_name)
            images_path = os.path.join(folder_path, IMAGES_SUBFOLDER)
            
            delete_directory(images_path)
            os.makedirs(images_path, exist_ok=True)

            if os.path.isdir(folder_path):
                blogpost_path = os.path.join(folder_path, "blogpost.html")

                if os.path.exists(blogpost_path) and os.path.isfile(blogpost_path):
                    try:
                        with open(blogpost_path, "r", encoding="utf-8") as file:
                            html_content = file.read()

                        soup = BeautifulSoup(html_content, "html.parser")
                        edit_div = soup.find("div", class_="bd--edit")

                        if edit_div:
                            # Download images from <a> tags
                            for a_tag in edit_div.find_all("a"):
                                href = a_tag.get("href")
                                if href and href.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                                    download_image(href, images_path)

                            # Download images from <img> tags
                            for img_tag in edit_div.find_all("img"):
                                src = img_tag.get("src")
                                if src:
                                    full_src = urljoin(BASE_URL, src)
                                    download_image(full_src, images_path)

                    except Exception as e:
                        print(f"Error processing {blogpost_path}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

def delete_directory(directory_path):
    """
    Deletes a directory and its contents (subdirectories and files).

    Args:
        directory_path (str): The path to the directory to delete.
    """
    try:
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
            print(f"Directory '{directory_path}' and its contents deleted successfully.")
        else:
            print(f"Directory '{directory_path}' does not exist.")

    except OSError as e:
        print(f"Error deleting directory '{directory_path}': {e}")

def download_image(url, folder_path):
    """Downloads an image from a given URL to a specified folder."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        filename = os.path.basename(url)
        filepath = os.path.join(folder_path, filename)

        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
    except Exception as e:
        print(f"An error occurred during download: {e}")


def main():
    list_folders_in_directory(directory)


if __name__ == '__main__':
    main()