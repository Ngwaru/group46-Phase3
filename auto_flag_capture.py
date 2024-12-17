import re
import sys
import subprocess
from time import sleep 
import csv
import requests 
from bs4 import BeautifulSoup
import pandas as pd


groups = [' nharrand/intsec-group-1:latest',
 ' nharrand/intsec-group-2:latest',
 ' nharrand/intsec-group-3:latest',
 ' noorabh/passoire_group4_hardened:v1',
 ' kivayuri/group5_phase2:v5',
 ' 0x00a0/passoire_group06:latest',
 ' nharrand/intsec-group-7:latest',
 ' laldemar/group8_hardend:latest',
 ' nharrand/intsec-group-9:latest',
 ' amanjuman/passoire:final',
 ' nharrand/intsec-group-11:latest',
 ' qdbjo/group_submission:latest',
 ' nharrand/intsec-group-14:latest',
 ' nharrand/intsec-group-20:latest',
 ' nharrand/intsec-group-21:latest',
 ' heishi99/passoire:V3.2',
 ' erangis/group24:3.0',
 ' nharrand/intsec-group-25:latest',
 ' nharrand/intsec-group-27:latest',
 ' hagendaz123/group28:finalv2',
 ' nharrand/intsec-group-30:latest',
 ' intsecproject/passoire-final:v2',
 ' udeshim/group_32_intsec:final-tag',
 ' nharrand/intsec-group-33:latest',
 ' nharrand/intsec-group-34:latest',
 ' nharrand/intsec-group-35:latest',
 ' qtung/g36-passoire-0512-v4:latest',
 ' nharrand/intsec-group-38:latest',
 ' kentfre/group40_passoire:latest',
 ' jonybotto/passoire:final',
 ' toxillo/intsec_passoire:v1',
 ' nharrand/intsec-group-44:latest',
 ' intsecgroup48/passoire-ready:latest',
 ' denny1024/is-grp50:v2.5.5',
 ' niu1028/sthlm-insec-ht2024-grp52:latest',
 ' nharrand/intsec-group-56:latest',
 ' balkongen/passoire-improved:latest',
 ' qlvin/grupp64:latest',
 ' nharrand/intsec-group-66:latest',
 ' helss/passoire:patch_17',
 ' victorlejon/intsec_defense:latest']


def get_flag_4(group_name, base_url):
    r = requests.get(base_url)
    content = BeautifulSoup(r.text, 'html.parser')
    #print(content.prettify())

    pattern = r"(flag_4 is .{40})"
    all_divs = content.get_text()
    captured_flag = "Not Found"
    flag_name = 4

    match = re.search(pattern, all_divs)
    if match:
        captured_flag = match.group(1)[-41:]
        
        with open("new_captured_flags_only.csv", "a") as f:
            thewriter = csv.writer(f)
            thewriter.writerow([group_name, flag_name, captured_flag])
        
    if captured_flag == "Not Found":
        print(f'Failed to get flag {flag_name}')
        with open("new_captured_flags_only.csv", "a") as f:
            thewriter = csv.writer(f)
            thewriter.writerow([group_name, flag_name, captured_flag])
    return r.ok


def get_flag_with_request(group_name, complete_ip):
        if complete_ip.endswith('flag_6'):
            flag_name = 6
        elif complete_ip.endswith('secret') :
            flag_name = 7
        else:
            flag_name = 3
        try:
            r = requests.get(complete_ip)
            if r.ok:
                content = BeautifulSoup(r.text, 'html.parser')
                pattern = r"(flag_. is .{40})"
                #all_pre = content.find_all('pre')
                string_text = content.get_text()
                captured_flag = "Not Found"
                
                match = re.search(pattern, string_text)
                if match:
                    captured_flag = match.group(1)[-41:]
                    
                with open("new_captured_flags_only.csv", "a") as f:
                    thewriter = csv.writer(f)
                    thewriter.writerow([group_name, flag_name, captured_flag])
        except:
            print(f'Failed to retrive flag {flag_name}')





def start_scrapping(group_name):
    group_ips = ['http://localhost:8080/passoire/']
    flag_specific_ip_endings = [ 'flag_3', 'uploads/flag_6', 'uploads/secret']
    for group_ip in group_ips: 
        base_url = group_ip+'index.php'
        try:
            get_flag_4(group_name, base_url)
        except:
            print("Failed To Scrape Flag 4")
    
        sleep(0.5)
        #a,b = pt.locateCenterOnScreen("img\\chrome.png", confidence=0.85)
        #pt.moveTo(a,b)
        #pt.click()
        for flag_specific_ip_ending in flag_specific_ip_endings:
            complete_ip = group_ip+flag_specific_ip_ending
            get_flag_with_request(group_name, complete_ip)
            sleep(0.1)


docker_group_commands = []
first_command = "docker run -d -p 8080:80 -p 3002:3002 -p 2222:22 -e HOST=localhost nharrand/intsec-group-20"
for group_name in groups:
    t = first_command.replace("nharrand/intsec-group-20", group_name)
    docker_group_commands.append(t)

    

    group_docker_command = t
    print(group_docker_command)
    result = subprocess.run(group_docker_command, shell=True)
    print("docker container started")
    sleep(60)
    
    subprocess.run("docker ps > active_group.txt", shell = True)
    print("docker ps command done")
    sleep(1)
    print("start scraping")
    sleep(1)
    start_scrapping(group_name)


    with open("active_group.txt", "r") as f:
        lines = f.read()

    pattern = r"NAMES\n.{12}"
    match = re.search(pattern, lines)

    if match:
        dirty_container = match.group(0)
        clean_container = dirty_container.strip("NAMES\n")
        command = f'docker stop {clean_container}'
        subprocess.run(command, shell=True)
        sleep(30)
        second_command = f'docker rm {clean_container}'
        subprocess.run(second_command, shell=True)
        
