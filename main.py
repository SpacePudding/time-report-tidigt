import requests
from datetime import datetime
import os

def main():
    # TODO: Use a function to calculate how many mintues I've worked
    work_hours_in_minutes = 480
    timeReport(work_hours_in_minutes)


def timeReport(work_hours_in_minutes):

    endpoint_time_report = 'https://tidig.consid.net/Time/PostTimeForm'


    cookies = {
        '.AspNetCore.Cookies': 'chunks-2',
        '.AspNetCore.CookiesC1': os.environ["CHUNKS1"],
        '.AspNetCore.CookiesC2': os.environ["CHUNKS2"]
    }

    # Obtain date in yyyy-mm-dd format
    current_date = datetime.now().date()
    formatted_date = current_date.strftime("%Y-%m-%d")

    time_report_data = {
        "dates": [formatted_date], 
        "articleId": 1, # Normal
        "amountMinutes": work_hours_in_minutes, 
        "customerId": 2, # Consid AB
        "projectId": 3313, # Internt
        "activity": "Certifiering",
        "caseNumber": None,
        "description": "Normal working hours",
        "employeeChildren": [],
        "customerManagerName": None}

    response = requests.post(endpoint_time_report, json=time_report_data, cookies=cookies)

if __name__ == '__main__':
    main()
