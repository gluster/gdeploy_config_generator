import argparse
from collections import defaultdict
import os
import math
import pkg_resources
import pkgutil

from jinja2 import Environment, FileSystemLoader


known_vol_types = [
    'Replica with dedicated arbiter configuration',
    'Replica with chained arbiter configuration'
]

pkg_resources = pkg_resources.get_distribution('gdeploy_config_generator')
env = Environment(loader=FileSystemLoader(os.path.join(pkg_resources.location, 'gdeploy_config_generator/static')))

def replica_with_dedicated_arbiter(parser):
    """ generate gdeploy config for dedicated arbiter configuration """
    parser.add_argument('-da', '--dedicated-arbiter', required=True)
    args, options = parser.parse_known_args()
    dedicated_arbiter = args.dedicated_arbiter
    hosts = args.hosts.split(',')
    if args.devices:
        devices = args.devices.split(',')
    else:
        devices = []

    if args.host_devices:
        host_devices = args.host_devices.split(',')
    else:
        host_devices = []


    mappings = defaultdict(list)
    total_devices = 0
    if host_devices:
        for host_device in host_devices:
            host, _devices = host_device.split(':')
            for device in _devices.split('&'):
                mappings[host].append(device)
                total_devices += 1
    if devices:
        for host in hosts:
            if not mappings[host]:
                mappings[host].append(*devices)
                total_devices += len(devices)

    dedicated_arbiter_host, _devices = dedicated_arbiter.split(':')
    dedicated_arbiter_devices = []
    for device in _devices.split('&'):
        dedicated_arbiter_devices.append(device)

    mappings[dedicated_arbiter_host] = dedicated_arbiter_devices

    volumes = defaultdict(list)

    count = 0
    for host in mappings:
        if host == dedicated_arbiter_host:
            continue
        count += 1
        vol_id = math.ceil(count/2)
        volumes["volume{}".format(vol_id)].append(host+":/mnt/data1/1")
        if count % 2 == 0:
            volumes["volume{}".format(vol_id)].append(dedicated_arbiter_host+":/mnt/data{}/{}".format(vol_id, vol_id))

    template = env.get_template('2+1_replica_volume_create.conf')
    hosts.append(dedicated_arbiter_host)
    data = {
        "hosts": hosts,
        "mappings": mappings,
        "volumes": volumes
    }
    print(template.render(data))
    return True

def replica_with_chained_arbiter(args):
    """ Validate the args for chained arbiter configuration """
    raise NotImplementedError("This feature is not implemented")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interactive-mode', action='store_true')
    parser.add_argument('-v', '--volume-type', choices=known_vol_types, required=True)
    parser.add_argument('-H', '--hosts', required=True)
    parser.add_argument('-d', '--devices')
    parser.add_argument('-D', '--host-devices')
    parser.add_argument('-V', '--vol-name')
    parser.add_argument('-f', '--force-volume-creatation', action='store_true')
    # Just for testing I am calling function directly, please ignore it
    replica_with_dedicated_arbiter(parser)

if __name__ == '__main__':
    main()
