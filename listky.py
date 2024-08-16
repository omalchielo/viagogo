import smtplib
import requests
import re
import json
from email.message import EmailMessage
import ssl
import time

url = "https://www.viagogo.com/Concert-Tickets/Country-and-Folk-Music/Taylor-Swift-Tickets/E-151949754?quantity=1"

def send_email(subject, content):
    email_sender = "botrozvrh@gmail.com"
    email_password = "ogkybntogxdmekzl"
    email_receiver = ["omalchielo@gmail.com"]

    em = EmailMessage()
    em.set_content(content)
    em["Subject"] = subject
    em["From"] = email_sender
    em["To"] = ", ".join(email_receiver)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

try:
    # Send an email notification that the bot has started
    send_email("Bot Started", "The ticket checking bot has started successfully.")

    last_status_email_time = time.time()
    status_interval = 2 * 60 * 60  # 2 hours in seconds

    while True:
        response = requests.get(url)
        html_content = response.text

        # Regex to find all JSON objects in the HTML content
        json_pattern = re.compile(r'\{.*?\}')
        json_matches = json_pattern.findall(html_content)

        ticket_details = ""
        very_cheap_ticket_details = ""
        found_ticket = False
        found_very_cheap_ticket = False

        for match in json_matches:
            try:
                json_object = json.loads(match)

                if ("count" in json_object and
                        "rawMinPrice" in json_object and
                        "formattedMinPrice" in json_object):

                    # Check if the price is below the threshold of 450
                    if json_object["rawMinPrice"] < 400:
                        found_ticket = True
                        # Accumulate ticket details
                        ticket_details += (
                            f"Count: {json_object['count']}\n"
                            f"Price: {json_object['formattedMinPrice']}\n"
                            f"Raw Price: {json_object['rawMinPrice']}\n"
                            f"Link: {url}\n\n"
                        )

                    # Check if the price is below the threshold of 350
                    if json_object["rawMinPrice"] < 350:
                        found_very_cheap_ticket = True
                        # Accumulate very cheap ticket details
                        very_cheap_ticket_details += (
                            f"Count: {json_object['count']}\n"
                            f"Price: {json_object['formattedMinPrice']}\n"
                            f"Raw Price: {json_object['rawMinPrice']}\n"
                            f"Link: {url}\n\n"
                        )

            except json.JSONDecodeError:
                continue

        if found_ticket:
            send_email("Tickets Found Below 450", f"Tickets under 450 found:\n\n{ticket_details}")

        if found_very_cheap_ticket:
            send_email("We Got It", f"We got it! Tickets found under 350:\n\n{very_cheap_ticket_details}")

        # Check if it's time to send a status email
        current_time = time.time()
        if current_time - last_status_email_time >= status_interval:
            send_email("Status Update", "The script is still running smoothly.")
            last_status_email_time = current_time

        time.sleep(480)  # Sleep for 8 minutes before the next check

except Exception as e:
    def send_status_email():
        email_sender = "botrozvrh@gmail.com"
        email_password = "ogkybntogxdmekzl"
        email_receiver = ["omalchielo@gmail.com"]
        subject = "CHYBA "

        em = EmailMessage()
        em.set_content(f"CHYBA: {str(e)}")
        em["Subject"] = subject
        em["From"] = email_sender
        em["To"] = ", ".join(email_receiver)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)

    send_status_email()
