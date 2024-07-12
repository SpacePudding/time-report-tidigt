from datetime import datetime

def extract_time_at_workplace(data):          
        monthly_time_json_table = {}

        for entry in data['timelineObjects']:
            if 'placeVisit' in entry:
                location_data = entry['placeVisit']['location']
                if 'name' in location_data and (location_data['name'] == "Consid AB" or location_data['name'] == "BorgWarner"):
                    duration = entry['placeVisit']['duration']
                    date = extract_date(duration)
                    if date in monthly_time_json_table:
                        monthly_time_json_table[date] += obtain_work_in_minutes(duration)
                    else:
                        monthly_time_json_table[date] = obtain_work_in_minutes(duration)

        monthly_worktime_json_table = subtract_lunch_time(monthly_time_json_table)
        monthly_rounded_worktime_json_table = round_workhours(monthly_worktime_json_table)

        return monthly_rounded_worktime_json_table

def subtract_lunch_time(monthly_time_json_table):

    minutes_eating_lunch = 30

    for entry in monthly_time_json_table:
        monthly_time_json_table[entry] = monthly_time_json_table[entry] - minutes_eating_lunch

    return monthly_time_json_table

def round_workhours(monthly_worktime_json_table):
    half_hour_in_minutes = 30

    for entry in monthly_worktime_json_table:
        time_to_add = half_hour_in_minutes - monthly_worktime_json_table[entry] % half_hour_in_minutes
        monthly_worktime_json_table[entry] = monthly_worktime_json_table[entry] + time_to_add

    return monthly_worktime_json_table

    
# Date is expressed in yyyy-mm-dd
def extract_date(duration):
    startTimestamp = duration['startTimestamp'] # Contains the format: yyyy-mm-ddThh:mm:ssZ
    return startTimestamp[:10]

def obtain_work_in_minutes(duration):

    seconds_per_minutes = 60

    # Timestamp in following format hh:mm:ss
    start_timestamp = duration['startTimestamp'][11:19] 
    end_timestamp = duration['endTimestamp'][11:19]

    start_time_object = datetime.strptime(start_timestamp, "%H:%M:%S")
    end_time_object = datetime.strptime(end_timestamp, "%H:%M:%S")
    time_difference = end_time_object - start_time_object

    return round(time_difference.total_seconds() / seconds_per_minutes)