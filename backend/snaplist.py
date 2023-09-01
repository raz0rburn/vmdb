#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import io
#print vm to string
import configparser
from tools import cli, pchelper, service_instance
from mysql.connector import MySQLConnection, Error
import re
#for Telegram
import telebot
from requests import get
import requests
import socket
import time
from datetime import datetime, date, time
import os
import sys
#for https connection
import ssl
#VMWare lib for python
from pyVmomi import vim
from sys import argv




snapshot_data = {}
snap_text = ''
class VirtualMachine:
    def __init__(self, machine_object):
        self.vm = machine_object
        if len(self._snapshot_info())==2:
            self.snapshot_count, self.snapshot_size = self._snapshot_info()
        else:
            self.snapshot_size = self._snapshot_info()
            self.snapshot_count = "N/A"
    @property
    def name(self):
        return self.vm.name
    def size(self):
        return self.snapshot_size
    def count(self):
        return self.snapshot_count
    def _snapshot_info(self):
        try:
            disk_list = self.vm.layoutEx.file
            size = 0
            count = 0
            for disk in disk_list:
                if disk.type == 'snapshotData':
                    size += disk.size
                    count += 1
                ss_disk = re.search('0000\d\d', disk.name)
                if ss_disk:
                    size += disk.size
            return count, round((size / 1024**3),2)
        except Exception: 
            return "No_data"

    def __repr__(self):
        return "{};{};{}".format(self.name, self.snapshot_size, self.snapshot_count)



def get_all_vms(connection):
    content = connection.content
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    return [VirtualMachine(managed_object_ref) for managed_object_ref in container.view]

def get_all_vms_snap(connection):
    content = connection.content
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    return [managed_object_ref for managed_object_ref in container.view]

def get_last_snapshot(vm):
    try:
        #print(vm.snapshot.rootSnapshotList[-1].name)
        return vm.name,vm.snapshot.rootSnapshotList[-1].name
    except AttributeError:
        return None,None

def list_snapshots_recursively(snapshots,vm_name, snap_size, snap_count):
    global snap_text
    for snapshot in snapshots:
        if (snapshot.state=='poweredOff'):
            snapshot_state = '📸'
        else:
            snapshot_state = '📷'

        snap_text += " %s %s; Name: %s; Description: %s; CreateTime: %s; Size: %s GiB Count %s; \n \n" % (
                                        snapshot_state,vm_name,snapshot.name, snapshot.description,
                                        snapshot.createTime.strftime("%Y-%m-%d %H:%M:%S"), snap_size, snap_count)

        
        #print(snapshot_data)
        snapshot_data[vm_name][snapshot.name] = {}
        snapshot_data[vm_name][snapshot.name]['description'] = snapshot.description
        datetime_tmp = snapshot.createTime.strftime("%Y-%m-%d %H:%M:%S")
        snapshot_data[vm_name][snapshot.name]['createTime'] = datetime_tmp
        print(snapshot_data[vm_name][snapshot.name]['createTime'])
        snapshot_data[vm_name][snapshot.name]['snapshot.state'] = str(snapshot.state)
        list_snapshots_recursively(snapshot.childSnapshotList,vm_name,snap_size, snap_count)
        
   
    return snapshot_data,snap_text


def get_snapshots_by_name_recursively(snapshots, snapname):
    snap_obj = []
    for snapshot in snapshots:
        if snapshot.name == snapname:
            snap_obj.append(snapshot)
        else:
            snap_obj = snap_obj + get_snapshots_by_name_recursively(
                                    snapshot.childSnapshotList, snapname)
    return snap_obj


def get_current_snap_obj(snapshots, snapob):
    snap_obj = []
    for snapshot in snapshots:
        if snapshot.snapshot == snapob:
            snap_obj.append(snapshot)
        snap_obj = snap_obj + get_current_snap_obj(
                                snapshot.childSnapshotList, snapob)
    return snap_obj


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

def get_db_iteration():
    mysql_config = read_mysql_config()
    conn = None
    
    
    try:
        conn = MySQLConnection(**mysql_config)
        cursor = conn.cursor()
        dateA = datetime.now()
        timeNow = dateA.strftime('%Y-%m-%d %H:%M:%S')
           
        sql = "SELECT iteration FROM snapinfo ORDER BY id DESC LIMIT 1"
         
        cursor.execute(sql)
        result = cursor.fetchone()
        iteration = int(result[0])
        print(iteration)
        return iteration
    except Error as error:
        print(error)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()

def snap_to_db(dc_name, vm_name,snap_name, snap_description, snap_size,snap_count,snap_createtime,snap_state,iteration):
    mysql_config = read_mysql_config()
    conn = None
    try:
        conn = MySQLConnection(**mysql_config)
        cursor = conn.cursor()
        dateA = datetime.now()
        timeNow = dateA.strftime('%Y-%m-%d %H:%M:%S')
        


                
        sql = "INSERT INTO snapinfo (datetime, vm_name, dc_name,snap_name, snap_description, snap_size, snap_count, snap_createtime,snap_state,iteration) VALUES (  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = [(timeNow, vm_name, dc_name, snap_name,snap_description, snap_size,snap_count, snap_createtime,snap_state, iteration+1)]
        print(val)
        cursor.executemany(sql, val)
        conn.commit()

    except Error as error:
        print(error)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()

def send_to_telegram(config,message):

    apiToken = config["Telegram"]["TOKEN"]
    chatID = config["Telegram"]["chat_id"]
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    print(apiURL)
    while True:
        try:
            response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
            print(response.text)
            break
        except Exception as e:
            print(e)
            import time
            time.sleep(60)


def main():

    
    configfname = sys.argv[2]
    dc_name = sys.argv[1]
    print(configfname)
    config = configparser.ConfigParser()
    #config.read("/opt/vmware-api/config.txt")
    config.read(configfname)
    bot = telebot.TeleBot(config["Telegram"]["TOKEN"])
    iteration = get_db_iteration()

    try:
        from pyVim.connect import SmartConnect
    except ImportError:
        from pyvim.connect import SmartConnect


    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE

    connection = SmartConnect(**config["VSphere"],sslContext=s)
    str_buf = io.StringIO()
    vm_full_list = list()
    print("date name size count")
    #full list of virtual machines creation 
    for virtual_machine in get_all_vms(connection):
        vm_element = list()
        vm_size = virtual_machine.snapshot_size
        vm_name = virtual_machine.name
        vm_count = virtual_machine.snapshot_count
        vm_element.append(vm_name)
        vm_element.append(vm_size)
        vm_element.append(vm_count)
        vm_full_list.append(vm_element)
    

    content = connection.RetrieveContent()
    #iterate list of VMs for snapshot
    for vm in get_all_vms_snap(connection):
        vm_name,vm_last_snapshot = get_last_snapshot(vm)
        #print("get_all_vms_snap",vm_name)
        #print("vm_last_snapshot",vm_last_snapshot)
        if vm_last_snapshot != None: 
            for vm_element in vm_full_list:
                if vm_name == vm_element[0]:
                    print("📸",vm_element[0],"'",vm_last_snapshot,"';","Size:",vm_element[1],"Mb;","Count:",vm_element[2],file=str_buf)
                    
                    vm_obj  = pchelper.get_obj(content, [vim.VirtualMachine], str(vm_name))
                    snapshot_data[str(vm_obj.name)] = {}
                    snapshot_paths,snap_text = list_snapshots_recursively(vm.snapshot.rootSnapshotList,str(vm_obj.name),vm_element[1],vm_element[2])
                    for snapshot in snapshot_paths:
                        print(snapshot)
                        snap_to_db(dc_name, vm_name,vm_last_snapshot,snapshot_data[vm_name][vm_last_snapshot]['description'],vm_element[1],vm_element[2],snapshot_data[vm_name][vm_last_snapshot]['createTime'],snapshot_data[vm_name][vm_last_snapshot]['snapshot.state'],iteration)



    print(str_buf.getvalue())
    if str_buf.getvalue() != "":
        print('📝'+' '+dc_name+chr(10)+snap_text)
        send_to_telegram(config,'📝'+' '+dc_name+chr(10)+snap_text)
    else:
        print('📷 '+dc_name+"🎉Снапшотов нет!")
        send_to_telegram(config,'📷 '+dc_name+"🎉Снапшотов нет!")

    str_buf.close()
    print(snapshot_data)
# Start program
if __name__ == "__main__":
    print("main")
    main()