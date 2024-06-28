class agency():
    def __init__(self, agency_id: str, agency_name: str, agency_url: str, agency_timezone: str, agency_lang: str, agency_phone: str, agency_email: str, agency_fare_url: str):
        self.agency_id = agency_id
        self.agency_name = agency_name
        self.agency_url = agency_url
        self.agency_timezone = agency_timezone
        self.agency_lang = agency_lang
        self.agency_phone = agency_phone
        self.agency_email = agency_email
        self.agency_fare_url = agency_fare_url


class route():
    def __init__(self, route_id: str, agency_id: str, route_short_name: str, route_long_name: str, route_desc: str, route_type: int, route_url: str, route_color: str, route_text_color: str,route_sort_order: int):
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
    def __init__(self, route_id: str, service_id: str, trip_id: str, trip_headsign: str, trip_short_name: str, direction_id: int, block_id: str, shape_id: str, wheelchair_accessible: int, bikes_allowed: int):
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
    def __init__(self, service_id: str, monday: int, tuesday: int, wednesday: int, thursday: int, friday: int, saturday: int, sunday: int, start_date: str, end_date: str):
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
    def __init__(self, trip_id: str, arrival_time: str, departure_time: str, stop_id: str, stop_sequence: int, pickup_type: int, drop_off_type: int, local_zone_id: str, stop_headsign: str, timepoint: int):
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
    def __init__(self, stop_id: str,stop_code: str,stop_name: str,stop_desc: str,stop_lon: float,stop_lat: float,zone_id: str,stop_url: str,location_type: int,parent_station: str,stop_timezone: str,level_id: str,wheelchair_boarding: int,platform_code: str):
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
    def __init__(self, from_stop_id: str, to_stop_id: str, transfer_type: int, min_transfer_time: int):
        self.from_stop_id = from_stop_id
        self.to_stop_id = to_stop_id
        self.transfer_type = transfer_type
        self.min_transfer_time = min_transfer_time

class stop_extensions():
    def __init__(self,object_id: str,object_system: str,object_code: str):
        self.object_id = object_id
        self.object_system = object_system
        self.object_code = object_code

class pathways():
    def __init__(self, pathway_id: str, from_stop_id: str, to_stop_id: str, pathway_mode: int, is_bidirectional: int, length: float, traversal_time: int, stair_count: int, max_slope: float, min_width: float, signposted_as: str, reversed_signposted_as: str):
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


