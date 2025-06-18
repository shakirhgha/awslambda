import os
import time
import boto3

ses = boto3.client('ses')

def handler(event, context):
    target_email = os.environ.get('TARGET_EMAIL')
    rate_limit = int(os.environ.get('RATE_LIMIT', '60'))  # messages per minute
    if not target_email:
        raise ValueError('TARGET_EMAIL not configured')

    delay = 60.0 / rate_limit if rate_limit else 0

    for record in event.get('Records', []):
        body = record['body']
        send_email(target_email, body)
        if delay > 0:
            time.sleep(delay)

    return {'status': 'processed', 'count': len(event.get('Records', []))}


def send_email(to_address, message_body):
    ses.send_email(
        Source=to_address,
        Destination={'ToAddresses': [to_address]},
        Message={
            'Subject': {'Data': 'Forwarded message'},
            'Body': {'Text': {'Data': message_body}}
        }
    )

