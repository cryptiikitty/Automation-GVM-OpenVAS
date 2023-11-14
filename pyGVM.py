# Start - python3 pyGVM.py --hosts 127.0.0.1 --time 01:00
 
import datetime
import sys
from gvm.protocols.latest import Gmp
import gvm
from gvm.protocols.latest import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
import re
import argparse
import pytz
from icalendar import Calendar, Event
import calendar
 
 
def parse_args():
    parser = argparse.ArgumentParser(description='Python GVM schedule')
    parser.add_argument('--time', type=str, help='scan start time')
    parser.add_argument('--hosts', type=str, help='host, or hosts(coma separated')
    parser.add_argument('--name', type=str, help='ex: schedule_group_1')
    parser.add_argument('--day', type=str, help='ex: 2022-10-4')
    args = parser.parse_args()
 
    return args
 
def create_target(gmp, ipaddress, currentName, port_list_id):
    # create a unique name by adding the current datetime
    name = f"{currentName} {ipaddress}"
    myTest = gvm.protocols.gmpv214.AliveTest('Consider Alive')
    port_list_id = port_list_id
    ipaddress = ipaddress
    response = gmp.create_target(name, hosts=[ipaddress], ssh_credential_id='id', ssh_credential_port='22', alive_test=myTest, port_list_id=port_list_id)
    #print(response)
    start = response.find('id="') + len('id="')
    end = response.find('"/')
    id_response = response[start: end]
    print(response)
    return id_response
 
def create_schedule(gmp, time, day):
    time = time
    day = day
    time_for_schedule = time.split(":")
    day_for_schedule = day.split("-")
    cal = Calendar()
 
    cal.add('prodid', '-//Foo Bar//')
    cal.add('version', '2.0')

    event = Event()
    event.add('dtstamp', datetime.datetime.now(tz=pytz.UTC))
    event.add('dtstart', datetime.datetime(int(day_for_schedule[0]), int(day_for_schedule[1]), int(day_for_schedule[2]), int(time_for_schedule[0]), int(time_for_schedule[1]), tzinfo=pytz.utc))
 
    cal.add_component(event)
 
    response = gmp.create_schedule(
        name="Schedule_" + str(day_for_schedule[0]) + "/" + str(day_for_schedule[1]) + "/" + str(day_for_schedule[2]) + " " + str(time),
        icalendar=cal.to_ical(),
        timezone='UTC'
    )
    start = response.find('" id="') + len('" id="')
    end = response.find('"><')
    id_response = response[start: end]
    print(response)
    return id_response
 
 
 
def create_task(gmp, currentName, name_task, ipaddress, target_id, scan_config_id, scanner_id, schedule_id):
    name = f"{currentName}_{name_task}"
    response = gmp.create_task(
        name=name,
        config_id=scan_config_id,
        target_id=target_id,
        scanner_id=scanner_id,
        schedule_id=schedule_id,
        preferences={"max_checks": 1, "max_hosts": 10},
    )
    start = response.find('id="') + len('id="')
    end = response.find('"/')
    id_response = response[start: end]
    print(response)
    return id_response
 
 
def start_task(gmp, task_id):
    response = gmp.start_task(task_id)
    # the response is
    # <start_task_response><report_id>id</report_id></start_task_response>
    start = response.find('<report_id>') + len('<report_id>')
    end = response.find('</report_id>')
    id_response = response[start: end]
    return id_response
 
 
def main():
    connection =gvm.connections.TLSConnection(hostname='127.0.0.1')
    gmp = Gmp(connection)
    gmp.authenticate('username', 'pass') #use vault
    args = parse_args()
    day = args.day
    day_for_schedule = day.split("-")
    with gmp:
        #print(day_for_schedule[0])
        currentYear = int(day_for_schedule[0])
        currentMonth = int(day_for_schedule[1])
        #calendar.month_name[3]
        currentSeason = calendar.month_name[currentMonth]
         
        currentName = str(currentYear) + '_' + str(currentSeason)
         
        #args = parse_args()
        ipaddress = args.hosts
        time = args.time
        name_task = args.name
        #day = args.day
        port_list_id = 'id'
        target_id = create_target(gmp, ipaddress, currentName, port_list_id)
        schedule_id = create_schedule(gmp, time, day)
        full_and_fast_scan_config_id = "id"
        openvas_scanner_id = "id"
        task_id = create_task(
            gmp,
            currentName,
            name_task,
            ipaddress,
            target_id,
            full_and_fast_scan_config_id,
            openvas_scanner_id,
            schedule_id,
        )
        # may be useful
        #report_id = start_task(gmp, task_id)
        #print("Started scan of host: ", ipaddress)
        #print("Corresponding report ID is:", report_id)
 
 
if __name__ == "__main__":
    main()
