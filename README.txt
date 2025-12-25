Workflow: 
- move in the "scripts" folder
- in the "pages" folder, create a folder <name>_<lastname> of the new member
- edit the DASH_PAGE_URLS in fetch_previews.py
- run fetch_previews.py to generate the member_previews.json: it will be used by the next script 
- in fetch_single_pages.py, edit the MEMBER_NAME
- launch fetch_single_pages.py
- in extract_images.py, edit the directory variable with the member name
- launch extract_images.py