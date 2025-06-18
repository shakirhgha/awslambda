# AWS Email Forwarder

This project demonstrates a simple serverless setup for receiving email with Amazon SES,
queuing the messages with SNS/SQS, and forwarding them to another address using a
Lambda function at a controlled rate.

## Architecture

1. **SES** receives inbound email. Configure SES to publish inbound messages to an
   SNS topic.
2. **SNS** has an SQS queue subscribed to it. Incoming messages from SES are
   stored in the queue.
3. **Lambda** (`sqs_email_forwarder.py`) is triggered by the SQS queue. It reads
   queued messages and forwards them via SES to the target address. The send rate
   is throttled using the `RATE_LIMIT` environment variable (messages per
   minute).

## Deploying

This repository only contains the forwarding Lambda function. To deploy:

1. Package `sqs_email_forwarder.py` with its dependencies (see
   `requirements.txt`).
2. Create the SNS topic and SQS queue, then subscribe the queue to the topic.
3. Configure SES to send inbound mail for your domain to the SNS topic.
4. Deploy the Lambda function with permissions to read from the SQS queue and
   send mail with SES. Set the environment variables:

   - `TARGET_EMAIL` – the email address to forward messages to.
   - `RATE_LIMIT` – number of emails to send per minute (default `60`).

This provides a minimal framework; adjust the infrastructure to fit your
production requirements.
