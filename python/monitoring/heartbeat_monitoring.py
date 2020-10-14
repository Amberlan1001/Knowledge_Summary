
import os
import socket
import time
import psutil
import subprocess
import dingtalk_chatbot
from config_load import params_config


web_hook = params_config.get('check_server', 'web_hook') # dingding 报警群web_hook id
sleep_time = params_config.getint('check_server', 'sleep_time') # 每多长时间检测一次服务状态
server_name = params_config.get("check_server", "server_name") # 服务名称
start_uwsgi_cmd = params_config.get("check_server", "start_uwsgi_cmd") # 启动uwsgi. 这里是uwsgi uwsgi.ini


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


def restart_server():
    os.system(start_uwsgi_cmd)
    pid_text_path = params_config.get("check_server", "pid_text_path")
    time.sleep(3)
    pid_num = get_pid(pid_text_path)
    if check_pid(pid_num):
        chat_bot.send_text('{}机器 - {}服务已重新启动@所有人'.format(machine_ip, server_name))
    else:
        chat_bot.send_text('{}机器 - {}服务启动失败@所有人'.format(machine_ip, server_name))


if __name__ == '__main__':
    chat_bot = dingtalk_chatbot.DingtalkChatbot(web_hook)
    machine_ip = get_host_ip()
    msg = "{} 机器 - {}已部署启动".format(machine_ip, server_name)
    time.sleep(3)
    chat_bot.send_text(msg)
    while True:
        pid_text_path = params_config.get("check_server", "pid_text_path")
        pid_num = get_pid(pid_text_path)
        result = check_pid(pid_num)
        if result:
            msg = '{}机器 - {}服务正常运行，请放心！'.format(machine_ip, server_name)
            chat_bot.send_text(msg)
        else:
            msg = '{}机器 - {}服务挂了！ 正在重启...@所有人'.format(machine_ip, server_name)
            chat_bot.send_text(msg)
            restart_server()
        time.sleep(sleep_time)
