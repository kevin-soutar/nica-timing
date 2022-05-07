from flask import Flask,request
from psycopg2 import connect
from secretinfo import database, ip, port, username, password
import psycopg2
import json

app = Flask(__name__)#remove this after development

con = connect(host=ip, port=port, database=database, user=username, password=password)

def format(input):
    output1 = input.replace('[','')
    output2 = output1.replace(']','')
    output3 = output2.replace('(','')
    output4 = output3.replace(')','')
    output5 = output4.replace(',','')
    output6 = output5.replace("'","")
    return output6

def import_team(conn, teamname):
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO team (team) VALUES (%s) ON CONFLICT DO NOTHING RETURNING team_id", (teamname,))
            for (id,) in cur:
                return str(id)
            cur.execute("SELECT team_id FROM team WHERE team = %s", (teamname,))
            (id,) = cur.fetchone()
            return str(id)

def import_racer(conn, nicaid,firstname,lastname,teamname):
        cur = conn.cursor()
        cur.execute(f'SELECT nica_id FROM racer WHERE nica_id = {nicaid};')
        nicaid_result = cur.fetchall()
        if nicaid_result == []:
                team_id = import_team(conn=conn,teamname=teamname)
                cur.execute("INSERT INTO racer(nica_id, first_name, last_name, team_id) VALUES (%s, %s, %s, %s)", (nicaid, firstname, lastname, team_id))
                conn.commit()

def import_category(conn, category):
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO category (category) VALUES (%s) ON CONFLICT DO NOTHING RETURNING category_id", (category,))
            for (id,) in cur:
                return str(id)
            cur.execute("SELECT category_id FROM category WHERE category = %s", (category,))
            (id,) = cur.fetchone()
            return str(id)

def import_race(conn,raceid,racename):
        cur = conn.cursor()
        cur.execute(f'SELECT race_result_id FROM race WHERE race_result_id = {raceid};')
        nicaid_result = cur.fetchall()
        if nicaid_result == []:
                cur.execute("INSERT INTO race(race_result_id,race_name) VALUES (%s, %s)", (raceid, racename))
                conn.commit()

def import_racer_id(conn,nicaid,bib,race,category):
        cur = conn.cursor()
        cur.execute(f'SELECT nica_id FROM racer_id WHERE nica_id = {nicaid};')
        nicaid_result = cur.fetchall()
        if nicaid_result == []:
                category_id = import_category(conn=conn,category=category)
                cur.execute("INSERT INTO racer_id(nica_id, bib_id, race_id, category_id) VALUES (%s, %s, %s, %s)", (nicaid, bib, race, category_id))
                conn.commit()

def format_time(time):
        time_interval = time.split(":")
        time_number =len(time_interval)
        if time_number == 2:
                time ="00:"+time
        return(time)

def import_race_info(conn,race,bib,laptimes,racestart):
        cur = conn.cursor()
        cur.execute(f'SELECT race_id,bib_id FROM racer_info WHERE race_id = {race} AND bib_id = {bib};')
        race_results = cur.fetchall()
        if race_results == []:
                cur.execute("INSERT INTO racer_info(race_id, bib_id,timestamp) VALUES (%s, %s,'now') RETURNING race_id,bib_id", (race, bib))
                conn.commit()
                race_results = cur.fetchall()
        if racestart == 1:
                cur.execute("UPDATE racer_info SET start_race = True WHERE race_id = %s AND bib_id =%s",(race, bib))
                conn.commit()
        if laptimes["lap1"] !="":
                cur.execute(f'SELECT lap1 FROM racer_info WHERE race_id = {race} AND bib_id = {bib};')
                lap1 = cur.fetchall()
                if lap1 != []:
                        cur.execute("UPDATE racer_info SET lap1 = %s, timestamp = 'now' WHERE race_id = %s AND bib_id =%s",(format_time(laptimes["lap1"]),race, bib))
                        conn.commit()
        if laptimes["lap2"] !="":
                cur.execute(f'SELECT lap2 FROM racer_info WHERE race_id = {race} AND bib_id = {bib};')
                lap1 = cur.fetchall()
                if lap1 != []:
                        cur.execute("UPDATE racer_info SET lap2 = %s, timestamp = 'now' WHERE race_id = %s AND bib_id =%s",(format_time(laptimes["lap2"]),race, bib))
                        conn.commit()       
        if laptimes["lap3"] !="":
                cur.execute(f'SELECT lap3 FROM racer_info WHERE race_id = {race} AND bib_id = {bib};')
                lap1 = cur.fetchall()
                if lap1 != []:
                        cur.execute("UPDATE racer_info SET lap3 = %s, timestamp = 'now' WHERE race_id = %s AND bib_id =%s",(format_time(laptimes["lap3"]),race, bib))
                        conn.commit()      
        if laptimes["lap4"] !="":
                cur.execute(f'SELECT lap4 FROM racer_info WHERE race_id = {race} AND bib_id = {bib};')
                lap1 = cur.fetchall()
                if lap1 != []:
                        cur.execute("UPDATE racer_info SET lap4 = %s, timestamp = 'now' WHERE race_id = %s AND bib_id =%s",(format_time(laptimes["lap4"]),race, bib))
                        conn.commit()
        if laptimes["lap5"] !="":
                cur.execute(f'SELECT lap5 FROM racer_info WHERE race_id = {race} AND bib_id = {bib};')
                lap1 = cur.fetchall()
                if lap1 != []:
                        cur.execute("UPDATE racer_info SET lap5 = %s, timestamp = 'now' WHERE race_id = %s AND bib_id =%s",(format_time(laptimes["lap5"]),race, bib))
                        conn.commit()

@app.route('/', methods = ['POST'])
def importInfo():
        request_json = request.json

        data =request_json["Values"]

        import_racer(conn=con,nicaid=data["NICAID"],firstname=data["FIRSTNAME"],lastname=data["LASTNAME"],teamname=data["CLUB"])
        import_racer_id(conn=con,nicaid=data["NICAID"],bib=data["DisplayBib"],race=request_json["EventID"],category=data["Wave"])
        import_race(conn=con,raceid=request_json["EventID"],racename=data["EVENT.NAME"])
        racelaps = {
                "lap1":data["Lap1"],
                "lap2":data["Lap2"],
                "lap3":data["Lap3"],
                "lap4":data["Lap4"],
                "lap5":data["Lap5"]
        }
        import_race_info(conn=con,race=request_json["EventID"],bib=data["DisplayBib"],laptimes=racelaps,racestart=int(data["StartCheckCalc"]))
        return ("info")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)