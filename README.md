## Description

Automate quarterly PCI DSS scans with greenbone vulnerability management(OpenVAS). The script was written for this version - https://github.com/Secure-Compliance-Solutions-LLC/GVM-Docker

But it can be adapted to any other. The script also contains sending messages to the eXpress messenger, feel free to replace and adjust the scripts to suit you

## Contains:
1. main.py - sets the scanning date
2. start.py - sends data to pyGVM
3. pyGVM.py - creates a scan + scheduler
4. target.xlsx - targets
5. gvm_to_express.py - bot for alerts

## How to Run:
1. Prepare the target.xlsx spreadsheet*
2. Run python3 main.py (on the workstation)
3. Check the received host lists using Notepad++ (comma-separated)
4. Copy the spreadsheet to the container*
6. Run python3 start.py
7. Run python3 gvm_to_express.py

### Example target.xlsx:
1 | schedule_group_25 | 127.0.0.1,127.0.02 | 01:00 | 08:00 |

```bash
Columns:
1 - queue (if there are 2+ scans in one day, they have the same value; for the next day, the value increases by 1)
2 - scheduler group name
3 - IP list. IMPORTANT: IPs are listed without spaces, separated by commas. The column width should be maximum (255)
4 - start time of the scan
5 - end time of the scan
6 - do not fill, the script will assign the scan date here

COLUMNS 1-5 MUST BE FILLED IN, OTHERWISE THERE WILL BE ERRORS

```

### Moving target.xlsx to the container:

```bash
cp -ap target.xlsx /../storage/postgres-db/target.xlsx
docker exec -it 460 /bin/bash
cd /home/pyscript/
cp -ap /opt/database/target.xlsx target.xlsx
```

The script integrates with Vault for secure storage of sensitive data, such as authentication details. Ensure proper Vault configuration and setup of environment variables for secure handling of credentials.
