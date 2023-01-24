# KrakenFlex Back End Test - Christopher Higgs
## Quick Start
This program generates a list of outages for the site 'Norwich Pear Tree'.

To run (using Python 3.9 or above):
```
pip install -r requirements.txt
```
```
python outages.py
```
To run unit tests:
```
python -m unittest discover tests
```
## Overview
This program generates a list of valid outages for the site 'Norwich Pear Tree' by making HTTP requests to the API:

 `https://api.krakenflex.systems/interview-tests-mock-api/v1/{endpoint}`
 
 This list is then sent to the `POST /site-outages/norwich-pear-tree` endpoint.


When executed, this program will:

1. Retrieve all outages from the system from the `GET /outages` endpoint.

2. Retrieve site information from the `GET /site-info/norwich-pear-tree` endpoint.

3. Add valid outages whose IDs match devices in the site information to a list.

4. Send this list of outages to `POST /site-outages/norwich-pear-tree`.


**Outages that won't be sent:**
* Outages whose ID does not match an ID present in the site's list of devices.
* Outages that began before 00:00 on 01/01/2022

**Outages that will be included but will produce a warning:**
* Those whose begin or end dates are in the future
* Those whose end date is before the begin date


## Dependencies

* Python >= 3.9

Please install the following:
* [requests](https://pypi.org/project/requests/)
* [prettytable](https://pypi.org/project/prettytable/)

These can be installed with:
```
pip3 install -r requirements.txt
```

## How to Run
Execute the program by running the `outages.py` file:
```
python outages.py
```

## Testing
This program is accompanied by a suite of unit tests created using the `unittest` library.

Run all tests by executing:
```
python -m unittest discover tests
```

**OR** 

Run a specific test by executing:
```
python -m unittest tests/[test_file_name]
```
For example:
```
python -m unittest tests/test_make_request.py
```


## List of Test Cases

Below is a list of each test case:

### `test_check_date_warnings.py`

From a given begin and end date, this function produces a list of warnings.

| Test | Given | Expected Result | Passing?|
| ------- | ------- | ------- | ------- |
| _test_no_warnings_ | dates are valid | no warnings generated | ✅
| _test_negative_duration_ | end date comes before begin date | negative duration warning generated | ✅ 
| _test_future_begin_ | begin date occurs in the future | future begin date warning generated | ✅ 
| _test_future_end_ | end date occurs in the future | future end date warning generated  | ✅ 
| _test_all_warnings_ | both dates occur in the future + negative duration | all 3 possible warnings generated | ✅ 


### `test_generate_site_outages.py`

These tests verify the function of generate_site_outages(), which produces an enhanced list of outages based on site information and a list of all outages.

| Test | Given | Expected Result | Passing?|
| ------- | ------- | ------- | ------- |
| _test_site_outages_successful_only_ | valid outages only and valid site-info | valid outages are returned according to the schema | ✅
| _test_site_outages_successful_mix_ | several invalid outages, one valid outage | valid outage is returned according to the schema | ✅ 
| _test_site_outages_invalid_outage_dates_ | only outages with invalid dates | return an empty list | ✅ 
| _test_site_outages_no_site_outages_ | no outages relating to the given site | return an empty list  | ✅ 
| _test_site_outages_invalid_outages_mix_ | outages with invalid dates and outages not relating to the given site | return an empty list | ✅ 
| _test_site_outages_no_outages_ | no outages | return an empty list | ✅ 

### `test_make_request.py`

These tests verify the function of make_request(), which sends an HTTP request to the given API endpoint.

| Test | Given | Expected Result | Passing?|
| ------- | ------- | ------- | ------- |
| _test_status_code_200_get_ | status code 200 after GET request | data is returned and '200 OK' message printed | ✅
| _test_status_code_200_get_none_ | status code 200 after GET request but data is None | exit and print error | ✅ 
| _test_status_code_200_post_ | status code 200 after POST request | return status code 200 and print '200 OK' | ✅ 
| _test_status_code_client_error_403_get_ | status code 403 after GET request | exit interpreter and print error | ✅ 
| _test_status_code_client_error_403_post_ | status code 403 after POST request | exit interpreter and print error | ✅ 
| _test_status_code_client_error_404_get_ | status code 404 after GET request | exit interpreter and print error | ✅ 
| _test_status_code_client_error_404_post_ | status code 404 after POST request | exit interpreter and print error | ✅ 
| _test_status_code_client_error_429_get_ | status code 429 after GET request | exit interpreter and print error | ✅ 
| _test_status_code_client_error_429_post_ | status code 429 after POST request | exit interpreter and print error | ✅ 
| _test_status_code_server_error_500_post_ | status code 500 after GET request | retry 5 times, then exit interpreter and print error | ✅ 


**NB: The last test in test_make_request.py attempts retries and takes ~15 seconds**

## Thank you for your time!