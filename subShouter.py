#!/usr/bin/env python3

import os, sys, smtplib, ssl, configparser, shutil
from email.mime.text import MIMEText 
from email.mime.message import MIMEMessage
from pathlib import Path

parser = configparser.ConfigParser()
parser.read('subConfig.ini')
# General settings
timeout = parser['scan']['timeout']



# email settings
port = parser['email']['port']
password = parser['email']['password']
sender_email = parser['email']['sender_email']
receiver_email = parser['email']['receiver_email']

# local file settings
programs = parser['files']['programs']
resolvers = parser['files']['resolvers']

# DNS updater settings
source = parser['DNS']['source']

# use dnsvalidaator to create list of resolvers for amass - https://github.com/vortexau/dnsvalidator
# /opt/dnsvalidator/dnsvalidator -tL https://public-dns.info/nameservers.txt -threads 200 -o ./resolvers.txt && sort -R resolvers.txt | tail -n25 > 25resolvers.txt

def subEnumerate(program):
    print("**** Begginning amass enumeration of domains in " + program)
    os.system("amass enum -df ./programs/" + program + "/domains.txt -rf " + resolvers + " -dir ./programs/" + program + " -src -ip -timeout 120")

def subTrack(program):
    print("**** Beginning amass track for " + program)
    os.system("amass track -df ./programs/" + program + "/domains.txt -dir ./programs/" + program + "  > ./programs/" + program + "/message.txt")

def subReport(program):
    print("**** sending results email to " + receiver_email)
    subject = "amass results for " + program
    fp = open("./programs/" + program + "/message.txt", "r")
    msg = MIMEText(fp.read())
    fp.close()
    msg['Subject'] = "amass results for " + program
    msg['From'] = sender_email
    msg['To'] = receiver_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("subshouter@gmail.com", password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

if len(sys.argv) < 2:
    print("subShouter usage\n\n./subShouter.py <option>\n\nOptions: enum, add, del, purge\n")
    exit()

if (sys.argv[1]) == "enum":
    p = open(programs)
    for program in p:
        program = program.rstrip('\n')
        print("program = " + program)
        subEnumerate(program)
        subTrack(program)
        subReport(program)
    p.close()
    exit()

if (sys.argv[1]) == "add":
    newProgram = sys.argv[2].rstrip('\n')
    print("Adding new program: " + newProgram)
    # Check program does no already exist in programs.txt and add it if not
    p = open(programs)
    for program in p:
        if program == newProgram:
            print("Program '" + newProgram +"' already exists")
            exit()
    p.close()
    p = open(programs, 'a')
    p.write("\n"+newProgram)
    p.close()
    # Check if program directory already exists and add it if not
    if not os.path.exists("./programs/" + newProgram):
        os.makedirs("./programs/" + newProgram)
    # Create symlink from program directory to amass_config.ini file
    os.symlink("../../amass_config.ini", "./programs/"+newProgram+"/config.ini")
    Path("./programs/"+newProgram+"/domains.txt").touch()
    print(program+" added. Please add root domains to ./programs/"+newProgram+"/domains.txt")
    with open(programs) as filehandle:
        lines = filehandle.readlines()
    with open(programs, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)

if sys.argv[1] == "del":
    program = sys.argv[2]
    print("Deleting "+ program +" from programs.txt.  This will not remove the data folder from ./programs/")
    with open(programs, "r") as p:
        lines = p.readlines()
    with open(programs, "w") as p:
        for line in lines:
            if line.strip('\n') != program:
                p.write(line)

if sys.argv[1] == "purge":
    print("Purging all programs that are not in programs.txt\n\n*****  THERE IS NO COMING BACK FROM THIS - ALL DATA FOR DELETED PROGRAMS WILL BE ERASED *****")
    agree = input("type YES to continue: ")
    count = 0
    if agree == "YES":
        folderSet = set(line.strip() for line in open(programs))
        for folder in os.listdir("./programs"):
            if folder not in folderSet:
                print("Deleting " + folder)
                shutil.rmtree("./programs/"+folder)
                count+=1
    print("Deleted "+str(count)+" directories from ./programs/")
    exit()

if sys.argv[1] == "list":
    print("Current programs that will be enumerated:")
    p = open(programs)
    for program in p:
        print(program.strip('\n'))
    exit()

if sys.argv[1] == "dns":
    print("Updating resolvers")
    os.system('curl '+source+' -s | sort -R | tail -n 25 > ./resolvers.txt')
    exit()
