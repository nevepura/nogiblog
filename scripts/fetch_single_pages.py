import os
import json
import requests
'''
Input: member_previews
Output: all the html pages of a member
'''

PAGES_FOLDER = 'pages'
MEMBER_NAME = 'shiori_kubo' #TODO edit
MEMBER_FOLDER = os.path.join(PAGES_FOLDER, MEMBER_NAME)
MEMBER_PREVIEWS = 'data/member_previews.json'
PREVIEW_FILE = 'preview.json'
BLOG_POST_FILE = 'blogpost.html'

def main():
    # open member_previews
    print(f'prefix is {MEMBER_FOLDER}')
    with open(MEMBER_PREVIEWS, 'r') as f:

        # for each preview from the file, create a folder named pages/<member>/<date>
        previews = json.load(f)
        for preview in previews:   
            datez = preview['datez']
            clean_date = datez.replace(' ', '_')

            blog_post_path = os.path.join(MEMBER_FOLDER, clean_date)
            print(f'New path for single blog post: {MEMBER_NAME}: {blog_post_path}')
            
            # If the path already exists, then the page has already been fetched. Then skip this fetching.
            if os.path.exists(blog_post_path):
                print(f'The current page {blog_post_path} is already present. Skipping current fetch. ')
                continue
            os.makedirs(blog_post_path, exist_ok=True)

            # save the preview file in the folder as preview.json
            preview_path = os.path.join(blog_post_path, PREVIEW_FILE)
            print(f'path to put preview: {preview_path}')
            with open(preview_path, 'w') as out:
                #print(f'preview: {preview}')
                json.dump(preview, out, indent=2)
            
            # use the link to fetch the html of the single page, and save it as page.html in the folder.
            page = requests.get(preview['page_link']).text
            
            blog_post_path = os.path.join(blog_post_path, BLOG_POST_FILE)
            print(f'path to put blog post: {blog_post_path}')
            with open(blog_post_path, 'w') as out: 
                out.write(page)

if __name__ == '__main__':
    main()