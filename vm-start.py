#!/usr/local/bin/python
# Spins up a VM on Digital Ocean
# 
# This is based mostly on the 'tugboat' configuration, but needs an API token
# in the config, like so (in ~/.tugboat):
# 
# authentication:
#   client_key: ...
#   api_key: ...
#   token: ...
# defaults:
#   ssh_key: <identifier num>
#
# It also requires a cloudint user-data file to be supplied.

import sys
import yaml
import time
import argparse
import datetime
import digitalocean
from os.path import expanduser

home = expanduser("~")

name = "vm-%s" % datetime.date.today().strftime("%Y%m%d")

parser = argparse.ArgumentParser()
parser.add_argument('vm_name', nargs='?', default=name, metavar="VM name",
                  help="name of the VM (defaults to vm-$(date))")
parser.add_argument("-u", "--user", dest="user_data_file", metavar="file",
                    help="use the supplied user-data (cloudinit) file (default ~/.cloudinit.txt",
                    default=home + '/.cloudinit.txt')
parser.add_argument("-c", "--conf", dest="configfile", metavar="file",
                    help="specify the config file with your API token (default ~/.tugboat)",
                    default=home + '/.tugboat')
args = parser.parse_args()

# Load configuration
try:
    config = open(args.configfile, 'r').read()
except IOError:
    print "Could not read config file %s" % args.configfile
    sys.exit(1)
config = yaml.load(config)
try:
    token = config['authentication']['token']
except TypeError:
    print "Could not find \'token\' config under \'authentication\' in config file."
    sys.exit(1)
try:
    ssh_key = int(config['defaults']['ssh_key'])
except TypeError:
    print "Could not set default SSH key from config file."
    sys.exit(1)

# Load User data from file
try:
    user_data = open(args.user_data_file, 'r').read()
except IOError:
    print "Could not read user_data file %s" % args.user_data_file
    sys.exit(1)

droplet = digitalocean.Droplet(token=token,
                               name=args.vm_name,
                               region='ams3',
                               image='ubuntu-14-04-x64',
                               size_slug='512mb',
                               backups=False,
                               ssh_keys=[ssh_key],
                               user_data=user_data,
                               ipv6=True)

droplet.create()
ip = droplet.load().ip_address
while not ip:
    ip = droplet.load().ip_address
    time.sleep(1)
print ip
