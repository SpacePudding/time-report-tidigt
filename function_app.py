import azure.functions as func
import logging
import workhours
import os
import requests
from datetime import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="timereport")
def TimeReport(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    time_report = workhours.obtain_workhours_this_month()

    timeReportConsid(time_report)

    return func.HttpResponse("TimeReport was a success!")


def timeReportConsid(time_report):

    session = requests.session()

    endpoint_current_time = 'https://tidig.consid.net/Time/TimeRangeData'
    endpoint_time_report = 'https://tidig.consid.net/Time/PostTimeForm'

    cookies = {
        '.AspNetCore.Cookies': 'chunks-2',
        '.AspNetCore.CookiesC1': os.environ["CHUNK1"],
        '.AspNetCore.CookiesC2': os.environ["CHUNK2"]
    }

    response = session.get(endpoint_current_time, params=obtain_current_time_endpoint_params(), cookies=cookies)
    current_work_data = response.json()

    for entry in time_report:
        for timeEntry in current_work_data['timeDateData']:
            if timeEntry['date'] == entry and timeEntry['reportedMinutesForTimeBank'] == 0:

                time_report_data = {
                    "dates": [entry], 
                    "articleId": 1, # Normal
                    "amountMinutes": time_report[entry], 
                    "customerId": 2080, # Borgwarner
                    "caseNumber": None,
                    "description": "Normal arbetstimmar hos kund",
                    "employeeChildren": [],
                    "operatingUnitId": 1152,
                    "customerManagerName": None,
                    "workPlaceId": "AtCustomer"}
                
                travel_report_data = {
                    "dates": [entry], 
                    "articleId": 23, # Normal
                    "amountMinutes": 60, 
                    "customerId": 2080, # Borgwarner
                    "caseNumber": None,
                    "description": None,
                    "employeeChildren": [],
                    "operatingUnitId": 1152,
                    "customerManagerName": None,
                    "workPlaceId": "AtCustomer"}

                session.post(endpoint_time_report, json=time_report_data, cookies=cookies)
                session.post(endpoint_time_report, json=travel_report_data, cookies=cookies)

def obtain_current_time_endpoint_params():

    current_date = datetime.now()

    # Get the first day of the current month
    first_day_of_month = current_date.replace(day=1).strftime('%Y-%m-%d')

    # Get the current date in yyyy-mm-dd format
    current_date_str = current_date.strftime('%Y-%m-%d')

    return {'startDate': f'{first_day_of_month}','endDate': f'{current_date_str}'}   