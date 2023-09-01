#!/usr/bin/env python
# William Lam
# www.virtuallyghetto.com

"""
vSphere Python SDK program for listing all ESXi datastores and their
associated devices
"""
from mysql.connector import MySQLConnection, Error
from datetime import datetime, date, time
import json
from pyVmomi import vmodl, vim
from tools import cli, service_instance, pchelper

import configparser

from pprint import pprint
#global dict
ds_dict = {}
host_list = []
# http://stackoverflow.com/questions/1094841/



def to_dict1(esxihost_name,host_fs):
    #print(esxihost_name,host_fs.volume.name)
    """
    Prints the host file system volume info

    :param host_fs:
    :return:
    """

    if host_fs.volume.name not in ds_dict:
        ds_dict[host_fs.volume.name]= {}
        ds_dict[host_fs.volume.name]['hosts'] = []
    if esxihost_name not in ds_dict[host_fs.volume.name]:
        ds_dict[host_fs.volume.name]['hosts'].append(esxihost_name)

    ds_dict[host_fs.volume.name]['ds_name'] = host_fs.volume.name
    ds_dict[host_fs.volume.name]['UUID'] = host_fs.volume.uuid
    ds_dict[host_fs.volume.name]['vmfs_version'] = host_fs.volume.version
    ds_dict[host_fs.volume.name]['is_local_vmfs'] = host_fs.volume.local
    ds_dict[host_fs.volume.name]['SSD'] = host_fs.volume.ssd

    #print("dict1=",ds_dict)



def to_dict2(ds_obj):

    summary = ds_obj.summary
    ds_capacity = summary.capacity
    ds_freespace = summary.freeSpace
    ds_uncommitted = summary.uncommitted if summary.uncommitted else 0
    ds_provisioned = ds_capacity - ds_freespace + ds_uncommitted
    ds_overp = ds_provisioned - ds_capacity
    ds_overp_pct = (ds_overp * 100) / ds_capacity \
        if ds_capacity else 0

    #print(esxihost_name,summary.name)
    if summary.name not in ds_dict:
        ds_dict[summary.name]= {}
        ds_dict[summary.name]['hosts'] = []



    ds_dict[summary.name]['URL'] = summary.url
    ds_dict[summary.name]['capacity'] = int(ds_capacity) / 1024**3
    ds_dict[summary.name]['free_space'] = int(ds_freespace) / 1024**3
    ds_dict[summary.name]['uncommitted'] = int(ds_uncommitted) / 1024**3
    ds_dict[summary.name]['provisioned'] = int(ds_provisioned) / 1024**3
    if ds_overp > 0:
        ds_dict[summary.name]['ds_overp'] = int(ds_overp) / 1024**3
        ds_dict[summary.name]['ds_overp_pct'] = int(ds_overp_pct)/ 1024**3
    ds_dict[summary.name]['hosts_quantity'] = format(len(ds_obj.host))
    ds_dict[summary.name]['vm_quantity'] = format(len(ds_obj.vm))
    #print("dict2=",ds_dict)

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

def dict_to_db():
    mysql_config = read_mysql_config()
    conn = None

    dateA = datetime.now()
    timeNow = dateA.strftime('%Y-%m-%d %H:%M:%S')
    
    

    for ds_name in ds_dict:
            try:
                
                conn = MySQLConnection(**mysql_config)
                cursor = conn.cursor()


                if 'UUID' in ds_dict[ds_name]:
                    
                    UUID = ds_dict[ds_name]['UUID']
                else:
                    UUID = ''
                if 'vmfs_version' in ds_dict[ds_name]:
                    vmfs_version = ds_dict[ds_name]['vmfs_version']
                else:
                    vmfs_version = '' 
                if 'is_local_vmfs' in ds_dict[ds_name]:
                    is_local_vmfs = ds_dict[ds_name]['is_local_vmfs']
                else:
                    is_local_vmfs = False 
                if 'SSD' in ds_dict[ds_name]:
                    SSD = ds_dict[ds_name]['SSD']
                else:
                    SSD = False
                if 'URL' in ds_dict[ds_name]:
                    URL = ds_dict[ds_name]['URL']
                else:
                    URL = ''

                if 'capacity' in ds_dict[ds_name]:
                    capacity = ds_dict[ds_name]['capacity']
                else:
                    capacity = 0
                if 'free_space' in ds_dict[ds_name]:
                    free_space = ds_dict[ds_name]['free_space']
                else:
                    free_space = 0
                if 'uncommitted' in ds_dict[ds_name]:
                    uncommitted = ds_dict[ds_name]['uncommitted']
                else:
                    uncommitted = 0

                if 'provisioned' in ds_dict[ds_name]:
                    provisioned = ds_dict[ds_name]['provisioned']
                else:
                    provisioned = 0
                
                if 'hosts_quantity' in ds_dict[ds_name]:
                    hosts_quantity = ds_dict[ds_name]['hosts_quantity']
                else:
                    hosts_quantity = 0
                if 'vm_quantity' in ds_dict[ds_name]:
                    vm_quantity = ds_dict[ds_name]['vm_quantity']
                else:
                    vm_quantity = 0
                
                
                        
                sql = "INSERT INTO dsinfo (datetime, ds_name, UUID, vmfs_version, is_local_vmfs, SSD, URL,capacity,uncommitted,provisioned,free_space, hosts_quantity,vm_quantity) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = [(timeNow, ds_name, UUID, vmfs_version, is_local_vmfs, SSD, URL,capacity,uncommitted,provisioned, free_space, hosts_quantity,vm_quantity)]
                print(val)
                cursor.executemany(sql, val)
                conn.commit()

            except Error as error:
                print(error)
            finally:
                if conn is not None and conn.is_connected():
                    conn.close()


            try:
                conn = MySQLConnection(**mysql_config)
                cursor = conn.cursor()
                i = 0;
                if ds_dict[ds_name]['hosts']:
                    while i<len(ds_dict[ds_name]['hosts']):
                        esxihost_name = ds_dict[ds_name]['hosts'][i]
                        sql = "INSERT INTO dshostinfo (datetime, ds_name, esxihost_name) VALUES ( %s, %s, %s)"
                        val = [(timeNow, ds_name, esxihost_name)]
                        print(val)
                        cursor.executemany(sql, val)
                        conn.commit()
                        i+=1;
            except Error as error:
                print(error)
            finally:
                if conn is not None and conn.is_connected():
                    conn.close()

def main():
    """
   Simple command-line program for listing all ESXi datastores and their
   associated devices
   """
    
    parser = cli.Parser()
    parser.add_custom_argument('--json', default=False, action='store_true', help='Output to JSON')
    args = parser.get_args()
    si = service_instance.connect(args)

    try:

        content = si.RetrieveContent()
        # Search for all ESXi hosts
        objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.HostSystem],
                                                          True)
        esxi_hosts = objview.view
        objview.Destroy()

        datastores = {}
        for esxi_host in esxi_hosts:
            if not args.json:
                
                print("{}\t{}\t\n".format("ESXi Host:    ", esxi_host.name))

            # All Filesystems on ESXi host
            storage_system = esxi_host.configManager.storageSystem
            host_file_sys_vol_mount_info = \
                storage_system.fileSystemVolumeInfo.mountInfo

            datastore_dict = {}
            # Map all filesystems
            for host_mount_info in host_file_sys_vol_mount_info:
                # Extract only VMFS volumes


                if host_mount_info.volume.type == "VMFS":

                    extents = host_mount_info.volume.extent
                    if not args.json:
                        print
                                                
                    else:
                        datastore_details = {
                            'uuid': host_mount_info.volume.uuid,
                            'capacity': host_mount_info.volume.capacity,
                            'vmfs_version': host_mount_info.volume.version,
                            'local': host_mount_info.volume.local,
                            'ssd': host_mount_info.volume.ssd
                        }

                    extent_arr = []
                    extent_count = 0
                    for extent in extents:
                        if not args.json:
                            #print("{}\t{}\t".format("Extent[" + str(extent_count) + "]:",extent.diskName))
                            extent_count += 1
                        else:
                            # create an array of the devices backing the given
                            # datastore
                            extent_arr.append(extent.diskName)
                            # add the extent array to the datastore info
                            datastore_details['extents'] = extent_arr
                            # associate datastore details with datastore name
                            datastore_dict[host_mount_info.volume.name] = \
                                datastore_details
                    if not args.json:
                        print
                    print(esxi_host.name,host_mount_info.volume.name)
                    host_list.append(esxi_host.name)
                    to_dict1(esxi_host.name,host_mount_info)

            # associate ESXi host with the datastore it sees
            datastores[esxi_host.name] = datastore_dict

        if args.json:
            print(json.dumps(datastores))

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1


    parser = cli.Parser()
    parser.add_optional_arguments(cli.Argument.DATASTORE_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)

    content = si.RetrieveContent()
    # Get list of ds mo
    datastore = pchelper.search_for_obj(content, [vim.Datastore], args.datastore_name)
    if datastore:
        ds_obj_list = [datastore]
    else:
        ds_obj_list = pchelper.get_all_obj(content, [vim.Datastore])
    for ds in ds_obj_list:
            to_dict2(ds)
    pprint(ds_dict)
    dict_to_db()
    return 0


# Start program
if __name__ == "__main__":
    main()
