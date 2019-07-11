import os
import json
import requests
import numpy as np
import urllib.request

def download_all_files(PROJECT_URL, PROJECT_DIR, fileidlist, filenamelist):
    """
    """
    if not os.path.exists(PROJECT_DIR):
        os.makedirs(PROJECT_DIR)
    for i in np.arange(len(filenamelist)):
        url  = PROJECT_URL+fileidlist[i]
        path = PROJECT_DIR+filenamelist[i] 
        print('... Downloading {0} to {1} ...'.format(url, path))
        urllib.request.urlretrieve(url, path)

def list_all_files(url, ext=None, npages_max=-1):
    """
    list_all_files(url, ext=None)
    """
    # Initialize the lists
    names, ids = url_to_idlist(url, kind='file', ext=ext)
    print('Initial length of hit list is {0}'.format(len(ids)))
    # How many pages do we need to go through ?
    npages = url_to_npages(url)
    if(npages_max > 0):
        if(npages_max < npages):
            npages=npages_max
    print('npages = {0}'.format(npages))
    # Let's skim through them and add our files
    for ipage in np.arange(2,npages+1):
        newnames, newids = url_to_idlist(url+'/?page='+str(ipage), kind='file', ext=ext)
        names.extend(newnames)
        ids.extend(newids)
    print('Final length of hit list is {0}'.format(len(ids)))
    return names, ids

def url_to_idlist(url, kind='all', ext=None):
    """
    url_to_idlist(url, kind='folder'):
    List all files and/or directories at given addresses. Return names and IDs.
    """
    data = get_url(url)['data']
    namelist = []
    idlist   = []
    if isinstance(data, list):
        for i in np.arange(len(data)):
            if isinstance(data[i], dict):
                elt_kind = data[i]['attributes']['kind']
                elt_name = data[i]['attributes']['name']
                elt_id   = data[i]['id']
                add=False
                if((elt_kind == 'folder' and kind != 'file') or (elt_kind == 'file' and kind != 'folder')):
                    add = True
                    if(kind == 'file' and (ext is not None)):
                        elt_ext = elt_name.split(".")[-1]
                        if(elt_ext != ext):
                            add = False
                if add:
                    namelist.append(elt_name)
                    idlist.append(elt_id)
    else:
        print('input is not a list... check it up!')
    return namelist, idlist
    
def url_to_npages(url):
    """
    url_to_npages
    """
    npages = get_url(url)['links']['last'].split("?page=")[1]
    return int(npages)

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
