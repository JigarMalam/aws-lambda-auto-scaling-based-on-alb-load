import boto3
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):
    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(minutes=5)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/ApplicationELB',
        MetricName='RequestCount',
        Dimensions=[
            {
                'Name': 'LoadBalancer',
                'Value': 'app/Jigar-LB-ELB-AutoS-Noti2/256xxxxx'
            }
        ],
        StartTime=start_time,
        EndTime=now,
        Period=300,
        Statistics=['Sum']
    )

    request_count = int(response['Datapoints'][0]['Sum']) if response['Datapoints'] else 0
    logger.info(f"RequestCount: {request_count}")

    # Get currently running instances
    instances = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])
    instance_ids = [i['InstanceId'] for r in instances['Reservations'] for i in r['Instances']]
    logger.info(f"Running EC2 Instances: {instance_ids}")

    # Scaling Logic...
    if request_count > 1000:
        # Launch new instance
        ec2.run_instances(
            ImageId='ami-xxxxxxxxxxxx',
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1,
            KeyName='your-key',
            SecurityGroupIds=['sg-xxxxxxx'],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'AutoScaleInstance'},
                        {'Key': 'LaunchedBy', 'Value': 'Lambda'}
                    ]
                }
            ]
        )
        sns.publish(
            TopicArn='arn:aws:sns:ap-south-1:xxxxxxxxxxxx:YourTopicName',
            Message=f'High load detected: {request_count} requests. Launched new EC2 instance.',
            Subject='Auto-Scaling Notification'
        )

    elif request_count < 200 and instance_ids:
        ec2.terminate_instances(InstanceIds=[instance_ids[0]])
        sns.publish(
            TopicArn='arn:aws:sns:ap-south-1:xxxxxxxxxxxx:YourTopicName',
            Message=f'Low load detected: {request_count} requests. Terminated EC2 instance {instance_ids[0]}.',
            Subject='Auto-Scaling Notification'
        )

