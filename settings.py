"""
File: settings.py
Description: stores local settings used by the qgis python plugin
Author: Robert Moerman
Contact: robert@afrispatial.co.za
Company: AfriSpatial
"""

import database_params

# Database settings
DATABASE_HOST = database_params.DATABASE_PARAMS["HOST"]
DATABASE_PORT = database_params.DATABASE_PARAMS["PORT"]
DATABASE_NAME = database_params.DATABASE_PARAMS["NAME"]
DATABASE_USER = database_params.DATABASE_PARAMS["USER"]
DATABASE_PASSWORD = database_params.DATABASE_PARAMS["PASSWORD"]
DATABASE_PARAMS = database_params.DATABASE_PARAMS
DATABASE_SCHEMA = "public"
DATABASE_LAYERS = {}

# Define database layers
DATABASE_LAYERS["BEACONS"] = {
    "SCHEMA":"public",
    "TABLE":"beacons",
    "NAME":"Beacon",
    "NAME_PLURAL":"Beacons",
    "PKEY":"gid", 
    "GEOM":"geom", 
    "GEOM_TYPE":"points",
    "SQL":{
        "SELECT":"SELECT beacon FROM beacons WHERE gid = %s;",
        "UNIQUE":"SELECT COUNT(*) FROM beacons WHERE %s = %s;",
        "EDIT":"SELECT {fields} FROM beacons WHERE gid = %s;",
        "DELETE":"DELETE FROM beacons WHERE gid = %s;",
        "INSERT":"INSERT INTO beacons({fields}) VALUES ({values}) RETURNING gid;",
        "UPDATE":"UPDATE beacons SET {set} WHERE {where};"
        }
}
DATABASE_LAYERS["PARCELS"] = {
    "SCHEMA":"public",
    "TABLE":"parcels",
    "NAME":"Parcel",
    "NAME_PLURAL":"Parcels",
    "PKEY":"id",
    "GEOM":"the_geom",
    "GEOM_TYPE":"polygons",
    "SQL":{
        "SELECT":"SELECT parcel_id FROM parcel_lookup WHERE id = %s;",
        "EDIT":"SELECT l.id, array_agg(s.gid) FROM ( SELECT b.gid, d.parcel_id FROM beacons b INNER JOIN parcel_def d ON d.beacon = b.beacon) s JOIN parcel_lookup l ON s.parcel_id = l.parcel_id WHERE l.id = %s GROUP BY l.id;",
        "AUTOCOMPLETE":"SELECT parcel_id FROM parcel_lookup WHERE available;",
        "UNIQUE":"SELECT COUNT(*) FROM parcel_lookup WHERE parcel_id = %s;",
        "AVAILABLE":"SELECT available FROM parcel_lookup WHERE parcel_id = %s;",
        "INSERT":"INSERT INTO parcel_def(parcel_id, beacon, sequence) VALUES (%s, %s, %s);",
        "DELETE":"DELETE FROM parcel_def WHERE parcel_id = %s;",
    }
}

# DB Triggers:
# - auto create parcel id in parcel_lookup if it does not exist on
# insert/update on parcel_def
# - auto update available field in parcel_lookup on insert/update/delete on
# parcel_def

DATABASE_LAYERS_ORDER = ["BEACONS", "PARCELS"]

# Define other sql commands
DATABASE_OTHER_SQL = {
    "AUTO_SURVEYPLAN":"SELECT array_agg(plan_no) FROM survey;",
    "AUTO_REFERENCEBEACON":"SELECT array_agg(beacon) FROM beacons WHERE beacon NOT IN (SELECT beacon_to FROM beardist WHERE beacon_to NOT IN (SELECT ref_beacon FROM survey));",
    "EXIST_REFERENCEBEACON":"SELECT ref_beacon FROM survey where plan_no = %s;",
    "EXIST_BEARDISTCHAINS":"SELECT bearing, distance, beacon_from, beacon_to FROM beardist WHERE plan_no = %s",
    "INDEX_REFERENCEBEACON":"SELECT i.column_index::integer FROM (SELECT row_number() over(ORDER BY c.ordinal_position) -1 as column_index, c.column_name FROM information_schema.columns c WHERE c.table_name = 'beacons' AND c.column_name NOT IN ('geom', 'gid') ORDER BY c.ordinal_position) as i WHERE i.column_name = 'beacon';"
}