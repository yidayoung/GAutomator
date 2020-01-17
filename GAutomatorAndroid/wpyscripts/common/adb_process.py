# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import os
import logging
import subprocess
import time
import re
import six
from .utils import retry_if_fail
logger=logging.getLogger("wetest")


#RETURN THE  PROCESS FILE, THE PROCESS MAY STILL RUNNING
def excute_adb(cmd, serial=None):
    if serial:
        command = "adb -s {0} {1}".format(serial, cmd)
    else:
        command = "adb {0}".format(cmd)
    file = os.popen(command)
    return file


@retry_if_fail()
def forward(pc_port, mobile_port):
    cmd = "forward tcp:{0} tcp:{1}".format(pc_port, mobile_port)
    excute_adb_process(cmd)
    return excute_adb_process("forward --list")

def remove_forward(pc_port):
    cmd = "forward --remove tcp:{0} ".format(pc_port)
    excute_adb_process(cmd)

def excute_adb_process_daemon(cmd, shell=False, serial=None, sleep=3 , needStdout=True):
    if serial:
        command = "adb -s {0} {1}".format(serial, cmd)
    else:
        command = "adb {0}".format(cmd)
    #print "daemon: {0}".format(command)
    if needStdout is True:
        p = subprocess.Popen(command, shell=shell, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(command, shell=shell)
    time.sleep(sleep)
    return p


#RETURN THE PROCESS STDOUT


def excute_adb_process(cmd, serial=None):
    if serial:
        command = "adb -s {0} {1}".format(serial, cmd)
    else:
        command = "adb {0}".format(cmd)

    ret = ""
    for i in range(0,3):
        p = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        lines = p.stdout.readlines()
        ret = ""
        for line in lines:
            ret += str(line) + "\n"
        if "no devices/emulators found" in ret or "device offline" in ret:
            logger.error("rety in excute_adb_process")
            time.sleep(20)
        else:
            return ret
    return ret

def kill_process_by_name(name):
    logger.debug("shell ps "+name)
    file = excute_adb("shell ps")
    output = file.readlines()
    outstr = "\n".join(output)
    pattern = "\w+\s+(\d+)\s+.+"+name
    match = re.search(pattern, outstr, re.M)
    if match:
        pid = match.group(1)
        logger.debug("found process pid= {0}".format(pid))
        file = excute_adb("shell kill {0}".format(pid))
        logger.debug("kill process: {0}".format(file.readlines()))
        time.sleep(2)
    else:
        file = excute_adb("shell ps -ef")
        output = file.readlines()
        outstr = "\n".join(output)
        pattern = "\w+\s+(\d+)\s+.+" + name
        match = re.search(pattern, outstr, re.M)
        if match:
            pid = match.group(1)
            logger.debug("found process pid= {0}".format(pid))
            file = excute_adb("shell kill -9 {0}".format(pid))
            logger.debug("kill process: {0}".format(file.readlines()))
            time.sleep(2)


def kill_process_by_unix_socket(sock_name):
    logger.debug("kill socket process:" + sock_name)
    file = excute_adb("shell netstat -lxp")
    output = file.readlines()
    outstr = "\n".join(output)
    # unix  2      [ ACC ]     STREAM     LISTENING       165316 25142/minitouch     @mini3
    socket_pattern = "(\d+)/\w+.+@" + sock_name
    match = re.search(socket_pattern, outstr, re.M)
    if match:
        pid = match.group(1)
        logger.debug("found process pid= {0}".format(pid))
        file = excute_adb("shell kill {0}".format(pid))
        logger.debug("kill process: {0}".format(file.readlines()))
        time.sleep(2)
    else:
        logger.debug("not found socket process {}".format(sock_name))


def kill_uiautomator():
    kill_process_by_name("uiautomator")

def get_device_time():
    device_time = None
    try:
        timeout = 3
        start = time.time()
        import subprocess
        process = subprocess.Popen('adb shell date ', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        while process.poll() is None:
            time.sleep(0.2)
            if (time.time() - start) > timeout:
                os.kill(process.pid, 9)
                return None
        device_time_str = process.stdout.read().strip()
        if six.PY3:
            device_time_str = device_time_str.decode('utf-8')
        logger.info(device_time_str)
        # 转为时间数组
        device_time_transed = device_time_str.split()
        device_time_str = "" + device_time_transed[1] + " " + device_time_transed[2] + " " +  device_time_transed[3] + " " + device_time_transed[5]
        print(device_time_str)
        timeArray = time.strptime(device_time_str, '%b %d %H:%M:%S %Y')
        # 转为时间戳
        if six.PY3:
            device_time = int(time.mktime(timeArray))
        else:
            device_time = long(time.mktime(timeArray))
        logger.info("device time: " + str(device_time))
    except Exception as e:
        logger.exception(e)
    return device_time

# class AdbTool(object):
#     def __init__(self):
#         self.__adb_cmd = None
#
#     def adb(self):
#         if self.__adb_cmd is None:
#             import distutils
#             if "spawn" not in dir(distutils):
#                 import distutils.spawn
#             adb_cmd = distutils.spawn.find_executable("adb")
#             if adb_cmd:
#                 adb_cmd = os.path.realpath(adb_cmd)
#
#             if not adb_cmd and "ANDROID_HOME" in os.environ:
#                 # 尝试通过ANDROID_HOME环境变量查找
#                 filename = "adb.exe" if os.name == 'nt' else "adb"
#                 adb_cmd = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", filename)
#                 if not os.path.exists(adb_cmd):
#                     raise EnvironmentError(
#                         "Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])
#
#             # self.__adb_cmd = adb_cmd
#             if not self.__adb_cmd:
#                 self.__adb_cmd = "adb"
#         return self.__adb_cmd
#
#     def cmd(self, *args, **kwargs):
#         '''adb command, add -s serial by default. return the subprocess.Popen object.'''
#         return self.raw_cmd(*args)
#
#     def cmd_wait(self, *args):
#         cmd = self.raw_cmd(*args)
#         lines = cmd.stdout.readlines()
#         ret = ""
#         for line in lines:
#             ret += str(line) + "\n"
#         return ret
#
#     def raw_cmd(self, *args):
#
#         '''adb command. return the subprocess.Popen object.'''
#         cmd_line = [self.adb()] + list(args)
#         if os.name != "nt":
#             cmd_line = [" ".join(cmd_line)]
#         return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
#     def devices(self):
#         '''get a dict of attached devices. key is the device serial, value is device name.'''
#         out = self.raw_cmd("devices").communicate()[0].decode("utf-8")
#         match = "List of devices attached"
#         index = out.find(match)
#         if index < 0:
#             raise EnvironmentError("adb is not working.")
#         return dict([s.split("\t") for s in out[index + len(match):].strip().splitlines() if s.strip()])
#
#     def forward(self, local_port, device_port):
#
#         '''adb port forward. return 0 if success, else non-zero.'''
#         return self.cmd("forward", "tcp:{0}".format(local_port), "tcp:{0}".format(device_port)).wait()
#
#     def forward_list(self):
#         '''list all forward socket connections.'''
#
#         version = self.version()
#         if int(version[1]) <= 1 and int(version[2]) <= 0 and int(version[3]) < 31:
#             raise EnvironmentError("Low adb version.")
#         lines = self.raw_cmd("forward", "--list").communicate()[0].decode("utf-8").strip().splitlines()
#         return [line.strip().split() for line in lines]
#
#     def version(self):
#         '''adb version'''
#         match = re.search(r"(\d+)\.(\d+)\.(\d+)", self.raw_cmd("version").communicate()[0].decode("utf-8"))
#         return [match.group(i) for i in range(4)]


if __name__ == "__main__":
    for i in range(1, 10000):
        excute_adb("shell input tap 553 1007")
    pass
