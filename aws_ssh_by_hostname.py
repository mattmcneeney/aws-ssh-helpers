#!/usr/bin/python

import boto3
import argparse
import subprocess
import sys

ec2 = boto3.client('ec2')

def main():
   parser = argparse.ArgumentParser(description='SSH into an EC2 instance via its name (tag)')
   parser.add_argument('--bastion', metavar='user@bastion', type=str, help='the name of a bastion machine to tunnel through')
   parser.add_argument('--public', action='store_true', help='use the public IP of the EC2 instance (default is private)')
   parser.add_argument('--index', metavar='i', type=int, help='the index of the machine if multiple machines share the same Name tag')
   parser.add_argument('-p', metavar='PORT', type=int, help='the SSH port to use')
   parser.add_argument('machine', metavar='user@machine', type=str, help='the name of the EC2 intance')
   args = parser.parse_args()

   # Split username from machine name if needed
   username = None
   if '@' in args.machine:
      username = args.machine.split('@')[0]
      machine = args.machine.split('@')[1]
   else:
      machine = args.machine

   # If a bastion machine was specified, find it's IP address
   bastion_username = None
   bastion_ip = None
   if args.bastion:
      if '@' in args.bastion:
         bastion_username = args.bastion.split('@')[0]
         bastion_machine = args.bastion.split('@')[1]
      else:
         bastion_machine = args.bastion
      bastion_ip = findInstanceByName(bastion_machine, 0, True)

   # Find the destination machine IP
   machine_ip = findInstanceByName(machine, args.index or 0, args.public)

   # Prepend username if needed
   if bastion_username:
      bastion_ip = '%s@%s' % (bastion_username, bastion_ip)
   if username:
      machine_ip = '%s@%s' % (username, machine_ip)

   # Specify port if needed
   port = None
   if args.p:
      port = '-p %s' % args.p

   # Build up the command, making sure we forward any authentication
   # agents and force pseudo-terminal allocation
   if bastion_ip:
      command = 'ssh -A -t %s %s ssh %s %s' % \
         ((port or ''), bastion_ip, (port or ''), machine_ip)
   else:
      command = 'ssh -A %s %s' % ((port or ''), machine_ip)
   print command

   # Ready to go
   subprocess.call(command, shell=True)

def findInstanceByName(name, num, usePublicIp):
   response = ec2.describe_instances(
      Filters=[{ 'Name': 'tag:Name', 'Values': [name] }]
   )
   tag = 'PrivateIpAddress'
   if usePublicIp:
      tag = 'PublicIpAddress'
   try:
      return response['Reservations'][num-1]['Instances'][0][tag]
   except Exception:
      print 'Could not find %s IP address for %s - aborting' % ((usePublicIp and 'public') or 'private', name)
      sys.exit(1)

if __name__ == '__main__':
   main()
