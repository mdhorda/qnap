import json

def jsonprint(data):
    """
    Prettify JSON string.
    """
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
