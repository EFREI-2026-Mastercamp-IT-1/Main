from classes import *


def parse_agency():
    f = open("static/Version2/agency.txt", "r")
    agency_list = []
    for line in f:
        if line.startswith("agency_id"):
            continue
        else:
            agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_email,agency_fare_url = line.strip().split(",")
            agency_list.append(agency(agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_email,agency_fare_url))
    f.close()
    return agency_list

def parse_routes():
    f = open("static/Version2/routes.txt", "r")
    route_list = []
    for line in f:
        if line.startswith("route_id"):
            continue
        else:
            route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color,route_sort_order = line.strip().split(",")
            route_list.append(route(route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color,route_sort_order))
    f.close()
    return route_list

def parse_trips():
    f = open("static/Version2/trips.txt", "r")
    trip_list = []
    for line in f:
        if line.startswith("route_id"):
            continue
        else:
            route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,block_id,shape_id,wheelchair_accessible,bikes_allowed = line.strip().split(",")
            trip_list.append(trips(route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,block_id,shape_id,wheelchair_accessible,bikes_allowed))
    f.close()
    return trip_list

def parse_calendar():
    f = open("static/Version2/calendar.txt", "r")
    calendar_list = []
    for line in f:
        if line.startswith("service_id"):
            continue
        else:
            service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date = line.strip().split(",")
            calendar_list.append(calendar(service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date))
    f.close()
    return calendar_list

def parse_calendar_dates():
    f = open("static/Version2/calendar_dates.txt", "r")
    calendar_dates_list = []
    for line in f:
        if line.startswith("service_id"):
            continue
        else:
            service_id,date,exception_type = line.strip().split(",")
            calendar_dates_list.append(calendar_dates(service_id,date,exception_type))
    f.close()
    return calendar_dates_list

def parse_stop_times():
    f = open("static/Version2/stop_times.txt", "r")
    stop_times_list = []
    for line in f:
        if line.startswith("trip_id"):
            continue
        else:
            trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,local_zone_id,stop_headsign,timepoint = line.strip().split(",")
            stop_times_list.append(stop_times(trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,local_zone_id,stop_headsign,timepoint))
    f.close()
    return stop_times_list

def parse_stops():
    f = open("static/Version2/stops.txt", "r")
    stops_list = []
    for line in f:
        if line.startswith("stop_id"):
            continue
        else:
            stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station,stop_timezone,wheelchair_boarding = line.strip().split(",")
            stops_list.append(stops(stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station,stop_timezone,wheelchair_boarding))
    f.close()
    return stops_list

def parse_transfer():
    f = open("static/Version2/transfers.txt", "r")
    transfer_list = []
    for line in f:
        if line.startswith("from_stop_id"):
            continue
        else:
            from_stop_id,to_stop_id,transfer_type,min_transfer_time = line.strip().split(",")
            transfer_list.append(transfer(from_stop_id,to_stop_id,transfer_type,min_transfer_time))
    f.close()
    return transfer_list

def parse_stop_extensions():
    f = open("static/Version2/stop_extensions.txt", "r")
    stop_extensions_list = []
    for line in f:
        if line.startswith("object_id"):
            continue
        else:
            object_id,object_system,object_code = line.strip().split(",")
            stop_extensions_list.append(stop_extensions(object_id,object_system,object_code))
    f.close()
    return stop_extensions_list

def parse_pathways():
    f = open("static/Version2/pathways.txt", "r")
    pathways_list = []
    for line in f:
        if line.startswith("from_stop_id"):
            continue
        else:
            from_stop_id,to_stop_id,pathway_mode,is_bidirectional,length,traversal_time,stair_count,max_slope,min_width,signposted_as,reversed_signposted_as = line.strip().split(",")
            pathways_list.append(pathways(from_stop_id,to_stop_id,pathway_mode,is_bidirectional,length,traversal_time,stair_count,max_slope,min_width,signposted_as,reversed_signposted_as))
    f.close()
    return pathways_list

def parse_all():
    return parse_agency(),parse_routes(),parse_trips(),parse_calendar(),parse_calendar_dates(),parse_stop_times(),parse_stops(),parse_transfer(),parse_stop_extensions(),parse_pathways()
