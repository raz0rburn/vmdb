#!/usr/bin/env python
"""
List Of Hosts in a Cluster
"""
from pyVim import connect
from pyVmomi import vim
import sys
import atexit
import argparse
import getpass
import ssl
import requests
#mysql
from mysql.connector import MySQLConnection, Error
from datetime import datetime, date, time
import configparser
from tools import cli, service_instance, pchelper
def get_args():
    """ Get arguments from CLI """
    parser = argparse.ArgumentParser(
        description='Arguments for talking to vCenter')

    parser.add_argument('-s', '--host',
                        required=True,
                        action='store',
                        help='vSpehre service to connect to')

    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='Username to use')

    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='Password to use')

    parser.add_argument('--cluster-name',
                        required=False,
                        action='store',
                        default=None,
                        help='Name of the cluster you wish to list the hosts')

    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass(
            prompt='Enter password')

    return args

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

def get_obj(content, vimtype, name = None):
    return [item for item in content.viewManager.CreateContainerView(
        content.rootFolder, [vimtype], recursive=True).view]

def cl2db(clusters):

    mysql_config = read_mysql_config()
    conn = None
    for cluster in clusters:
            try:
                cluster_name = cluster.name
            except:
                cluster_name = ''
            try:
                total_cpu = int(cluster.summary.totalCpu)
            except:
                total_cpu = 0
            try:
                total_memory = float(cluster.summary.totalMemory)/(1024*1024*1024)
            except:
                total_memory = 0  
            try:
                num_cpu_cores = int(cluster.summary.numCpuCores)
            except:
                num_cpu_cores = 0      
            try:
                num_cpu_threads  = int(cluster.summary.numCpuThreads)
            except:
                num_cpu_threads = 0
            try:
                num_hosts  = int(cluster.summary.num_hosts)
            except:
                num_hosts = 0
            try:
                num_eff_hosts  = int(cluster.summary.num_eff_hosts)
            except:
                num_eff_hosts = 0
            try:
                current_failover_level = int(cluster.summary.currentFailoverLevel)
            except:
                current_failover_level = -1
            try:
                num_vmotions = int(cluster.summary.numVmotions)
            except:
                num_vmotions = 0  
            try:
                usage_total_cpu = int(cluster.summary.usageSummary.totalCpuCapacityMhz)
            except:
                usage_total_cpu = 0    
            try:
                usage_total_mem = int(cluster.summary.usageSummary.totalMemCapacityMhz)
            except:
                usage_total_mem = 0
            try:
                conn = MySQLConnection(**mysql_config)
                cursor = conn.cursor()
                dateA = datetime.now()
                timeNow = dateA.strftime('%Y-%m-%d %H:%M:%S')
                hosts_list = []
                sql = "INSERT INTO clusterinfo (datetime, cluster_name, total_cpu, total_memory, num_cpu_cores, num_cpu_threads, num_hosts, num_eff_hosts, current_failover_level, num_vmotions, usage_total_cpu, usage_total_mem) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = [(timeNow, cluster_name, total_cpu, total_memory, num_cpu_cores, num_cpu_threads, num_hosts, num_eff_hosts, current_failover_level, num_vmotions, usage_total_cpu, usage_total_mem)]
                print(val)
                cursor.executemany(sql, val)
                conn.commit()
   
        
            except Error as error:
                print(error)
            finally:
                if conn is not None and conn.is_connected():
                    conn.close()


def host2db(clusters):
    mysql_config = read_mysql_config()
    conn = None    
    hosts_list = []
    for cluster in clusters:
        hosts = cluster.host
        host_count = 0
        for hosts2 in hosts:
            host_count = host_count +1
            hosts_list.append(hosts2.name)
            hostid = hosts2
            hardware=hostid.hardware
            cpuobj=hardware.cpuPkg[0]
            systemInfo=hardware.systemInfo
            memoryInfo=hardware.memorySize
            try:
                host_name = hosts2.name
            except:
                host_name = ''
            try:
                cluster_name = cluster.name
            except:
                cluster_name = ''
            cluster_name = cluster.name
            try:
                num_cpu_packages = int(hostid.hardware.cpuInfo.numCpuPackages)
            except:
                num_cpu_packages = 0
            try:
                num_cpu_cores = int(hostid.hardware.cpuInfo.numCpuCores)
            except:
                num_cpu_cores = 0
            try:
                num_cpu_threads = int(hostid.hardware.cpuInfo.numCpuThreads)
            except:
                num_cpu_packages = 0
            try:
                cpu_mhz = int(hostid.hardware.cpuInfo.hz)//1000000
            except:
                cpu_mhz = 0
            try:
                memory_size = (memoryInfo)/(1024*1024*1024)
            except:
                memory_size = 0
            try:
                bios_date = str(hardware.biosInfo.releaseDate)
            except:
                bios_date = ''
            try:
                bios_vendor = str(hardware.biosInfo.vendor)
            except:
                bios_vendor = ''
            try:
                cpu_vendor = str(cpuobj.vendor)
            except:
                cpu_vendor = ''
            try:
                cpu_desc = str(cpuobj.description)
            except:
                cpu_desc = ''
            try:
                srv_vendor = str(systemInfo.vendor)
            except:
                srv_vendor = ''
            try:
                srv_model = str(systemInfo.model)
            except:
                srv_model = ''

            print('Host: '+host_name)
            print('Cluster: '+cluster_name)
            print('num_cpu_packages: ',num_cpu_packages)
            print('num_cpu_cores: ',num_cpu_cores)
            print('num_cpu_threads: ',num_cpu_threads)
            print('cpu_mhz: ',cpu_mhz)
            print('bios_date: ',bios_date)
            print('bios_vendor: ',bios_vendor)
            print('cpu_vendor: ',cpu_vendor)
            print('cpu_desc: ',cpu_desc)
            print('srv_info: ',srv_vendor)
            print('srv_model: ',srv_model)
            print('memory_size: ',memory_size)
            try:
                conn = MySQLConnection(**mysql_config)
                cursor = conn.cursor()
                dateA = datetime.now()
                timeNow = dateA.strftime('%Y-%m-%d %H:%M:%S')
                hosts_list = []
                sql = "INSERT INTO hostinfo (datetime, host_name, cluster_name, num_cpu_packages, num_cpu_cores, num_cpu_threads, cpu_mhz, bios_date, bios_vendor, cpu_vendor, cpu_desc, srv_vendor, srv_model,memory_size) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = [(timeNow, host_name, cluster_name, num_cpu_packages, num_cpu_cores, num_cpu_threads, cpu_mhz, bios_date, bios_vendor, cpu_vendor, cpu_desc, srv_vendor, srv_model,memory_size)]
                print(val)
                cursor.executemany(sql, val)
                conn.commit()
   
        
            except Error as error:
                print(error)
            finally:
                if conn is not None and conn.is_connected():
                    conn.close()


def get_vm_info(clusters):
    hosts_list = []
    for cluster in clusters:
        print("cluster name:",cluster.name)
        print("cluster name:",cluster.summary)

        hosts = cluster.host
        host_count = 0
        for hosts2 in hosts:
            host_count = host_count +1
            hosts_list.append(hosts2.name)
            #print(hosts2.name)
            vms = hosts2.vm
            #print('Cluster: '+cluster.name)
            #print('Host: '+hosts2.name)
            #            vm_count = 0
            for vm in vms:
                print('Capability: '+ str(vm.capability))
                print('Datestore: '+ str(vm.datastore))
                #print('Config: '+ str(vm.config))
                print('Guest: '+str(vm.guest.disk))
                print('GuestDiskInfo')
                print('GuestFullName: '+str(vm.guest.guestFullName))
                print('GuestFullName')
                print('Guest: '+str(vm.guest.hostName))
                print('GuestHostName')
                print('Guest: '+str(vm.guest.ipAddress))
                print('GuestIpAddress')
                print('Guest: '+str(vm.guest.net))
                print('GuestNic')
                print('Guest: '+str(vm.resourcePool))
                print('GuestResourcePool')
                print('Guest: '+str(vm.runtime))#
                print('GuestRuntime')#
                print('Guest: '+str(vm.layout))#
                print('GuestLayout')#
                print('Guest: '+str(vm.resourcePool))
                print('GuestResourcePool')
                print('Hardware:',vm.config.hardware)

def get_host_info(clusters):
    hosts_list = []
    for cluster in clusters:
        hosts = cluster.host
        host_count = 0
        for hosts2 in hosts:
            host_count = host_count +1
            hosts_list.append(hosts2.name)
            print(hosts2.name)
            vms = hosts2.vm
            print('Cluster: '+cluster.name)
            print('Host: '+hosts2.name)
            #vm_count = 0
            hostid = hosts2
            #hostid=si.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0]
            hardware=hostid.hardware
            print(hardware.cpuInfo)
            print(hardware.biosInfo)

            cpuobj=hardware.cpuPkg[0]
            systemInfo=hardware.systemInfo
            print (cpuobj.vendor,cpuobj.description)
            print ('The server hardware is',systemInfo.vendor,systemInfo.model)
            memoryInfo=hardware.memorySize
            print ('The memory size is ',(memoryInfo)/(1024*1024*1024),'GB')
        
            try:
                cluster_name = cluster.name
            except:
                cluster_name = ''
            try:
                total_cpu = cluster.summary.totalCpu
            except:
                total_cpu = 0
            try:
                total_memory = cluster.summary.totalMemory
            except:
                total_memory = 0  
            try:
                num_cpu_cores = cluster.summary.numCpuCores
            except:
                num_cpu_cores = 0      
            try:
                num_cpu_threads  = cluster.summary.numCpuThreads
            except:
                num_cpu_threads = 0
            try:
                num_hosts  = cluster.summary.num_hosts
            except:
                num_hosts = 0
            try:
                num_eff_hosts  = cluster.summary.num_eff_hosts
            except:
                num_eff_hosts = 0
            try:
                current_failover_level = cluster.summary.currentFailoverLevel
            except:
                current_failover_level = -1
            try:
                num_vmotions = cluster.summary.numVmotions
            except:
                num_vmotions = 0  
            try:
                usage_total_cpu = cluster.summary.usageSummary.totalCpuCapacityMhz
            except:
                usage_total_cpu = 0    
            try:
                usage_total_mem = cluster.summary.usageSummary.totalMemCapacityMhz
            except:
                usage_total_mem = 0    


        print("cluster name:",cluster.name)
        print("cluster summary",cluster.summary)
        print("total_cpu:",total_cpu)
        print("total_memory:",total_memory)
        print("num_cpu_cores:",num_cpu_cores)
        print("num_cpu_threads:",num_cpu_threads)
        print("num_hosts:",num_hosts)
        print("num_eff_hosts:",num_eff_hosts)
        print("current_failover_level:",current_failover_level)
        print("num_vmotions:",num_vmotions)
        print("usage_total_cpu:",usage_total_cpu)
        print("usage_total_mem:",usage_total_mem)

        hosts = cluster.host
        host_count = 0
        for hosts2 in hosts:
            host_count = host_count +1
            hosts_list.append(hosts2.name)
            print(hosts2.name)
            vms = hosts2.vm
            print('Cluster: '+cluster.name)
            print('Host: '+hosts2.name)
            #vm_count = 0
            hostid = hosts2
            #hostid=si.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0]
            hardware=hostid.hardware
            print(hardware.cpuInfo)
            print(hardware.biosInfo)

            cpuobj=hardware.cpuPkg[0]
            systemInfo=hardware.systemInfo
            print (cpuobj.vendor,cpuobj.description)
            print ('The server hardware is',systemInfo.vendor,systemInfo.model)
            memoryInfo=hardware.memorySize
            print ('The memory size is ',(memoryInfo)/(1024*1024*1024),'GB')


def main():
    #args = get_args()
    # connect this thing
    parser = cli.Parser()
    parser.add_custom_argument('--json', default=False, action='store_true', help='Output to JSON')
    args = parser.get_args()
    si = service_instance.connect(args)
    cluster_name = 'cl3.sakha.gov.ru'
    # disconnect this thing
    atexit.register(connect.Disconnect, si)

    content = si.RetrieveContent()

    for cluster_obj in get_obj(content, vim.ComputeResource,
            cluster_name):
        if cluster_name:
            if cluster_obj.name == cluster_name:
                for host in cluster_obj.host:
                    print(host.name)
        else:
            print(cluster_obj.name)


    content = si.RetrieveContent()
    viewTypeComputeResource = [vim.ComputeResource]
    containerView = content.viewManager.CreateContainerView(content.rootFolder, viewTypeComputeResource, True)  # create container view
    clusters = containerView.view
    
    #get_host_info(clusters)
    cl2db(clusters)
    host2db(clusters)

# start this thing
if __name__ == "__main__":
    main()