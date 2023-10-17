from colorama import init, Fore, Back, Style
from datetime import datetime
import csv
import ast
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from time import sleep
import requests
import json
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("MailHUB - by 0felix000")
init() 

with open('settings.json', 'r') as f:
    j = json.load(f)

webhook = j["webhook"]
delay  = int(j["delay"])

tasks = []
def webhookk(sender, reciepient, subject, content):
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    hook = {
  "content": None,
  "embeds": [
    {
      "color": "16711680",
      "fields": [
        {
          "name": "Sender",
          "value": sender,
          "inline": True
        },
        {
          "name": "Reciepient",
          "value": reciepient,
          "inline": True
        },
        {
          "name": "Subject",
          "value": subject
        },
        {
          "name": "Time",
          "value": str(current_time),
          "inline": True
        },
        {
          "name": "Content",
          "value": content,
          "inline": True
        }
      ],
      "author": {
        "name": "MailHUB",
        "icon_url": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/af/Apple_JE3_BE3.png/revision/latest/thumbnail/width/360/height/360?cb=20200519232834"
      },
      "footer": {
        "text": "by 0felix000",
        "icon_url": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/af/Apple_JE3_BE3.png/revision/latest/thumbnail/width/360/height/360?cb=20200519232834"
      }
    }
  ],
  "attachments": []
}
    if webhook != "":
        r = requests.post(webhook, json = hook)

def ausgabe(x):
    text =  Fore.WHITE + "|" + Fore.RED + datetime.now().strftime("%H:%M:%S")+"."+(str(datetime.now().microsecond))[:4] + Fore.WHITE + "|" + " --- " + x
    return text

def do(id, inpu):
    inpu = ast.literal_eval(inpu)
    Email = inpu[0]
    Password = inpu[1]
    Reciepient = inpu[2]
    Subject = inpu[3]
    Content = inpu[4]

    def taskausgabe(x):
        text = ausgabe(str(id) + Fore.BLUE + " | " + Fore.WHITE +  Email + Fore.GREEN +" > "+ Fore.WHITE + x)
        return text

    # Email configuration
    sender_email = inpu[0]
    receiver_email = inpu[2]
    subject = inpu[3]
    body = inpu[4]

    # Gmail SMTP settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # 587 for TLS, 465 for SSL

    # Your Gmail account credentials (replace with your actual credentials)
    gmail_username = Email
    gmail_password = Password  # App Password or Gmail account password if less secure apps are enabled

    # Create the email message
    message = MIMEMultipart()

    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))


    # Connect to Gmail's SMTP server and send the email
    print(taskausgabe("Sending Email..."))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_username, gmail_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print(taskausgabe("Successuflly sent Email!"))
        webhookk(Email,Reciepient,subject,Content)
    except Exception as e:
        print(taskausgabe("Failed sending Email..."))



def start():
    print(ausgabe("Initialized MailHUB."))
    data_array = []
    
    with open("tasks.csv", 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data_array.append(row)
    
    tasks =  data_array

    print(ausgabe("Successfully loaded " + str(len(tasks) - 1) + " Tasks!"))

    print(ausgabe(""))
    print(ausgabe("Press enter to start all tasks"))
    input()
    x = 0
    for task in tasks:
        if x != 0:
            do(x, str(task))
            sleep(delay)
            print(ausgabe("Sleeping " + str(delay) + ".000 Seconds..."))
        x = x + 1

    
start()
input()