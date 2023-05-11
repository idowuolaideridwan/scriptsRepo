import boto3

autoscaling = boto3.client('autoscaling')
elb = boto3.client('elbv2')

# Create launch configuration
autoscaling.create_launch_configuration(
    LaunchConfigurationName='MyLaunchConfiguration',
    ImageId='ami-0abcdef1234567890',
    InstanceType='t2.micro',
    SecurityGroups=[
        'sg-0abcdef1234567890',
    ],
)

# Create load balancer
response = elb.create_load_balancer(
    Name='MyLoadBalancer',
    Subnets=[
        'subnet-0abcdef1234567890',
    ],
    Scheme='internet-facing',
    Tags=[
        {
            'Key': 'Name',
            'Value': 'MyLoadBalancer'
        },
    ]
)

load_balancer_arn = response['LoadBalancers'][0]['LoadBalancerArn']

# Create target group
response = elb.create_target_group(
    Name='MyTargetGroup',
    Protocol='HTTP',
    Port=80,
    VpcId='vpc-0abcdef1234567890',
)

target_group_arn = response['TargetGroups'][0]['TargetGroupArn']

# Create listener
elb.create_listener(
    LoadBalancerArn=load_balancer_arn,
    Protocol='HTTP',
    Port=80,
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': target_group_arn,
        },
    ]
)

# Create auto scaling group
autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='MyAutoScalingGroup',
    LaunchConfigurationName='MyLaunchConfiguration',
    MinSize=1,
    MaxSize=5,
    DesiredCapacity=3,
    LoadBalancerNames=[
        'MyLoadBalancer',
    ],
    HealthCheckType='ELB',
    HealthCheckGracePeriod=300,
    AvailabilityZones=boto3.client('ec2').describe_availability_zones()['AvailabilityZones'],
    Tags=[
        {
            'ResourceId': 'MyAutoScalingGroup',
            'ResourceType': 'auto-scaling-group',
            'Key': 'Name',
            'Value': 'MyAutoScalingGroup',
            'PropagateAtLaunch': True
        },
    ]
)
