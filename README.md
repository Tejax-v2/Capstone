# DoctorDroid

This tool scans your android device through ADB, generates the user-friendly PDF report and mails you the results at your specified email id.

## Description

DoctorDroid is an academic capstone project. This tool is designed to scan your android device for any unusual behaviour and generate a user-friendly PDF report from anywhere through wireless debugging. It uses android debug bridge features to get device data. The data is compiled categorically in tabular format into a PDF and mails the results to the email address input in form in tool homepage

## Getting Started

### Dependencies

* Linux - For running the server
* Flask - For Web application and endpoint handling
* Python - For scripting and automation
* ADB - For Android Debug Bridge commands
* FPDF - For generating PDF reports
* smtplib - For sending emails
* Ngrok - For port forwarding
* Android Device - For scanning and generating report

### Executing program

* Turn on Developers Options in Android Device
* Turn on wireless debugging
* Go to http://<ip-address-of-server>:5000
* Submit the email id in the website form
* If everything goes well, check the inbox
* Voila! You got your report

## Help

Make sure the installation steps are followed correctly. If you still face any problem, please create an issue in this repository.

## Authors

Developed by

Tejas Tupke - [@Tejax-v2](https://github.com/Tejax-v2)

## Version History

* 0.1
    * Initial Release