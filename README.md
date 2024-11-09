# 📧 Celery Application 

## Overview

This project is a Celery-based application that handles the scheduling and execution of tasks for sending weekly sale transaction emails to the admin. It communicates with two separate backend servers (Django and Node.js), requesting sales data and triggering the email reports. The application is deployed on an AWS EC2 instance and utilizes Supervisor for process management, ensuring that Celery worker and beat tasks run continuously.

## Features

- **Scheduled Task Management**: The application periodically sends requests to the Django and Node.js backend servers to retrieve sale transaction data and sends email reports to the admin.
- **API Key Authentication**: The application uses API key-based authentication to make requests to both servers.
- **Celery Worker and Beat**: 
  - **Celery Worker**: Executes the tasks of fetching data and sending emails.
  - **Celery Beat**: Schedules the periodic tasks to ensure reports are sent at the right time.
  
## Deployment and Process Management

- **Hosted on AWS EC2**: The Celery application is deployed on an AWS EC2 instance, ensuring reliability and uptime.
- **Supervisor Process Management**: 
  - **Supervisor** is used to manage the Celery worker and beat processes, keeping them running in the background and restarting them automatically in case of failure.
  
