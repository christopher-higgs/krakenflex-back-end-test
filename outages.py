import requests
import sys
import time
from datetime import datetime
from http import HTTPStatus
from prettytable import PrettyTable

def make_request(type, endpoint, headers, data=None, retries=0):
    """ Make an HTTP request to the krakenflex API.
    
    Keyword arguments:
    type     -- [str] Request type. 'GET' and 'POST' only.
    endpoint -- [str] API endpoint. e.g. 'outages'
    headers  -- [dict] HTTP headers to be attached to the request.
    data     -- [list(dict)] (Optional) Payload to be sent to the server. Only used for POST requests (defaults to None)
    retries  -- [int] (Optional) Recursion counter. Used to count retry attempts when status code 500 is received.
    """
    url = f'https://api.krakenflex.systems/interview-tests-mock-api/v1/{endpoint}'
    if type == 'GET':
        r = requests.get(url, headers=headers)
    elif type == 'POST':
        r = requests.post(url, headers=headers, json=data)
    else:
        print(f'Invalid request type \'{type}\'')
        sys.exit(1)
    phrase = HTTPStatus(r.status_code).phrase
    if r.status_code == 200:
        print(f'{r.status_code} {phrase}')
        if type == "GET" and r.json(): # avoid returning None
            return r.json()
        elif r.json() == None:
            print(f'Server returned 200 but no valid data')
            sys.exit(1)
        else:
            return r.status_code
    elif r.status_code == 500 and retries < 5:
        print(f'Server returned {r.status_code}: {phrase}... Retrying... {retries+1}/5')
        time.sleep(retries*1.5)
        retries+=1
        make_request(type,endpoint,headers,data,retries)
    else:
        print(f'Error ({r.status_code}: {phrase})')
        sys.exit(1)

def generate_site_outages(outages, site, earliest):
    """ Generate a list of outages for a site.
    
    Keyword arguments:
    outages  -- a list of outages (dict) from 'GET /outages'
    site     -- site information from 'GET /site-info/norwich-pear-tree'
    earliest -- the earliest date an outage is deemed valid (ISO 8601 form) 
               e.g. '2022-01-01T00:00:00.000Z'
    """
    site_outages = []
    for outage in outages:
        if outage["begin"] < earliest:
            continue
        for device in site["devices"]:
            if outage["id"] == device["id"]:
                site_outages.append({
                    "id": outage["id"],
                    "name": device["name"],
                    "begin": outage["begin"],
                    "end": outage["end"]
                    })
    return site_outages

def check_date_warnings(begin, end):
    """ Check site outages for dates that appear invalid.
    
    Keyword arguments:
    begin  -- [datetime] outage's begin date
    end    -- [datetime] outage's end date
    """
    warnings = []
    now = datetime.now()
    if end < begin:
        warnings.append('Negative duration detected\n')
    if begin > now:
        warnings.append('Outage has future begin date\n')
    if end > now:
        warnings.append('Outage has future end date\n')
    return warnings

def generate_pretty_table(site_outages):
    """ Return PrettyTable showing site outages + warnings

    Keyword arguments:
    site_outages  -- [list(dict)] list of outages for a site
    """
    table = PrettyTable()
    table.field_names = ['Device Name', 'Begin', 'End', 'Duration', '']

    for outage in site_outages:
        begin = datetime.strptime(outage["begin"], '%Y-%m-%dT%H:%M:%S.%fZ') # string to datetime object
        end = datetime.strptime(outage["end"], '%Y-%m-%dT%H:%M:%S.%fZ')
        duration = end - begin
        warnings = check_date_warnings(begin, end) # generate any warnings
        warning_str = 'WARNING: \n' if len(warnings) > 0 else ''
        for warning in warnings:
            warning_str+=warning
        begin_str = begin.strftime('%Y-%m-%d %H:%M:%S') # format date nicely
        end_str = end.strftime('%Y-%m-%d %H:%M:%S')
        table.add_row([outage["name"], begin_str, end_str, str(duration)[:-7], warning_str])
    table.align = 'l' # align columns left
    table.sortby = 'Device Name'
    return table

def main():
    with open('./api-key.txt') as f:
        key = f.read() # get API key from file
    headers = {'x-api-key': key}

    site = make_request('GET', 'site-info/norwich-pear-tree', headers) # get site info
    outages = make_request('GET', 'outages', headers) # get all outages

    earliest = '2022-01-01T00:00:00.000Z'
    site_outages = generate_site_outages(outages, site, earliest) # create site outages list (after 2022-01-01)

    make_request('POST', 'site-outages/norwich-pear-tree', headers, site_outages)
    print(generate_pretty_table(site_outages))

if __name__ == "__main__":
    main()