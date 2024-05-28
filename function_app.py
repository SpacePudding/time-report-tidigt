import azure.functions as func
import logging
import os
import requests
from datetime import datetime


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="timereport")
def TimeReport(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Obtain date in yyyy-mm-dd format
    current_date = datetime.now().date()
    formatted_date = current_date.strftime("%Y-%m-%d")
    work_in_minutes = 480

    timeReportConsid(formatted_date, work_in_minutes)

    return func.HttpResponse("TimeReport was a success!")


def timeReportConsid(formatted_date, work_in_minutes):

    endpoint_time_report = 'https://tidig.consid.net/Time/PostTimeForm'

    cookies = {
        '.AspNetCore.Cookies': 'chunks-2',
        '.AspNetCore.CookiesC1': os.environ["CHUNK1"],
        '.AspNetCore.CookiesC2': os.environ["CHUNK2"]
    }

    time_report_data = {
        "dates": [formatted_date], 
        "articleId": 1, # Normal
        "amountMinutes": work_in_minutes, 
        "customerId": 2, # Consid AB
        "projectId": 3313, # Internt
        "activity": "Certifiering",
        "caseNumber": None,
        "description": "Normal working hours",
        "employeeChildren": [],
        "customerManagerName": None}

    requests.post(endpoint_time_report, json=time_report_data, cookies=cookies)