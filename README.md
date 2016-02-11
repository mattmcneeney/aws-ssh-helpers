# AWS SSH Helpers

## Prerequisites

* Python (2.7+)
* [boto3](https://boto3.readthedocs.org/en/latest/guide/quickstart.html#installation) (e.g. `pip install boto3`)

Make sure you have set up your AWS credentials (using `aws configure`) and that you have access to all EC2 resources.

## Usage

### aws_ssh_by_hostname.py

```bash
usage: aws_ssh_by_hostname.py [-h] [--bastion user@bastion] [--public]
                              [--index i] [-p PORT]
                              user@machine

SSH into an EC2 instance via its name (tag)

positional arguments:
  user@machine          the name of the EC2 intance

optional arguments:
  -h, --help            show this help message and exit
  --bastion user@bastion
                        the name of a bastion machine to tunnel through
  --public              use the public IP of the EC2 instance (default is
                        private)
  --index i             the index of the machine if multiple machines share
                        the same Name tag
  -p PORT               the SSH port to use
```
