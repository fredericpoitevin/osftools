import json

def display(json_data):
    print(json.dumps(json_data, indent=4))

def explore_data_structure(data):
    """
    explore_data_structure
    """
    if isinstance(data, (list,)):
        print('> input is a list of length {0}'.format(len(data)))
    elif isinstance(data, dict):
        print('> input is a dictionary, with the following keys: \n{0}'.format(data.keys()))
    else:
        print('> input is not a list nor a dictionary. We print it below:\n {0}'.format(data))
