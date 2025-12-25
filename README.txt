# Workflow
## Configuration
- in config.py, edit the MEMBER_NAME
- in config.py edit the DASH_PAGE_URLS
- in the "pages" folder, create a folder <name>_<lastname> of the new member

## Execution
- move in the "scripts" folder
- run fetch_previews.py to generate the member_previews.json: it will be used by the next script 
- launch fetch_single_pages.py
- launch extract_images.py