# AWS Beginner Workshop

Versioning: 
0.5 - Initial commit
0.7 20250319 - added tagging, cost insight

todo: 
lambda, database configuration, glue, event bridge, crud operations / updated web app, event generator and revising of pre-built iam roles to allows workshop steps. 


*This entire workshop is intended to be run from start to finish, with every section building upon the previous one. Please follow the instructions carefully and do not skip any steps or start halfway through.*

Every caption will feature some text, and then give you some exercises to try. You can recognize the exercises by the numbering in front of them. 

1. Log in using the link, username and password provided to you. 
2. Check that you are in the Europe (Frankfurt) / eu-central-1 region by clicking on the region selector in the top right corner of the console.

## Cloudshell

Since you might not have the ability to install tools and get a working shell on your corporate machine, we'll 'borrow' a temporary workspace for you called Cloudshell. 

Cloudshell can be accessed by clicking the Cloudshell button at the bottom left of your AWS console. When you open it, AWS starts a shell session for you, much like the command window in Windows, terminal window in MacOS or a command shell in linux. 

Under the hood, cloudshell is a small virtual machine that is prepared for you, running linux. The shell you are using responds to linux commands. Here are a few you are going to need: 
```bash
# List files and directories
ls
# List all files, hidden files, file permissions and timestamps: 
ls -al

# List current directory
pwd
# Change directory
cd mydirectory
# Go back to previous directory
cd ..
# Create a new directory
mkdir mydirectory
# Remove directory
rmdir mydirectory

# Create a new file
touch myfile.txt
# Remove file
rm myfile.txt

# Edit a file
nano myfile.txt
# Save the file (in nano, press CTRL+O), enter a filename and press Enter
# Save and exit (in nano, press CTRL+X, then Y, then Enter)
```

Your cloudshell environment is dedicated for you - but will be cleaned up after a period of inactivity. Software such as git, python, docker and AWS CLI are already installed for you. We will use those tools during the workshop.

1. Check if AWS CLI is installed: ```aws --version```
2. Check if git is installed: ```git --version```
3. Check if python is installed: ```python --version```
4. Check if docker is installed: ```docker --version```

## AWS CLI
AWS services can be configured in several ways. The entire platform and all services available on it, is accessible via the AWS CLI (as well as other Infrastructure-as-Code tools like cloudformation, terraform, or languages like python and javascript using the AWS-CDK). 

During the workshop, we will use the AWS CLI to interact with AWS services. Every step we do using AWS CLI can also be performed via the AWS Console - but the AWS CLI tends to be a lot quicker/easier, provided you know what you're doing. 

You can find the AWS CLI documentation here: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

Remember that you can check the outcome of the commands you perform using AWS CLI by checking the relevant pages in the AWS Console. 

AWS CLI commands are run from the command line. You can recognize them by the ```aws``` prefix.

1. Check which user you are logged in as: ```aws sts get-caller-identity```


## EC2 - virtual machines in the cloud

One of the main perks of using cloud services, is that they allow you to very quickly provision and scale IT infrastructure. Instead of having to go out and buy physical servers, data centers to host them, and a bunch of underlying network infrastructure to connect it all, using a cloud provider like AWS, you can very quickly provision virtual machines (VMs) that you can use to run your applications.

The AWS service that allows you to spin up VMs is called EC2 (Elastic Compute Cloud). EC2 offers a lot of options for different types of VMs, different sizes, and different operating systems - but for this workshop, we'll just keep things nice and simple. 

1. Search for EC2 in the AWS console search bar
2. Click on EC2
3. Click on "Launch Instance"

Pick the following options to configure your instance: 
- Name and tags
    - Name: *pick a name for your new server*

- Application and OS Images (Amazon Machine Image)
    - Amazon Linux 2023
    - Amazon Machine Image (AMI): Amazon Linux 2023 AMI

- Instance type
    - t2.micro

- Key pair (login)
    - Key pair name - required: *pick Proceed without a key pair*

- Network settings
    - Network: (ignore, should be fine)
    - Subnet: (ignore, should be fine)
    - Auto-assign public IP: (should say 'Enable')
    - Firewall (security groups): select existing security group 'workshop-webserver-sg'

4. Click on 'Launch instance'
5. Click on the instance that you just launched in the green text. This will take you to the instance details page.

Depending on how quick you are to click, you may see the 'Instance state' listed as 'pending'. Pending means the instance is still being provisioned and in the process of spinning up. Once it's ready, the instance state will change to 'running'.

6. Check the checkbox in front of your new webserver to open the details pane below. Make a note of the Public IPv4 address and the Private IPv4 address of your server. 

Now, even though you've created the server, it's not doing anything yet. We need to install some software on it to make it do something useful. Let's turn your server into a web server.

7. While your server is selected in the instance overview, click Connect. 

AWS offers several ways to connect to your server - we'll use the 'EC2 Instance Connect' option. Leave everything on default, and click 'Connect'.
You'll be taken to a terminal session on your new server, which behaves pretty much the same as your CloudShell (But don't forget your cloudshell and webserver are completely different systems)

Notice the prompt in the terminal session. It should say 'ec2-user@ip-172-31-23-3 ~]$

- ec2-user is the username you're logged in as
- ip-172-31-23-3 is the private IP address of your server
- ~ is the home directory of the user you're logged in as

8. Let's get started and install web server program on your new vm. Run the following commands: 
```bash
sudo dnf update -y
# this command updates your system packages. This is standard linux maintenance practice, and even though it will not find anything up update, since that's already done when creating and spinning up the server, it's still a good practice to do this.

sudo dnf install -y httpd
# this command installs the Apache web server (httpd) on your system. Apache is a popular web server software that can serve web pages and handle HTTP requests.

# sudo is an important command in the linux world, it allows you to run commands as the superuser (root) - which not being logged in as root. Try running these commands without sudo, and you'll find that you get a permission denied error.

# The reason you are able to use sudo is because you're logged in as the ec2-user, which is a user that has sudo privileges. Both for security and human error reasons, you don't want to administer your server as the root user. By using sudo, you can perform the commands you need with less risk of doing things you might regret. 

# 
```

After that, you have updated the system packages and installed the web server software. Before we start the webserver, let's create a html page so the webserver has something to ... you know ... serve. 

9. Let's create a html page: ```sudo nano /var/www/html/index.html``` and enter the content below, then save and exit:
```html
<h1>Amazon Linux 2023 Web Server</h1>
<h2>Private IP: YOUR-PRIVATE-IP</h2>
<h2>Public IP: YOUR-PUBLIC-IP</h2>
```

Replace YOUR-PRIVATE-IP and YOUR-PUBLIC-IP with the actual private and public IP addresses of your server.

You can check the contents of the index.html file by typing ```cat /var/www/html/index.html```.

10. Let's start the web server: ```sudo systemctl start httpd```.
11. Let's make sure the web server starts automatically on boot: ```sudo systemctl enable httpd```
12. Let's check if the web server is running: ```sudo systemctl status httpd```

If everything went well, you should be able to access your web server from the internet.

13. Open a new browser tab, and go to ```http://YOUR-PUBLIC-IP```. You should see your web server's page.

## Load balancing

Having one webserver up and running is great - but running your app on a single server is not very resilliant. If the server goes down, your app will be unavailable - and if the host gets too busy, your app might become very slow. 

To make applications more robust to handle these sort of problems, you can use load balancers. Load balancers are services that distribute traffic across multiple servers, and can help you handle high traffic and ensure your app is always available. 

But to balance some load, we'll first need a second server, just like the one you created earlier. But this time, we'll provision it using the AWS CLI and a user-data script.

1. create a user-data file using nano: ```nano user-data.sh``` and enter the content below, then save and exit:
```bash
#!/bin/bash

# Update system packages
dnf update -y

# Install Apache (httpd)
dnf install -y httpd

# Get EC2 Metadata using IMDSv2 (More Secure)
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -s)

PRIVATE_IP=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" -s http://169.254.169.254/latest/meta-data/local-ipv4)
PUBLIC_IP=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" -s http://169.254.169.254/latest/meta-data/public-ipv4)

# Generate index.html
cat <<EOF > /var/www/html/index.html
<h1>Amazon Linux 2023 Web Server</h1>
<h2>Private IP: $PRIVATE_IP</h2>
<h2>Public IP: ${PUBLIC_IP}</h2>
EOF

# Start and enable Apache web server
systemctl start httpd
systemctl enable httpd
```

You'll recognize a lot of the commands from the previous step. By having them in a user-data script, you can run them automatically when the server is provisioned - without having to manually log in and run them.

2. Set the correct file permissions for the user-data script: ```chmod +x user-data.sh```

3. Launch the second server by running the following command in Cloudshell (replace MY-SERVER-NAME with the name you want to give the server):

```bash
aws ec2 run-instances \
    --image-id ami-0b74f796d330ab49c \
    --instance-type t2.micro \
    --security-group-ids sg-03540e5abba9a012b \
    --subnet-id subnet-3fc22c73 \
    --user-data file://user-data.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MY-SERVER-NAME},{Key=CREATED_BY,Value='"$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}')"'}]'
```

4. The command will echo a lot of information about the new instance and present you with a : 
Hit 'q' to exit the review information and check the EC2 console to see your new instance! 

You just created the entire server - including the OS, the web server, and the content - with pretty much a single command. 

5. Check the public IP of the new server. Then open a new browser tag and point it to http://PUBLIC-IP. You should see your new server's page.

Compare the web pages served by both servers. They should be different, since each server has its own private IP and public IP.

6. Small interlude - let's make sure your first server is tagged. Look up the instance ID of your first server and run:
```bash
aws ec2 create-tags \
    --resources i-YOUR-INSTANCE-ID \
    --tags Key=CREATED_BY,Value="$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}')"
```

Since we have two servers, we can now use a load balancer to distribute traffic between them. Load balancers are services that distribute traffic across multiple servers, and can help you handle high traffic and ensure your app is always available.

7. Let's create a classic loadbalancer:

```bash
aws elb create-load-balancer \
    --load-balancer-name YOUR-LOAD-BALANCER-NAME \
    --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80 \
    --security-groups sg-06330e05af8282fd8 \
    --subnets subnet-bab418d0 subnet-3fc22c73 subnet-8bfde6f6 \
    --tags Key=Name,Value=YOUR-LOAD-BALANCER-NAME Key=CREATED_BY,Value="$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}')"
```

When the load balancer has been created, the command will echo back its dns name, which will look like: YOUR-LOAD-BALANCER-NAME-123456788.eu-central-1.elb.amazonaws.com

If you open a new browser tab and point it to http://YOUR-LOAD-BALANCER-NAME-123456788.eu-central-1.elb.amazonaws.com, you'll find there is no content being served. This is because we not actually registered any targets with the load balancer - so right now, it doesn't know where to send the requests we send it to.

8. First, let's look up the Instance Id's of your running servers. You can do this through the EC2 console page, or by running the following command: 

```bash
aws ec2 describe-instances \
    --filters "Name=tag:CREATED_BY,Values=$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}')" "Name=instance-state-name,Values=running" \
    --query "Reservations[*].Instances[*].{ID:InstanceId,Name:Tags[?Key=='Name'].Value|[0],State:State.Name,PrivateIP:PrivateIpAddress,PublicIP:PublicIpAddress}" \
    --output table

# Notice this command is again a bit more elaborate than it needs to be - but this way you won't get confused by the output. 
```

9. Using the Instance Id's from the previous command, register the servers with the load balancer:
```bash
aws elb register-instances-with-load-balancer \
    --load-balancer-name YOUR-LOAD-BALANCER-NAME \
    --instances i-xxxxxxxxxxxx i-yyyyyyyyyyyy
```

When performed successfully, the command will echo back a json object with the instance ids that were registered.

Now when you try the http://YOUR-LOAD-BALANCER-NAME-123456788.eu-central-1.elb.amazonaws.com again, you'll see it's still not working. This is because, even though the load balancer now knows which targets are potentially available for it to send requests to, it doesn't know which of those targets are actually healthy and available.

To fix this, we need to create a health check for the load balancer.

10. Create a health check for the load balancer:
```bash
aws elb configure-health-check \
    --load-balancer-name YOUR-LOAD-BALANCER-NAME \
    --health-check Target=HTTP:80/,Interval=30,Timeout=5,UnhealthyThreshold=2,HealthyThreshold=2
```

When performed successfully, the command will echo back a json object with the health check configuration.

And now, when you try the http://YOUR-LOAD-BALANCER-NAME-123456788.eu-central-1.elb.amazonaws.com again, you should see a response from one of your servers. If you hit refresh a few times, you should see the pages from the servers you created alternate.

aws elb describe-load-balancers --load-balancer-names test-lb2 \
    --query "LoadBalancerDescriptions[*].Instances"


## Security groups and public IP's

AWS Security groups are a way to control access to your EC2 instances. They act as firewalls. 

Right now, both your webservers can be reached directly over the internet, by simply pointing a browser to http://PUBLIC-IP. This is not a good idea for several reasons. It has some security concerns, and it completely negates the load balancer we created.

So let's change that by making the VM's not reachable over the internet. There are several ways we can accomplish this. 

We could ... move the ec2's to a private subnet. Very viable, but not in scope for this workshop.
We could ... remove the security group rules that allow traffic from the internet. This would indeed make the VM's unreachable over the internet - but since the load balancer uses the same port and protocol to perform the health check, it would also break our load balancing setup. 

So for now, let's simply remove the public IP address from the instances. This will make the VM's unreachable over the internet, but the load balancer will still be able to reach them.

1. First, stop the instances:
```bash
aws ec2 stop-instances --instance-ids i-YOUR-FIRST-INSTANCE-ID i-YOUR-SECOND-INSTANCE-ID
```

You'll see in the EC2 console that the instance state for both your instances is now 'Stopping'. And a while later, they will show up as 'Stopped'.

You can also verify instance state by running:
```bash
aws ec2 describe-instances \
    --filters "Name=tag:CREATED_BY,Values=$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}')" \
    --query "Reservations[*].Instances[*].{ID:InstanceId,Name:Tags[?Key=='Name'].Value|[0],State:State.Name,PrivateIP:PrivateIpAddress,PublicIP:PublicIpAddress}" \
    --output table
```

Removing the auto assigning of a public ip address is a change that needs to be performed on the network interface of both instances. 

2. You can find the network interface id's of both instances by running:
```bash
aws ec2 describe-instances \
    --filters "Name=tag:CREATED_BY,Values=$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}')" \
    --query "Reservations[*].Instances[*].NetworkInterfaces[*].NetworkInterfaceId" \
    --output table

# you can also look this up via the EC2 console
```

3. To make sure a public IP is no longer assigned, run:
```bash
aws ec2 modify-network-interface-attribute --network-interface-id eni-YOUR-NETWORK-INTERFACE-ID --no-associate-public-ip-address

# run this command twice - once for each network interface.
```

4. Then, start your instances again:
```bash
aws ec2 start-instances --instance-ids i-YOUR-FIRST-INSTANCE-ID i-YOUR-SECOND-INSTANCE-ID
```

When your instances are up and running again, check their public IP addresses - either through the console or aws cli. 
You'll notice that they no longer have a public IP. 

5. Check your browser tabs: http://YOUR-FIRST-PUBLIC-IP and http://YOUR-SECOND-PUBLIC-IP will no longer work - but the load balancer still does! 

You can also verify using the load balancer overview in the EC2 console, that your load balancer still has two healthy targets - even though your hosts no longer have public IP addresses.


## S3

Amazon S3 (Simple Storage Service) is an object storage service. S3 is a very easy way to store files and access them from anywhere in the world - if you configure access the way you want. We'll be creating a bucket, and then using it as a data store for some test data we'll generate. 

1. S3 bucket names have to be globally unique. To see which buckets are already present, type ```aws s3 ls```
2. Look for the S3 service in the AWS Service search bar, and compare the general purpose buckets with the output in your cloudshell.

3. Now let's create your own bucket. Creating a bucket is quite simple with the ```aws s3 mb``` command. But in order to make sure your bucket is unique, we'll make the command a little fancier: 

```bash
aws s3 mb s3://$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}')-$(aws sts get-caller-identity --query Account --output text)
```

Note that there are a few | symboles in the elaborate command above. Those are called pipes, and they are used to pass the output of one command as input to another. 
Pipes are one of the ways that allow you to run very complex commands, where one step is dependent upon another. 

4. Check the output of the command - and then verify the S3 console page and the present buckets with ```aws s3 ls```. 

5. Last step is to tag your bucket. Tagging your resources is a good idea in general. Run the following command, and replace ```YOUR-BUCKET-NAME``` with the name of the bucket you created.

```bash
aws s3api put-bucket-tagging --bucket YOUR-BUCKET-NAME --tagging 'TagSet=[{Key=CREATED_BY,Value='"$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}')"'}]'
```

## Test data

In order to generate some test data, we'll drafts a simple python program that creates some fake sales information in the bucket you created. 

1. open nano: ```nano```

When nano opens, you'll see some new options appear at the bottom of your Cloudshell window. You've just opened a console-based text editor, and are now editing a new file. 

2. Copy the following code into nano:
```python
import boto3
import random
import string
import time
import json

s3 = boto3.client('s3', region_name='eu-central-1')

# Pregenerated customer IDs
customer_ids = [
    'CUST123456', 'CUST789012', 'CUST345678', 'CUST901234',
    'CUST567890', 'CUST123789', 'CUST456012', 'CUST789345',
    'CUST012678', 'CUST345901'
]

# Pregenerated item-price combinations
item_price_combinations = [
    {'description': 'Item A', 'price': 10.0},
    {'description': 'Item B', 'price': 20.0},
    {'description': 'Item C', 'price': 30.0},
    {'description': 'Item D', 'price': 40.0},
    {'description': 'Item E', 'price': 50.0},
    {'description': 'Item F', 'price': 60.0},
    {'description': 'Item G', 'price': 70.0},
    {'description': 'Item H', 'price': 80.0},
    {'description': 'Item I', 'price': 90.0},
    {'description': 'Item J', 'price': 100.0}
]

def generate_random_data():
    # Generate a unique 15-number identifier
    identifier = ''.join(random.choices(string.digits, k=15))
    # Select a random customer ID from the pregenerated list
    customer_id = random.choice(customer_ids)
    # Generate an order ID
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    # Randomly select a subset of item-price combinations
    items = random.sample(item_price_combinations, k=random.randint(1, 5))
    # Assign a random amount to each selected item
    for item in items:
        item['amount'] = random.randint(1, 10)
    return identifier, customer_id, order_id, items

def lambda_handler(event, context):
    try:
        bucket_name = event.get('bucket_name', 'YOUR-BUCKET-NAME')
        identifier, customer_id, order_id, items = generate_random_data()
        
        content = {
            'customerID': customer_id,
            'orderID': order_id,
            'items': items
        }
        
        s3.put_object(Bucket=bucket_name, Key=f"data_{identifier}.json", Body=json.dumps(content))
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data uploaded successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

if __name__ == '__main__':
    while True:
        lambda_handler({'bucket_name': 'YOUR-BUCKET-NAME'}, None)
        time.sleep(1)
```

3. Replace ```YOUR-BUCKET-NAME``` with the name of the bucket you created.
4. Write the buffer of nano to a new file: ```Crtl+O```, type filename ```generate_data.py```, and hit```Enter```
5. Save and exit: ```Ctrl+X```

6. You can see the new file you created with ```ls```
7. You can view the contents of the file you created with ```cat generate_data.py```

The pytho file you just created will generate some test data and store it in your S3 bucket. Let's run it:
6. Type: ```python3 generate_data.py``` 

You'll notice that the program doesn't appear to be doing a whole lot - but it is! It's generating some test data and storing it in your S3 bucket. 

You can verify this by checking the S3 console page, and viewing the contents of your bucket. Refresh a few times to see the new files being generated.

7. In cloudshell, type ```Ctrl+C``` to stop the program.

8. You've seen that the python script has generated a bunch of files in your S3 bucket using the console. You can also use AWS CLI to do that, by typing ```aws s3 ls s3://your-bucket-name```.

You may have already tried opening one of the created files through the S3 console, but you'll find that AWS won't let you open them - that's because the files are not public. S3 buckets are created private by default, which means they're not accessible over the internet. 

You can however view the files in CloudShell by typing
```bash

aws s3 cp s3://your-bucket-name/file-name -

# remember to change your bucketname to your s3 bucketname
# remember to change file-name to the name of the file you want to view. It'll look something like 'data_995817511516300.json'

# cp is short for copy, the - is short for standard output. By copying the contents of the file to standard output, it gets displayed in your shell.
```

If you're familiar with the JSON file format, which is commonly used for data exchange between services and applications, you'll see that the file contains some entirely random sales data - there's a customer, an order and some items that make up the order. 

All of the data is generated randomly, by the python script you ran. 


## RDS 

We created some webservers and a loadbalancer using AWS EC2 and related services. All well and good - but the app we're serving doesn't actually do anything yet. (I'm sure you've noticed that, even though those hosts no longer have public IP addresses, the web content they're serving still claims they do. We haven't updated the index.html files, remember?)

Now, in order to make our nice infrastructure do something, we are going to build out some processes and service configurations that:
- pick up the order data from S3 (whether it's already there, or freshly added to your s3 bucket)
- transformes it into usable format
- stores it in a database

... so that ultimately we'll be able to display data from the dabase in our web application. 

First things first: let's create a database. We'll use Amazon RDS (Relational Database Service) to create a PostgreSQL database.

RDS is what's known as a PAAS / platform service. It allows us to spin up databases, and manage them, without having to worry about the underlying infrastructure. Note that we don't even have to spin up a server to install the database - RDS will do that for us.

1. Create our database:
```bash
aws rds create-db-instance \
    --db-instance-identifier "$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}' | tr -cd 'a-zA-Z0-9-' | sed 's/^[^a-zA-Z]*/awsuser-/')-$(aws sts get-caller-identity --query Account --output text)-orders-db" \
    --db-instance-class db.t4g.micro \
    --engine postgres \
    --allocated-storage 20 \
    --master-username dbadmin \
    --master-user-password dbpassword \
    --db-name orders \
    --vpc-security-group-ids sg-0044dbb2dc1995730 \
    --db-subnet-group-name workshop-db-subnet-group \
    --publicly-accessible \
    --backup-retention-period 7 \
    --storage-encrypted \
    --tags Key=CREATED_BY,Value="$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}')"

# Pick whatever password you like. The other entries are fine the way they are. You don't have to change them.

# Don't mess with the security group, subnet group and other connectivity-related options. They're required to provision a database, but for the scope of the workshop we won't create those from scratch. Just consume what's already there. 

# PLEASE NOTE: There are a few options here that are NOT standard. By default, for example, you would never set your database to be publicly accessible. The only reason we do this now, is so we can use Cloudshell and psql to perform database operations.
```

2. Check the status of the database you created, either using the AWS console or by running: 
```bash
aws rds describe-db-instances \
  --query "DBInstances[*].{DBInstance:DBInstanceIdentifier, Status:DBInstanceStatus}" \
  --output table
```

You'll see the database going through several statusses while spinning up. First it will be 'creating', then 'backing-up' and finally 'available'.

Congratuations - you've created a database. 

## Tagging

You may have noticed that the resources you've created have tags attached to them. Most services and resources you can deploy in AWS can be tagged. And tags can be used for basically anything. 

A tag is just that: an identifier or label that you stick onto a resource. They can be useful for maintenance purposes - or just to tell who created what, when or why. 

Tags are also very useful when you need to allocate AWS cost to a specific application that consists of several infrastructure components. For example, you may want to know what the stack you've just deployed - two web servers, a load balancer and a database - actually costs. 

Tagging is not a mandatory practice - and if you're the only one using a particular AWS account, or you know for a fact that all cost incurred in an account can be attributed to a single application or responsible party, you can just use the account-wide cost explorer and cost dashboard. 

But in your case, you're not the only one using this particular account. And you may want some more granular insight. 

You'll may have noticed the following option in a lot of the AWS CLI commands you've used up to this point: 

```bash
 --tags Key=CREATED_BY,Value="$(aws sts get-caller-identity --query Arn --output text | awk -F'/''{print $NF}')"

 # try running the following snippet in cloudshell:
 aws sts get-caller-identity --query Arn --output text

 # you'll see that the output is something like the following:
 # aarn:aws:iam::391614831370:user/your-username

 # now run the following: 
 aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}'

 # you'll see that the output is something like the following:
 # your-username

 # awk is a linux command line tool that can be used to perform actions on files and strings. 
 # In this case, it's used to extract the value of the 'your-username' part of the string. 
 # After the aws sts command, we pipe the full arn into the awk command in order to reformat the arn to the snippet of text we actually want to use. 
```

So that's how we end up with the CREATED_BY - your-username tags. 

You can check all resources created and tagged with CREATED_BY and your-username, by running the following command: 

```bash
aws resourcegroupstaggingapi get-resources --tag-filters Key=CREATED_BY,Values=$(aws sts get-caller-identity --query Arn --output text | awk -F'/' '{print $NF}')

# scroll through the output using the up and down arrows. You'll recognize the output and specific aws services you've spun up.
# press q when you're done.
```

## AWS cost and cost insight

To monitor cost incurred by services running in an account, you can use the AWS cost explorer. It's pretty self explanatory - you can filter by service, instance type, region, usage type, etc.

You can also use cli to get some insight into cost that you have generated up to now.

1. Run the following command to get cost per service that you have generated over the last 30 days: 
```bash
aws ce get-cost-and-usage \
    --time-period Start=$(date -d "-30 days" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
    --granularity MONTHLY \
    --metrics "UnblendedCost" \
    --filter '{
        "Tags": {
            "Key": "CREATED_BY",
            "Values": ["'"$(aws sts get-caller-identity --query Arn --output text | awk -F '/' '{print $NF}')"'", "None"],
            "MatchOptions": ["EQUALS"]
        }
    }' \
    --group-by '[{"Type":"DIMENSION","Key":"SERVICE"}]' \
    --query "ResultsByTime[0].Groups[*].[Keys[0], Metrics.UnblendedCost.Amount]" \
    --output table

# notice that the command explicitly filters on the CREATED_BY tag, and your username as a value. If your resources are not tagged, they won't show up.
```

In very practical terms, you're playing around in my personal aws account. So I've implemented some measures that keep you from spending a ton of money on my behalf. Although the resources you'll deploy and build during the workshop technically are not free, in practical terms you'll be surprised how little you actually end up spending.

How to actually architect for cost is a whole different topic, which requires you to understand your requirements and the behavior of your workload. If you want to delve into actual architecture topics, read up on the AWS well architected framework. It guides you through a lot of relevant considerations when architecting for cloud deployments (and tends to make your designs better as a whole).

## Lambda

When spinning up resources in AWS, you tend to pay for what you use when you use it. For serverless services like AWS Lambda, you only pay for compute time while the Lambda function is running.

Serverless is an interesting term. In practical terms, a service can be called serverless when you don't have to provide infrastructure and spin up servers yourself in order to use it. 

Lambda is a serverless service that allows you to run code without provisioning a server for the code to run on. So you don't first have to start a virtual machine / ec2 or spin up a container before your code can execute. 

Don't be fooled though - obviously your code needs to run somewhere. But the way AWS has set up the service, you don't have to worry about that. It's all taken care of for you. All you have to do is write your code, deploy it and have it run when you need it to. And AWS will bill you for the compute resources required to run your code. 

More traditional, IAAS services like EC2, and to an extent RDS, incur a cost while instances are running. Because even when you're not actively putting load on the instance, it's still up, running and reserved for you. 

You can save some money by stopping instances when you don't need them. This can be useful for non-prd workloads, for example, that you may not need outside of office hours. 

We can automate shutting down the infrastructure you provisioned with a lambda function. Let's create one to handle that task for you.

1. First, we'll create the python script that lambda will run - which is supposed to check for running ec2 and rds instances and shut them down. Create a new file paste the following code:
```python
import boto3

# User must set this value before running the function
IAM_USERNAME = "your-username-here"  # <-- Change this to the IAM user you want to filter by

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    rds_client = boto3.client('rds')

    print(f"Filtering EC2 and RDS instances for user: {IAM_USERNAME}")

    # Stop EC2 instances with tag CREATED_BY = IAM_USERNAME
    ec2_instances = ec2_client.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']},
            {'Name': 'tag:CREATED_BY', 'Values': [IAM_USERNAME]}
        ]
    )

    ec2_instance_ids = [
        instance['InstanceId']
        for reservation in ec2_instances['Reservations']
        for instance in reservation['Instances']
    ]

    if ec2_instance_ids:
        ec2_client.stop_instances(InstanceIds=ec2_instance_ids)
        print(f"Stopping EC2 instances: {ec2_instance_ids}")
    else:
        print("No running EC2 instances found for user:", IAM_USERNAME)

    # Stop RDS instances with tag CREATED_BY = IAM_USERNAME
    rds_instances = rds_client.describe_db_instances()
    
    rds_stopped = False
    for db_instance in rds_instances['DBInstances']:
        db_instance_id = db_instance['DBInstanceIdentifier']
        tags = rds_client.list_tags_for_resource(
            ResourceName=db_instance['DBInstanceArn']
        )['TagList']

        # Check if CREATED_BY tag exists and matches IAM_USERNAME
        for tag in tags:
            if tag['Key'] == 'CREATED_BY' and tag['Value'] == IAM_USERNAME:
                if db_instance['DBInstanceStatus'] == 'available':  # Running state
                    rds_client.stop_db_instance(DBInstanceIdentifier=db_instance_id)
                    print(f"Stopping RDS instance: {db_instance_id}")
                    rds_stopped = True
                break

    if not rds_stopped:
        print("No running RDS instances found for user:", IAM_USERNAME)

    return {"status": "Success", "user": IAM_USERNAME}
```

2. Create a zip file from the lambda function:
```bash
zip -r YOUR_ZIP_FILE.zip lambda_function.py
```

Now you have the functionality you want the lambda function to perform in a zip file. But in order to affect resources in AWS successfully, lambda needs to be able to assume the right permissions at runtime. 

This is handled via an IAM role. An AWS IAM role is a set of permissions that a process that is allowed to assume that role, may affect. In this case, you want the lambda function to be able to stop ec2 and rds instances that you created, and are tagged with the CREATED_BY / your-iam-user tag.

In technical terms, an IAM role is simply a collection of IAM policies - and policies are JSON documents that contains a set of permissions that a process that is allowed to assume that role, may (or may not) affect.

IAM roles can be created in the AWS console - but this can also be handled via the AWS CLI.

3. First, let's create an IAM policy:

```bash
#First, run the following command in cloudshell: 
IAM_USERNAME=$(aws sts get-caller-identity --query Arn --output text | awk -F '/' '{print $NF}')
echo "IAM User: $IAM_USERNAME"

# This stores your iam username in the IAM_USERNAME environment variable in your shell. You can then use it in follow-up commands. Will use this to create an IAM policy: 

aws iam create-policy \
    --policy-name "EC2-RDS-Control-Policy-$IAM_USERNAME" \
    --policy-document "{
        \"Version\": \"2012-10-17\",
        \"Statement\": [
            {
                \"Effect\": \"Allow\",
                \"Action\": [
                    \"ec2:DescribeInstances\",
                    \"ec2:StopInstances\",
                    \"ec2:StartInstances\"
                ],
                \"Resource\": \"*\",
                \"Condition\": {
                    \"StringEquals\": {
                        \"ec2:ResourceTag/CREATED_BY\": \"$IAM_USERNAME\"
                    }
                }
            },
            {
                \"Effect\": \"Allow\",
                \"Action\": [
                    \"rds:DescribeDBInstances\",
                    \"rds:StopDBInstance\",
                    \"rds:StartDBInstance\"
                ],
                \"Resource\": \"*\",
                \"Condition\": {
                    \"StringEquals\": {
                        \"rds:db-tag/CREATED_BY\": \"$IAM_USERNAME\"
                    }
                }
            },
            {
                \"Effect\": \"Allow\",
                \"Action\": [
                    \"ec2:DescribeTags\",
                    \"rds:ListTagsForResource\"
                ],
                \"Resource\": \"*\"
            }
        ]
    }"
```



Notice that the policy we created Allows the following:

- Describe ec2 instances with tag CREATED_BY = IAM_USERNAME
- Stop ec2 instances with tag CREATED_BY = IAM_USERNAME
- Start ec2 instances with tag CREATED_BY = IAM_USERNAME
- Describe rds instances with tag CREATED_BY = IAM_USERNAME
- Stop rds instances with tag CREATED_BY = IAM_USERNAME
- Start rds instances with tag CREATED_BY = IAM_USERNAME
- Describe ec2 tags
- Describe rds tags

AWS has a lot of granularity when it comes to IAM policies. You can find out more about IAM policies here: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html

It tends to be easier to create policies in the AWS console, especially when you're not entirely sure what you're looking for. If you do - and if you want to be fast, creating them through cli or code is quicker. 

Now that we have a policy, we need to attach it to a role.

4. Attach the policy to the role:
```bash
# Setting the IAM_USERNAME environment variable is only necessary if you no longer have it set:
IAM_USERNAME=$(aws sts get-caller-identity --query Arn --output text | awk -F '/' '{print $NF}')

# Then attach your policy to a new role. 
aws iam attach-role-policy \
    --role-name "LambdaStopEC2RDS-$IAM_USERNAME-role" \
    --policy-arn "arn:aws:iam::391614831370:policy/EC2-RDS-Control-Policy-$IAM_USERNAME"
```

Great, now you have created a role that grants lambda the required permissions when it runs your code. 
You can also find out more about IAM roles here: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html

Time to create the actual lambda. 

5. Run the following command in Cloudshell:
```bash
aws lambda create-function \
    --function-name "stopec2rds-$(aws sts get-caller-identity --query Arn --output text | awk -F '/' '{print $NF}')" \
    --runtime python3.13 \
    --role arn:aws:iam::391614831370:role/LambdaStopEC2RDS-$IAM_USERNAME-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://YOUR_ZIP_FILE.zip   
```

This creates the lambda function, uploads the code and configures it to use the IAM role you created.

Time to test it out! 

6. Look up your function in AWS lambda console, and hit the test button. (You don't have to configure a test event since the function doesn't use any input data).

Have a look at the logs, and verify that the function is doing what you expect it to do.

You might also want to look up your ec2 and rds instances to see they're really shut down.

For reference, you can also try running the lambda function from the command line:
```bash
aws lambda invoke --function-name "stopec2rds-$(aws sts get-caller-identity --query Arn --output text | awk -F '/' '{print $NF}')" response.txt
```






## Creating your database schema

>> Proceed once your database reports 'Available'.

In order to connect to the database and perform database operations, you'll have to connect to it. To connect, you need to use the endpoint that was created for you. 

2. Find your database endpoint in the RDS console, or by running:
```bash
aws rds describe-db-instances --query "DBInstances[*].Endpoint.Address" --output text
```

With your database endpoint, and the username and password you entered when you created, you should be able to connect to your database using ```psql```

## Postgres and psql

To administer the database, we're using a command line tool called ```psql```. ```psql``` is short for 'PostgreSQL command line tool', and comes pre-installed on your Cloudshell environment. 

1. Run the following command in your cloudshell:
```bash
psql -h yourdbinstance.abc123xyz.us-east-1.rds.amazonaws.com -U dbadmin -d orders

# replace the endpoint with the value you found in the previous step

# after you've connected, you'll be asked for a password. Use the password you used when creating the database.
```

When you've logged in successfully, you'll notice that the prompt of your shell has changed. 

```
psql (15.12, server 17.2)
WARNING: psql major version 15, server major version 17.
         Some psql features might not work.
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.

orders=>
```

This tells you you're not logged in and using a postgres session. 

Since psql behaves differently than your regular shell, we'll go over a couple of commands you'll need to know. 

1. ```\l``` - List all databases
2. ```\c``` - Connect to a database
3. ```\dt``` - List all tables in the current database
4. ```\d``` - Describe a table

You can also use ```\?``` to get a list of all available commands.

Alright, back to business. In order to ingest data into the database, we need to generate a database schema that will match the data we're ingesting.

1. Run the following psql command: 
```sql
-- Create the customers table
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY
);

-- Create the orders table
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- Create the items table
CREATE TABLE items (
    item_id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0)
);

-- Create the order details table (Many-to-Many Relationship between orders and items)
CREATE TABLE order_details (
    order_detail_id SERIAL PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    item_id INT NOT NULL,
    amount INT NOT NULL CHECK (amount > 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);
```

2. Now, we need to create a database user that AWS Glue can use when ingesting data. 
```sql
CREATE USER glue_user WITH PASSWORD 'glue_password';
GRANT ALL PRIVILEGES ON DATABASE orders TO glue_user;
```

3. And while we're at it, let's also create a user that our web app can use to access the database. 
```sql
CREATE USER web_app_user WITH PASSWORD 'web_app_password';
GRANT ALL PRIVILEGES ON DATABASE orders TO web_app_user;
```

## Lambda and Glue

For ETL, we'll use an AWS service called Glue. Matillion is currently also using Glue to run its processes (DPC has its own agents). 

Glue is a data integration service that allows you to connect and transform data between different sources (like databases, S3, and others) and store it in a database.

The ETL process definition will be stored in a Glue job. But in order for the job to run, we need a way to trigger it. So let's use an S3 trigger, that fires when a new file is added to our S3 bucket. We can use AWS Lambda to catch the event - and then in turn trigger the Glue job.

Lambda is a serverless computing service that allows you to run code without having to worry about the underlying infrastructure. It has several runtimes, among which is python. 

1. Create an AWS Lambda function that will be triggered when a new file is added to the bucket.

1. Create an AWS Glue connection to the database. 
Go to the AWS Glue Console → Connections.
Click Add Connection → Select JDBC.
Enter:
Name: glue-postgres-connection
JDBC URL:
bash
Copy
Edit
jdbc:postgresql://your-postgres-endpoint:5432/your_database
Username: your_db_user
Password: your_db_password
Select the appropriate VPC, subnet, and security group.
Click Test Connection and save.

4. Create a 