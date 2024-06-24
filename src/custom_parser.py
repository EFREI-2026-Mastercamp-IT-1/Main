import csv
from classes import *

def parse_agency():
    agency_list = []
    with open("data/agency.txt", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            agency_list.append(agency(
                row['agency_id'],
                row['agency_name'],
                row['agency_url'],
                row['agency_timezone'],
                row['agency_lang'],
                row['agency_phone'],
                row['agency_email'],
                row['agency_fare_url']
            ))
    return agency_list

def parse_routes():
    route_list = []
    with open("data/routes.txt", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            route_list.append(route(
                row['route_id'],
                row['agency_id'],
                row['route_short_name'],
                row['route_long_name'],
                row['route_desc'],
                row['route_type'],
                row['route_url'],
                row['route_color'],
                row['route_text_color'],
                row['route_sort_order']
            ))
    return route_list

def parse_trips():
    trip_list = []
    with open("data/trips.txt", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trip_list.append(trips(
                row['route_id'],
                row['service_id'],
                row['trip_id'],
                row['trip_headsign'],
                row['trip_short_name'],
                row['direction_id'],
                row['block_id'],
                row['shape_id'],
                row['wheelchair_accessible'],
                row['bikes_allowed']
            ))
    return trip_list

def parse_calendar():
    calendar_list = []
    with open("data/calendar.txt", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            calendar_list.append(calendar(
                row['service_id'],
                row['monday'],
                row['tuesday'],
                row['wednesday'],
                row['thursday'],
                row['friday'],
                row['saturday'],
                row['sunday'],
                row['start_date'],
                row['end_date']
            ))
    return calendar_list

def parse_calendar_dates():
    calendar_dates_list = []
    with open("data/calendar_dates.txt", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            calendar_dates_list.append(calendar_dates(
                row['service_id'],
                row['date'],
                row['exception_type']
            ))
    return calendar_dates_list

def parse_stop_times():
    stop_times_list = []
    with open("data/stop_times.txt", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stop_times_list.append(stop_times(
                row['trip_id'],
                row['arrival_time'],
                row['departure_time'],
                row['stop_id'],
                row['stop_sequence'],
                row['pickup_type'],
                row['drop_off_type'],
                row['local_zone_id'],
                row['stop_headsign'],
                row['timepoint']
            ))
    return stop_times_list

def parse_stops():
    stops_list = []
    with open("data/stops.txt", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stops_list.append(stops(
                row['stop_id'],
                row['stop_code'],
                row['stop_name'],
                row['stop_desc'],
                row['stop_lat'],
                row['stop_lon'],
                row['zone_id'],
                row['stop_url'],
                row['location_type'],
                row['parent_station'],
                row['stop_timezone'],
                row['wheelchair_boarding'],
                row['level_id'],
                row['platform_code']
            ))
    return stops_list

def parse_transfer():
    transfer_list = []
    with open("data/transfers.txt", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            transfer_list.append(transfer(
                row['from_stop_id'],
                row['to_stop_id'],
                row['transfer_type'],
                row['min_transfer_time']
            ))
    return transfer_list

def parse_stop_extensions():
    stop_extensions_list = []
    with open("data/stop_extensions.txt", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stop_extensions_list.append(stop_extensions(
                row['object_id'],
                row['object_system'],
                row['object_code']
            ))
    return stop_extensions_list

def parse_pathways():
    pathways_list = []
    with open("data/pathways.txt", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pathways_list.append(pathways(
                row['pathway_id'],
                row['from_stop_id'],
                row['to_stop_id'],
                row['pathway_mode'],
                row['is_bidirectional'],
                row['length'],
                row['traversal_time'],
                row['stair_count'],
                row['max_slope'],
                row['min_width'],
                row['signposted_as'],
                row['reversed_signposted_as']
            ))
    return pathways_list

def parse_all():
    return (
        parse_agency(),
        parse_routes(),
        parse_trips(),
        parse_calendar(),
        parse_calendar_dates(),
        parse_stop_times(),
        parse_stops(),
        parse_transfer(),
        parse_stop_extensions(),
        parse_pathways()
    )


parse_all()
