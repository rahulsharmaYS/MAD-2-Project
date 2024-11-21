import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import shared_task  
from .workers import celery
from flask import current_app as app
from flask_mail import Message, Mail
from email.utils import COMMASPACE, formatdate
import csv
from celery.schedules import crontab
from email.mime.base import MIMEBase
from email import encoders
from io import StringIO
from datetime import datetime, timedelta
from celery import shared_task
from flask import current_app as app
from flask_mail import Mail
from .database import db
from .models import User, Sponsor, Campaign, CampaignRequest
import logging
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger('celery').setLevel(logging.DEBUG)

mail = Mail(app)

from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://localhost:6379/1', backend='redis://localhost:6379/2')

@celery.on_after_finalize.connect
def periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(timedelta(minutes=1), test_task.s(), name='test task')
    sender.add_periodic_task(timedelta(days=1), daily_reminders.s(), name='send daily reminders')
    sender.add_periodic_task(timedelta(days=30), monthly_activity_report.s(), name='send monthly activity reports')
    # sender.add_periodic_task(timedelta(seconds=10), daily_reminders.s(), name='send daily reminders')
    # sender.add_periodic_task(timedelta(seconds=15), monthly_activity_report.s(), name='send monthly activity reports')
app.conf.timezone = 'Asia/Kolkata'


@celery.task
def test_task():
    logging.info("Test task executed")
    try:
        email = ['your_own_test_gmail@gmail.com']
        name = 'User'
        send_email(email, "Final freaking testing", "Took all my soul out when it crashed :/", name)
    except Exception as e:
        logger.error("Error in test_task: %s", str(e))


def send_email(receivers, subject, message, user_name, attachment_content=None, attachment_filename=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'your_own_gmail@gmail.com'
    msg['To'] = COMMASPACE.join(receivers)
    msg.attach(MIMEText(generate_email_content(subject, message, user_name), 'html'))

    if attachment_content and attachment_filename:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment_content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment_filename}')
        msg.attach(part)


    smtp_server = 'smtp.gmail.com'
    port = 587
    smtp_user = 'your_own_gmail@gmail.com' 
    smtp_pass = 'abcd efgh ijkl mnop'  # here use your own Google App Password 

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, receivers, msg.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")

def generate_email_content(subject, message, user_name):
    return f"""
    <html>
        <head>
            <style>
                body {{font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;}}
                .container {{max-width: 600px; margin: auto; background: #f0f0f0; padding: 20px;}}
                h2 {{color: #007BFF;}}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>{subject}</h2>
                <p>Dear {user_name},</p>
                <p>{message}</p>
                <p>Best wishes,</p>
                <p>Your SponsorNet Team</p>
                <p><i>This is an auto-generated email. Please do not reply.</i></p>
                <a href="mailto:rahulsharmays97@gmail.com">Contact us</a>
            </div>
        </body>
    </html>
    """


@celery.task
def daily_reminders():
    logging.info("Sending daily reminders...")
    # print("Sending daily reminders...")
    influencers = User.query.filter(User.role_id == 2, User.is_banned == False).all()
    today = datetime.utcnow().date()
    for influencer in influencers:
        pending_requests = CampaignRequest.query.filter(
            CampaignRequest.user_id == influencer.username,
            CampaignRequest.status == 'Pending'
        ).count()
        if pending_requests > 0:
            send_email([influencer.email], "Reminder: Pending Ad Requests",
                        "You have pending ad requests. Please check your dashboard.",
                        influencer.username)
        else:
            send_email([influencer.email], "Daily Update",
                        "You have no pending ad requests. Keep up the good work!", influencer.username)
            
    # return "Daily reminders sent successfully!"

@celery.task
def monthly_activity_report():
    logging.info("Sending monthly activity reports...")
    sponsors = Sponsor.query.all()
    for sponsor in sponsors:
        campaigns = CampaignRequest.query.filter(CampaignRequest.sponsor_id == sponsor.sponsor_name).all()
        report_content = generate_monthly_report(campaigns)
        send_email([sponsor.email], "Monthly Activity Report", report_content, sponsor.sponsor_name)

    return "Monthly activity reports sent successfully!"


@shared_task
def generate_monthly_report(campaigns):
    print("Generating monthly report...")
    print('yo')
    print(campaigns)
    total_campaigns = len(campaigns)
    growth = sum(campaign.negotiated_price for campaign in campaigns)/total_campaigns
    budget_used = sum(float(campaign.payment.replace(',', '').replace('$', '')) for campaign in campaigns if campaign.payment)
    final_budget_after_negotiation = sum(campaign.negotiated_price for campaign in campaigns)
    ad_titles = ', '.join(campaign.ad_title for campaign in campaigns) if campaigns else 'N/A'
    ad_descriptions = ', '.join(campaign.ad_description for campaign in campaigns) if campaigns else 'N/A'
    terms_and_conditions = ', '.join(campaign.terms_and_conditions for campaign in campaigns) if campaigns else 'N/A'
    assigned_influencers = ', '.join(campaign.user_id for campaign in campaigns) if campaigns else 'N/A'
    
    return f"""
    <html>
        <head>
            <style>
                body {{font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;}}
                .container {{max-width: 600px; margin: auto; background: #f0f0f0; padding: 20px;}}
                h2 {{color: #007BFF;}}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Monthly Activity Report</h2>
                <p>Dear Sponsor,</p>
                <p>Here's the summary of your campaigns for this month:</p>
                <p>Total Campaigns: {total_campaigns}</p>
                <p>Growth % in Sales: {growth} %</p>
                <p>Actual Budget spent: {final_budget_after_negotiation}</p>
                <p>Total Advertisements: {ad_titles}</p>
                <p>Ad Descriptions: {ad_descriptions}</p>
                <p>Terms and Conditions: {terms_and_conditions}</p>
                <p>Assigned Influencers: {assigned_influencers}</p>
                <p>Best wishes,</p>
                <p>Your SponsorNet Team</p>
                <p><i>This is an auto-generated email. Please do not reply.</i></p>
                <a href="mailto:rahulsharmays97@gmail.com">Contact us</a>
            </div>
        </body>
    </html>
    """

from celery import Task
class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = 60 

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f'Task {self.name} with ID {task_id} failed: {exc}')


@shared_task
def export_campaign_csv(sponsor_id, sponsor_name):
    logging.info(f"Exporting campaign CSV for Sponsor ID: {sponsor_id}, Name: {sponsor_name}")
    sponsor = Sponsor.query.filter_by(sponsor_id=sponsor_id).first()
    if not sponsor:
        logging.error(f"Sponsor with ID {sponsor_id} not found.")
        return

    campaigns = Campaign.query.filter_by(sponsor_id=sponsor_name).all()
    if not campaigns:
        logging.error(f"No campaigns found for sponsor ID {sponsor_id}.")
        return
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Campaign ID', 'Campaign Name', 'Ad Title', 'Ad Description', 'Start Date', 'End Date', 'Budget','Visibility', 'Terms and Conditions'])
    
    for campaign in campaigns:
        writer.writerow([
            campaign.campaign_id,
            campaign.campaign_name,
            campaign.ad_title,
            campaign.ad_description,
            campaign.start_date.strftime('%Y-%m-%d') if campaign.start_date else None,
            campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
            campaign.payment,
            campaign.is_private,
            campaign.terms_and_conditions
        ])

    output.seek(0)
    csv_content = output.getvalue()
    output.close()

    send_email(
        [sponsor.email],
        "Campaign Details CSV",
        "Attached is the CSV file with details for your campaigns.",
        sponsor.sponsor_name,
        csv_content,'campaign_details.csv'
    )
    return "Campaign details exported and sent successfully!"


def send_csv_email(recipients, subject, body, sender_name, file_content, filename):
    msg = Message(subject, recipients=recipients, body=body, sender=f"{sender_name} <no-reply@yourapp.com>")
    msg.attach(filename, 'text/csv', file_content)
    mail.send(msg)



@shared_task
def export_all_campaigns():
    sponsors = Sponsor.query.all()
    for sponsor in sponsors:
        export_campaign_csv.delay(sponsor.sponsor_id, sponsor.sponsor_name)




# tasks call
# test_task()

# # send daily reminders at 6pm
# daily_reminders.delay()


# monthly_activity_report()

# export_all_campaigns()
