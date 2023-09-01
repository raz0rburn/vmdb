#!/usr/bin/env python3
"""
Written by Chris Hupman
Github: https://github.com/chupman/
Example: Get guest info with folder and host placement

"""
import json
from tools import cli, service_instance

#mysql
from mysql.connector import MySQLConnection, Error
from datetime import datetime, date, time
from ipaddress import IPv4Address
import configparser
import sys
from sys import argv
data = {}


def get_nics(guest):
    nics = {}
    for nic in guest.net:
        if nic.network:  # Only return adapter backed interfaces
            if nic.ipConfig is not None and nic.ipConfig.ipAddress is not None:
                nics[nic.macAddress] = {}  # Use mac as uniq ID for nic
                nics[nic.macAddress]['netlabel'] = nic.network
                ipconf = nic.ipConfig.ipAddress
                i = 0
                nics[nic.macAddress]['ipv4'] = {}
                for ip in ipconf:
                    if ":" not in ip.ipAddress:  # Only grab ipv4 addresses
                        nics[nic.macAddress]['ipv4'][i] = ip.ipAddress
                        nics[nic.macAddress]['prefix'] = ip.prefixLength
                        nics[nic.macAddress]['connected'] = nic.connected
                    i = i+1
    return nics


def vmsummary(summary, guest):
    vmsum = {}
    config = summary.config
    net = get_nics(guest)
    committed= 0
    uncommitted = 0 
    try:
        committed = summary.storage.committed
    except Exception: 
        committed = 0
    finally:
        try:
            uncommitted  = summary.storage.uncommitted
        except Exception: 
            uncommitted = 0
        finally:
            provisioned_space = int(committed + uncommitted) / 1024**3
    vmsum['provisioned_space'] = provisioned_space
    try:
        committed = int(summary.storage.committed) / 1024**3
    except Exception: 
            committed = 0
    vmsum['usage_storage'] = committed
    vmsum['guest_disk_usage'] = sum([int(i.capacity - i.freeSpace) for i in summary.vm.guest.disk]) / 1024**3
    try:
        vmsum['mem'] = str(config.memorySizeMB / 1024)
    except Exception: 
        vmsum['mem'] = 'null'
    vmsum['cpu'] = str(config.numCpu)
    vmsum['path'] = config.vmPathName
    vmsum['guestos_id'] = config.guestId
    vmsum['ostype'] = config.guestFullName
    vmsum['state'] = summary.runtime.powerState
    vmsum['annotation'] = config.annotation if config.annotation else ''
    vmsum['net'] = net
    if summary.guest is not None:
        ip_address = summary.guest.ipAddress
        tools_version = summary.guest.toolsStatus
        if tools_version is not None:
            vmsum['vmwtools'] = tools_version
        else:
            vmsum['vmwtools'] = 'None'

        if ip_address:
            vmsum['ip_primary'] = ip_address
        else:
            vmsum['ip_primary'] = 'None'
       # 'host name': vm.runtime.host.name,
      #     'last booted timestamp': vm.runtime.bootTime}
    try:
        vmsum['boottime'] = summary.runtime.bootTime.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        vmsum['boottime'] = 'null'
    vmsum['template'] = summary.config.template
    return vmsum


def vm2dict(datacenter, cluster, host, vm, summary):
    # If nested folder path is required, split into a separate function
    vmname = vm.summary.config.name
    data[datacenter][cluster][host][vmname]['folder'] = vm.parent.name
    data[datacenter][cluster][host][vmname]['provisioned_space'] = summary['provisioned_space']
    data[datacenter][cluster][host][vmname]['usage_storage'] = summary['usage_storage']
    data[datacenter][cluster][host][vmname]['guest_disk_usage'] = summary['guest_disk_usage']
    data[datacenter][cluster][host][vmname]['mem'] = summary['mem']
    data[datacenter][cluster][host][vmname]['cpu'] = summary['cpu']
    data[datacenter][cluster][host][vmname]['path'] = summary['path']
    data[datacenter][cluster][host][vmname]['net'] = summary['net']
    data[datacenter][cluster][host][vmname]['ostype'] = summary['ostype']
    data[datacenter][cluster][host][vmname]['state'] = summary['state']
    data[datacenter][cluster][host][vmname]['annotation'] = summary['annotation']
    data[datacenter][cluster][host][vmname]['vmwtools'] = summary['vmwtools']
    data[datacenter][cluster][host][vmname]['ip_primary'] = summary['ip_primary']
    data[datacenter][cluster][host][vmname]['boottime'] = summary['boottime']
    data[datacenter][cluster][host][vmname]['guestos_id'] = summary['guestos_id']
    data[datacenter][cluster][host][vmname]['template'] = summary['template']

    print(datacenter)
    print(cluster)
    print(host)
    print(vmname)
    print(data[datacenter][cluster][host][vmname]['net'])
    print(data[datacenter][cluster][host][vmname]['folder']) 
    print(data[datacenter][cluster][host][vmname]['provisioned_space']) 
    print(data[datacenter][cluster][host][vmname]['usage_storage']) 
    print(data[datacenter][cluster][host][vmname]['guest_disk_usage']) 
    print(data[datacenter][cluster][host][vmname]['mem'] )
    print(data[datacenter][cluster][host][vmname]['cpu'] )
    print(data[datacenter][cluster][host][vmname]['path'])
    print(data[datacenter][cluster][host][vmname]['net'])
    print(data[datacenter][cluster][host][vmname]['ostype'])
    print(data[datacenter][cluster][host][vmname]['state'])
    print(data[datacenter][cluster][host][vmname]['annotation'])
    print(data[datacenter][cluster][host][vmname]['vmwtools'])
    print(data[datacenter][cluster][host][vmname]['ip_primary'])
    print(data[datacenter][cluster][host][vmname]['boottime'])
    print(data[datacenter][cluster][host][vmname]['guestos_id'])
    print(data[datacenter][cluster][host][vmname]['template'])

def read_mysql_config(filename='/opt/vmware-api/config-mysql',section='client'):
    parser = configparser.ConfigParser()
    parser.read(filename)
    db={}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1].replace("\"","")
    else:
        raise Exception('{0} not found in the {1} file'.format(section,filename))
    return db

def vm2db(datacenter, cluster, host, vm, summary):

    mysql_config = read_mysql_config()
    conn = None
    try:
        conn = MySQLConnection(**mysql_config)
        cursor = conn.cursor()
        dateA = datetime.now()
        timeNow = dateA.strftime('%Y-%m-%d %H:%M:%S')
        dcname = datacenter
        try:
            ip_primary = int(IPv4Address(summary['ip_primary']))
        except Exception:
            ip_primary = 0

        vmname = vm.summary.config.name
        folder = vm.parent.name
        provisioned_space =  summary['provisioned_space']
        usage_storage = summary['usage_storage']
        guest_disk_usage = summary['guest_disk_usage']
        mem = summary['mem']
        
        cpu =  summary['cpu']
        path = summary['path']
        ostype =  summary['ostype']
        state = str(summary['state'])
        annotation =summary['annotation']
        vmwtools = str(summary['vmwtools'])
        boottime = summary['boottime']
        guestos_id =  summary['guestos_id']
        template = summary['template']
        try:
            cores_per_socket = vm.config.hardware.numCoresPerSocket
        except:
            cores_per_socket = 0
        try:
            sockets = int(cpu) / vm.config.hardware.numCoresPerSocket
        except:
            sockets = 0

        
        try:
            memory_overhead = int(vm.runtime.memoryOverhead)
        except:
            memory_overhead = 0
        try:
            max_cpu_usage = int(vm.runtime.maxCpuUsage)
        except:
            max_cpu_usage = 0
        try:
            max_memory_usage = int(vm.runtime.maxMemoryUsage)
        except:
            max_memory_usage = 0
        try:
            connection_state = str(vm.runtime.connectionState)
        except:
            connection_state = ''
        
        sql = "INSERT INTO vminfo (datetime, datacenter, cluster, host, vmname, folder, ip_primary, provisioned_space, guest_disk_usage, usage_storage, path, mem, cpu, cores_per_socket, sockets, ostype, state, connection_state, annotation, vmwtools, boottime, guestos_id, memory_overhead, max_cpu_usage, max_memory_usage,template) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = [(timeNow, datacenter, cluster, host, vmname, folder, ip_primary, provisioned_space, guest_disk_usage, usage_storage, path, mem, cpu, cores_per_socket, sockets, ostype, state, connection_state, annotation, vmwtools, boottime, guestos_id, memory_overhead, max_cpu_usage, max_memory_usage,template)]
        print(val)
        cursor.executemany(sql, val)
        conn.commit()

    except Error as error:
        print(error)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()

    #add DNS
    #add NIC name?

def nic2db(datacenter, cluster, host, vm, summary):

    mysql_config = read_mysql_config()
    conn = None

    dateA = datetime.now()
    timeNow = dateA.strftime('%Y-%m-%d %H:%M:%S')
    vmname = vm.summary.config.name

    #data[datacenter][cluster][host][vmname]['net'] = summary['net']
    for mac in summary['net']:
        for key in summary['net'][mac]['ipv4']:
            try:
                conn = MySQLConnection(**mysql_config)
                cursor = conn.cursor()


                print('vmname= ',vmname,'mac=',mac,'netlabel=',summary['net'][mac]['netlabel'],'ipv4=',summary['net'][mac]['ipv4'][key])
                netlabel = summary['net'][mac]['netlabel']
                prefix = summary['net'][mac]['prefix']
                connected = summary['net'][mac]['connected']
                ipv4 = summary['net'][mac]['ipv4'][key]    
                        
                sql = "INSERT INTO nicinfo (datetime, datacenter, cluster, host, vmname, mac, netlabel,prefix,connected,ipv4) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = [(timeNow, datacenter, cluster, host, vmname,mac,netlabel,prefix,connected,ipv4)]
                print(val)
                cursor.executemany(sql, val)
                conn.commit()

            except Error as error:
                print(error)
            finally:
                if conn is not None and conn.is_connected():
                    conn.close()

def data2json(raw_data, args):
    with open(args.jsonfile, 'w') as json_file:
        json.dump(raw_data, json_file)


def main():
    """
    Iterate through all datacenters and list VM info.
    """
    parser = cli.Parser()
    parser.add_custom_argument('--json', required=False, action='store_true',
                               help='Write out to json file')
    parser.add_custom_argument('--jsonfile', required=False, action='store',
                               default='getvmsbycluster.json',
                               help='Filename and path of json file')
    parser.add_custom_argument('--silent', required=False, action='store_true',
                               help='supress output to screen')
    args = parser.get_args()
    print("args=",args)
    #configfname = sys.argv[1]
    #config = configparser.ConfigParser()
    #config.read(configfname)
    #print("config=",config["VSphere"])
    si = service_instance.connect(args)
    outputjson = True if args.json else False
    content = si.RetrieveContent()
    children = content.rootFolder.childEntity
    for child in children:  # Iterate though DataCenters
        datacenter = child
        data[datacenter.name] = {}  # Add data Centers to data dict
        clusters = datacenter.hostFolder.childEntity
        for cluster in clusters:  # Iterate through the clusters in the DC
            # Add Clusters to data dict
            data[datacenter.name][cluster.name] = {}
            hosts = cluster.host  # Variable to make pep8 compliance
            for host in hosts:  # Iterate through Hosts in the Cluster
                hostname = host.summary.config.name
                # Add VMs to data dict by config name
                data[datacenter.name][cluster.name][hostname] = {}
                vms = host.vm
                for vm in vms:  # Iterate through each VM on the host
                    vmname = vm.summary.config.name
                    data[datacenter.name][cluster.name][hostname][vmname] = {}
                    summary = vmsummary(vm.summary, vm.guest)
                    print("vm2db")
                    vm2db(datacenter.name, cluster.name, hostname, vm, summary)
                    print("nic2db")
                    nic2db(datacenter.name, cluster.name, hostname,vm, summary)

    if not args.silent:
        print("json:")
        print(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))

    if outputjson:
        data2json(data, args)


# Start program
if __name__ == "__main__":
    print("main")
    main()
