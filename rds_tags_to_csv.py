#!/usr/bin/python

import boto3
import csv

import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

rds=boto3.client('rds',region_name='us-east-1')
rdsinstances=rds.describe_db_instances()
arns=[]
for dblen in range(len((rdsinstances['DBInstances']))):
    arns.append(rdsinstances['DBInstances'][dblen]['DBInstanceArn'])
for arnval in arns:
    dbname=arnval.split(':')[6]
    fil_name = dbname +".csv"
    csv_detail="db " + dbname
    list_data=list(csv_detail.split(' '))
    d=[list_data]
    print(list_data)
    with open(fil_name, "w") as f:
        writer = csv.writer(f)
        for row in d:
            writer.writerow(row)
### now moving tags details to csv     
    rdstags=rds.list_tags_for_resource(ResourceName=arnval)
    for i in range(len(rdstags['TagList'])): 
        dat = rdstags['TagList'][i]['Key'], rdstags['TagList'][i]['Value']
        print(dat)
        dt=[dat]
        with open(fil_name,'a') as fd:
            writer = csv.writer(fd)
            for row in dt:
                writer.writerow(row)
## sending mail to users with attachment
    fromaddr = "user.name@gmail.com" 
    toaddr = "client.user@gmail.com"
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "RDS tags detail of DB " + dbname
    body = "Hi Team,\n\nPlease find attached file of RDS instances Tags Details\n\n"

    msg.attach(MIMEText(body, 'Plain'))

    filename = fil_name
    attachment = open("/Users/user.name/Desktop/Python/" + fil_name, "rb")

    p = MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())

    #encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition',"attachment; filename = %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com',587)

    s.starttls()

    s.login(fromaddr, "mail_password")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
