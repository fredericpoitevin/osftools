import json
import requests

def format_url(PROJECT_NODE, ID=None):
    """
    format_url(PROJECT_NODE, ID=None)
    """
    OSF_API_URL = 'https://api.osf.io/v2/'
    url = OSF_API_URL+'nodes/'+PROJECT_NODE+'/files/osfstorage/'
    if ID is not None:
        url = url+ID+'/'
    return url
    
def get_url(url):
    """
    get_url
    """
    return requests.get(url).json()
