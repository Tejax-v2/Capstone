import http.server
import subprocess
import socketserver
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
sender_email = ""
receiver_email = ""
password = ""

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        ip = self.client_address[0]  # Extract source IP from incoming request
        print("Connected to:",ip)
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        # print("Parsed URL:",parsed_url)
        # print("Queryparams:",query_params)
        command = f"adb connect {ip}:5555" 
        try:
            # Run the command in the shell
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)        
            # Print the command output
            print("Command output:")
            print(result.stdout)
            mail_value = ""
            if 'mail' in query_params:
                mail_value = query_params['mail'][0]
                print("Received mail parameter:", mail_value)
            # Get email configuration from environment variables
            sender_email = os.getenv('SENDER_MAIL')
            receiver_email = mail_value
            password = os.getenv('SENDER_PASS')
            print("Sender email:", sender_email)
            print("Receiver email:", receiver_email)
            # Create message container
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = 'Test email from Python'
            # Email body
            body = 'This is a test email sent from Python.'
            # Attach body to message
            msg.attach(MIMEText(body, 'plain'))
            # Establish a connection to the SMTP server
            server = smtplib.SMTP('smtp.office365.com', 587)  # Replace with your SMTP server and port
            server.starttls()
            # Login to the SMTP server
            server.login(sender_email, password)
            # Send the email
            server.sendmail(sender_email, receiver_email, msg.as_string())
            # Close the connection
            server.quit()
            print('Email sent successfully!')
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(bytes("Processing device data..\nMail will be sent to your device soon", "utf8"))

        except subprocess.CalledProcessError as e:
            # If the command returns a non-zero exit status, print the error message
            print("Error executing command:")
            print(e.stderr)
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(bytes("Error", "utf8"))

PORT = 6060
Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server started at localhost:", PORT)
    httpd.serve_forever()

