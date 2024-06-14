class agency():
    def __init__(self, agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_email,agency_fare_url):
        self.agency_id = agency_id
        self.agency_name = agency_name
        self.agency_url = agency_url
        self.agency_timezone = agency_timezone
        self.agency_lang = agency_lang
        self.agency_phone = agency_phone
        self.agency_email = agency_email
        self.agency_fare_url = agency_fare_url

class route():
    def __init__(self, route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color,route_sort_order):
        self.route_id = route_id
        self.agency_id = agency_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.route_desc = route_desc
        self.route_type = route_type
        self.route_url = route_url
        self.route_color = route_color
        self.route_text_color = route_text_color
        self.route_sort_order = route_sort_order

class trips():
    def __init__(self, route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,block_id,shape_id,wheelchair_accessible,bikes_allowed):
        self.route_id = route_id
        self.service_id = service_id
        self.trip_id = trip_id
        self.trip_headsign = trip_headsign
        self.trip_short_name = trip_short_name
        self.direction_id = direction_id
        self.block_id = block_id
        self.shape_id = shape_id
        self.wheelchair_accessible = wheelchair_accessible
        self.bikes_allowed = bikes_allowed

class calendar():
    def __init__(self, service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date):
        self.service_id = service_id
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday
        self.start_date = start_date
        self.end_date = end_date

class calendar_dates():
    def __init__(self, service_id, date, exception_type):
        self.service_id = service_id
        self.date = date
        self.exception_type = exception_type

class stop_times():
    def __init__(self, trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,local_zone_id,stop_headsign,timepoint):
        self.trip_id = trip_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_id = stop_id
        self.stop_sequence = stop_sequence
        self.pickup_type = pickup_type
        self.drop_off_type = drop_off_type
        self.local_zone_id = local_zone_id
        self.stop_headsign = stop_headsign
        self.timepoint = timepoint

class stops():
    def __init__(self, stop_id,stop_code,stop_name,stop_desc,stop_lon,stop_lat,zone_id,stop_url,location_type,parent_station,stop_timezone,level_id,wheelchair_boarding,platform_code):
        self.stop_id = stop_id
        self.stop_code = stop_code
        self.stop_name = stop_name
        self.stop_desc = stop_desc
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon
        self.zone_id = zone_id
        self.stop_url = stop_url
        self.location_type = location_type
        self.parent_station = parent_station
        self.stop_timezone = stop_timezone
        self.wheelchair_boarding = wheelchair_boarding
        self.level_id = level_id
        self.platform_code = platform_code

class transfer():
    def __init__(self, from_stop_id,to_stop_id,transfer_type,min_transfer_time):
        self.from_stop_id = from_stop_id
        self.to_stop_id = to_stop_id
        self.transfer_type = transfer_type
        self.min_transfer_time = min_transfer_time

class stop_extensions():
    def __init__(self,object_id,object_system,object_code):
        self.object_id = object_id
        self.object_system = object_system
        self.object_code = object_code

class pathways():
    def __init__(self,pathway_id,from_stop_id,to_stop_id,pathway_mode,is_bidirectional,length,traversal_time,stair_count,max_slope,min_width,signposted_as,reversed_signposted_as):
        self.pathway_id = pathway_id
        self.from_stop_id = from_stop_id
        self.to_stop_id = to_stop_id
        self.pathway_mode = pathway_mode
        self.is_bidirectional = is_bidirectional
        self.length = length
        self.traversal_time = traversal_time
        self.stair_count = stair_count
        self.max_slope = max_slope
        self.min_width = min_width
        self.signposted_as = signposted_as
        self.reversed_signposted_as = reversed_signposted_as




class Node:
    def __init__(self, id, label, x, y):
        self.id = id
        self.label = label
        self.x = x
        self.y = y
        self.size = 5.0
        self.color = "#000000"

class Edge:
    def __init__(self, source, target,time):
        self.source = source
        self.target = target
        self.time = time
        self.size = 5.0
        self.color = "#000000"
