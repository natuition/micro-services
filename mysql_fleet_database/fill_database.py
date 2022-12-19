from glob import glob
import pymysql.cursors
import re
from urllib.parse import unquote
from datetime import datetime

sessions = glob("SN*/*", recursive=True)

db = pymysql.connect(host='127.0.0.1',
                     user='root',
                     password='my-secret-pw',
                     db='fleet')

try:

    for session in sessions:

        serial_number = session.split("/")[0]

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = f"SELECT * FROM Robots WHERE serial_number='{serial_number}';"
            cursor.execute(sql)
            if not cursor.fetchone():
                sql = f"INSERT INTO Robots (serial_number) VALUES ('{serial_number}');"
                cursor.execute(sql)
                db.commit()

        #session = f"{serial_number}/02-09-2022 07-50-59 251302"
        print(f"Treated session : '{session}'.")

        files = glob(f"{session}/*.txt")

        field = None
        field_name = None
        session_resume = None
        path_with_extract = None

        for file in files:

            if "field.txt" in file:
                with open(file) as file:
                    lines = file.readlines()
                    field = [eval(line) for line in lines]
            elif "field_name.txt" in file:
                with open(file) as file:
                    line = file.readline()
                    field_name = (unquote(line.replace("\n", "")))
            elif "session_resume.txt" in file:
                regex = r"(.*) : (.*)"
                with open(file) as file:
                    lines = file.readlines()
                    matches = re.finditer(regex, "".join(lines), re.MULTILINE)
                    matches = [[(eval(group) if "." in group or "(" in group or "[" in group or "{" in group else group) for group in match.groups()]
                               for match in matches]
                    session_resume = dict(zip([match[0] for match in matches], [
                        match[1] for match in matches]))

            elif "path_gps_with_extract.txt" in file:
                regex = r"^\[\s?(.*),\s?(.*),\s?'(.*)'\](.*)$"
                with open(file) as file:
                    lines = file.readlines()
                    matches = re.finditer(regex, "".join(lines), re.MULTILINE)
                    matches = [matche for matche in matches]
                    matches = matches[0:10]
                    path_with_extract = [[eval(group) if "." in group or len(group) == 1 else eval(group.split(" : ")[1]) if "{" in group else None for group in match.groups()]
                                         for match in matches]

        if field_name is None:
            field_name = "field"

        if session_resume is not None:
            # Create field
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = f"INSERT INTO Fields (label) VALUES ('{field_name}');"
                cursor.execute(sql)
                field_id = cursor.lastrowid

                corners_id = []
                for corner in field:
                    sql = f"INSERT INTO GPS_points (quality, latitude, longitude) VALUES (0, {corner[0]}, {corner[1]});"
                    cursor.execute(sql)
                    corners_id.append(cursor.lastrowid)

                for corner_id in corners_id:
                    sql = f"INSERT INTO Fields_corners (field_id, gps_point_id) VALUES ({field_id}, {corner_id});"
                    cursor.execute(sql)

            db.commit()

            # Create session
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                datetime_start = datetime.strptime(
                    session_resume["Start time"], '%d-%m-%Y %H-%M-%S %f')
                datetime_end = datetime.strptime(
                    session_resume["End time"], '%d-%m-%Y %H-%M-%S %f')

                sql = f"INSERT INTO Sessions (start_time, end_time, robot_serial_number, field_id, previous_sessions_id) VALUES ('{datetime_start.strftime('%Y-%m-%d %H:%M:%S')}', '{datetime_end.strftime('%Y-%m-%d %H:%M:%S')}', '{serial_number}', {field_id}, NULL);"
                cursor.execute(sql)
                session_id = cursor.lastrowid

            db.commit()

            # Create vesc_statistics
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                datetime_start = datetime.strptime(
                    session_resume["Start time"], '%d-%m-%Y %H-%M-%S %f')
                sql = f"INSERT INTO Vesc_statistics (session_id, voltage, timestamp) VALUES ({session_id}, {session_resume['Voltage at start']}, '{datetime_start.strftime('%Y-%m-%d %H:%M:%S')}');"
                cursor.execute(sql)

            db.commit()

            # Create path with extract
            with db.cursor(pymysql.cursors.DictCursor) as cursor:

                treated_plant_dict = {}

                for treated_plant in session_resume["Treated plant"]:
                    sql = f"SELECT id FROM Weed_types WHERE label='{treated_plant}';"
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    if not result:
                        sql = f"INSERT INTO Weed_types (label) VALUES ('{treated_plant}');"
                        cursor.execute(sql)
                        treated_plant_dict[treated_plant] = cursor.lastrowid
                    else:
                        treated_plant_dict[treated_plant] = result["id"]

                point_number = 0

                if path_with_extract is not None:

                    for path in path_with_extract:
                        sql = f"INSERT INTO GPS_points (latitude, longitude, quality) VALUES ({path[0]}, {path[1]}, {path[2]});"
                        cursor.execute(sql)

                        gps_point_id = cursor.lastrowid

                        sql = f"INSERT INTO Points_of_paths (point_number, session_id, gps_point_id) VALUES ({point_number}, {session_id}, {gps_point_id});"
                        cursor.execute(sql)

                        point_of_path_id = cursor.lastrowid

                        if path[3]:
                            for extracted_weed_name, extracted_weed_value in path[3].items():
                                if extracted_weed_name in treated_plant_dict:
                                    sql = f"INSERT INTO Extracted_weeds (point_of_path_id, weed_type_id, session_id, number) VALUES ({point_of_path_id}, {treated_plant_dict[extracted_weed_name]}, {session_id}, {extracted_weed_value});"
                                    cursor.execute(sql)

                        point_number += 1

            db.commit()

finally:
    db.close()
