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

## 🖼️ Screenshots

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

---

## 📂 File Structure

