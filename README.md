#  AWS Auto-Scaling with Lambda Based on ALB Network Load

This project demonstrates how to automatically **scale EC2 instances** based on network load using AWS **Application Load Balancer (ALB)**, **CloudWatch**, **Lambda**, **SNS**, and **EventBridge**.

---

##  Project Overview

- Monitor ALB `RequestCount` metric using Lambda every 5 minutes
- Auto-launch EC2 instance if traffic > HIGH threshold
- Auto-terminate EC2 instance if traffic < LOW threshold
- Notifications sent via Amazon SNS
- Load tested using Apache Benchmark (ab)

---

##  AWS Services Used

| Service      | Purpose                                      |
|--------------|----------------------------------------------|
| EC2          | Hosts web application (Apache)               |
| ALB          | Balances network traffic                     |
| CloudWatch   | Monitors `RequestCount` metric               |
| Lambda       | Serverless auto-scaling logic                |
| SNS          | Sends notifications on scale events          |
| IAM          | Permissions for Lambda to access resources   |
| EventBridge  | Triggers Lambda every 5 minutes              |

---

## Architecture Diagram

![architecture](screenshots/architecture-diagram.png)

---
## Prerequisites

- AWS Account
- IAM user with admin or appropriate permissions
- Basic knowledge of:
  - Python
  - EC2, Lambda, IAM, ALB, CloudWatch
- Apache Benchmark tool (`ab`) for load testing

## Step-by-Step Setup Guide

### 1. Create an EC2 Instance

- Launch an EC2 instance with Ubuntu
- Open port 80 in Security Group
- SSH into instance and run:
  ```
  sudo apt update
  sudo apt install apache2 -y
  sudo systemctl start apache2
  sudo systemctl enable apache2
  ```
- Test the EC2 IP in your browser
---
### 2. Set Up an Application Load Balancer (ALB)

- Go to EC2 → Load Balancers → Create
- Select Application Load Balancer
- Create Target Group and attach EC2 instance
- Test ALB DNS in browser

### 3. Create an SNS Topic

- Go to SNS → Topics → Create topic
- Name it `alb-scaling-topic`
- Create an Email Subscription and confirm it from your email inbox (must)

### 4. Create IAM Role for Lambda

Attach the following policies:
- AWSLambdaBasicExecutionRole
- Inline policy with permissions:
  - ec2:DescribeInstances
  - ec2:RunInstances
  - ec2:TerminateInstances
  - cloudwatch:GetMetricStatistics
  - sns:Publish

### 5. Create the Lambda Function

- Use Python 3.13
- Paste the `lambda_function.py` code
- Update values for:
  - ALB name (e.g., `app/my-alb-name/id`)
  - AMI ID, KeyName, Security Group, Subnet ID
  - SNS Topic ARN

### 6. Schedule Lambda with EventBridge

- Go to EventBridge → Rules → Create rule
- Rule name: `lambda-5min-scheduler`
- Schedule expression: `rate(5 minutes)`
- Add your Lambda function as the target

### 7. Load Testing (Simulate Traffic)

Install Apache Benchmark (`ab`) tool:
```
sudo apt install apache2-utils
ab -n 5000 -c 100 http://<your-alb-dns>/
```
### 8. Verify Auto-Scaling Behavior

- Check CloudWatch Metrics: RequestCount
- Check Lambda logs in CloudWatch Logs
- Check EC2 Instances page for scaling actions
- Check SNS email for notifications  

##  Screenshots

| Description                       | Screenshot                          |
|----------------------------------|--------------------------------------|
| SNS Topic + Subscription         | ![](screenshots/sns-topic-subscription.png) |
| IAM Role + Policies              | ![](screenshots/lambda-iam-role-policies.png) |
| Lambda Function Code             | ![](screenshots/lambda-function-code.png) |
| RequestCount Metric in CloudWatch| ![](screenshots/cloudwatch-requestcount-graph.png) |
| Lambda Execution Logs            | ![](screenshots/cloudwatch-lambda-logs.png) |
| Registered EC2 in ALB Target Group| ![](screenshots/alb-target-group-registered-ec2.png) |
| EC2 Instances Dashboard          | ![](screenshots/ec2-instances-dashboard.png) |
| SNS Email Notification           | ![](screenshots/sns-email-notification.png) |
| Apache Benchmark Load Test       | ![](screenshots/apache-benchmark-load-output.png) |
| EventBridge Trigger              | ![](screenshots/eventbridge-schedule-rule.png) |

## Testing

1. Run Apache Benchmark against your ALB
2. Lambda should detect high traffic and scale up
3. Verify:
   - New EC2 instance launches
   - SNS email is received
   - CloudWatch Logs capture Lambda activity

## Learnings

- Used CloudWatch metrics to trigger autoscaling
- Programmed logic using Lambda + Boto3
- Integrated SNS and EventBridge for automation
- Load-tested system with real-time triggers




