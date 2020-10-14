#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author       : zch
@CreateTime   : 2020-09-27 15:02:34
@LastEditTime : 2020-10-14 17:19:20
@FilePath     : /monitoring/heartbeat.py
@Description  : 
''' 

import os
import socket
import time
import psutil
import subprocess
from monitoring.dingtalkbot import DingtalkChatbot
from monitoring.config import monitor

web_hook = f"https://oapi.dingtalk.com/robot/send?access_token={monitor['hook']}"
mobile = monitor["mobile"]
sleep_time = monitor["sleep_time"]     # 每多长时间检测一次服务状态
server = monitor["server"]             # 服务名称
# sleep_time = params_config.getint('check_server', 'sleep_time') 


def get_check_program_pid(process_name):
    process = subprocess.Popen(['pgrep', '-f', process_name],
                               stdout=subprocess.PIPE, shell=False)
    pid = process.communicate()[0]
    return pid

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

machine_ip = get_host_ip()

def get_pid(pid_text_path):
    with open(pid_text_path) as pid_text:
        pid_num = int(pid_text.readlines()[-1])
    return pid_num


def check_pid(pid_num):
    if psutil.pid_exists(pid_num):
        return True
    else:
        return False

def restart_server(gunicorn_server_name=''):
    start_uwsgi_cmd = f"supervisorctl restart {gunicorn_server_name}"
    os.system(start_uwsgi_cmd)
    pid_text_path = './'
    time.sleep(3)
    pid_num = get_pid(pid_text_path)
    if check_pid(pid_num):
        sendtxtmsg('{}机器 - {}服务已重新启动@所有人'.format(machine_ip, gunicorn_server_name))
    else:
        sendtxtmsg('{}机器 - {}服务启动失败@所有人'.format(machine_ip, gunicorn_server_name))

def sendtxtmsg(msg, mobile=None):
    '''
    发送文本消息
    :param msg:
    :return:
    '''
    # 初始化
    dtalk = DingtalkChatbot(web_hook)
    dtalk.send_text(msg=msg, at_mobiles=mobile)

def headbeat(serverlist, sleep_time):
    """
    心跳监控端口，定时连接对应端口
    """
    msg = "{} 机器 - {}已部署启动".format(machine_ip, "心跳监控")
    sendtxtmsg(msg)

    while True:
        for one in serverlist:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((one['ip'], one['port']))
                except socket.error as e:
                    msg = f"Server: {one['server']}, Error:{str(e)}"
                    sendtxtmsg(msg, mobile=one['mobile'])

        time.sleep(sleep_time)

def sendMsg2DD(server_name, msg_str, err_flag=False):
    '''
    @description: 服务报错信息捕获，并发送至 DD
    @param: 
    @return: 
    '''
    if err_flag:
        msg = f"机器: {machine_ip}\n服务: [{server}]-[{server_name}] 报错！！！\n, 错误信息:{msg_str}"
    else:
        msg = f"机器: {machine_ip}\n服务: [{server}]-[{server_name}] {msg_str}!"
    sendtxtmsg(msg, mobile=mobile)

if __name__ == '__main__':
    ip_address = '127.0.0.1' 
    serverlist = [{
            'ip': ip_address,
            'port': 8000,
            'mobile': ['***'],
            'server': 'server'
        }
    ]   
    headbeat(serverlist, sleep_time)