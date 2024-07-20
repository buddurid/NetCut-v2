from helper import *



def parse_targets(args,devices): # 1 2 1-5 all
    res=[]
    n=len(devices)
    for choice in args:
        if choice.isdigit():
            if 0<=int(choice)<n:
                res.append(devices[int(choice)])
        elif "-" in choice and choice.count("-")==1:
            a,b=choice.split("-")
            if a.isdigit() and b.isdigit():
                for i in range(int(a),int(b)+1):
                    res.append(devices[i])
        elif choice=="all":
            return devices
    return list(set(res))
        
        
def start(devices,router):
    printcolor("do you want to use the devices saved from last time , otherwise we will make a scan that takes from 1-2 minutes . do you want to use the devices already saved ? (y/n) : ")
    res=input()
    if res=="y" or res=="Y" or res=="yes" or res=="YES":
        devices,_=read_logs()
        if len(devices)==0:
            error("log file is empty . a scan will be taken place for 1-2 minutes")
            devices=get_devices(max=25)
    else:
        devices=get_devices(max=25)
        

    #show()
    return devices,get_router(devices,router)

                        
def get_command():
    printcolor(">> ")
    inp=input().strip()
    return parse_args(inp)
def help():
    printcolor("available commands:\n\n")
    ask("\t show : prints devices present in your network\n\n")
    ask("\t rename : gives a description to a mac address that will be saved which will help you identifying the devices\n")
    success("\t\t example usage : rename 5c:fb:3a:99:f0:a0 mom's-phone")
    ask("\t refresh : performs a new scan for all devices connected tou your network\n\n")  
    ask("\t block : blocks devices from your network based on their index when you run show command\n\n")  
    success("\t\t accepted formats : 0 (for single index)  , 1-3 (devices from index 1 to 3 will be blocked (3 included ))  , all (blocks all devices (except yours ofc))") 
    success("\t\t example usage : block 1-5   : blocks from 1 to 5")
    success("\t\t example usage : block 1 4 2   : blocks devices 1 ,4 and 2 ")
    success("\t\t example usage : block all   : blocks all devices")
    success("\t\t example usage : block 1 2 4-6   : blocks 1,2,4,5,6\n\n")    
    ask("\t save : saves all ip's , mac addresses and their description for future usage if you want to avoid scans\n\n")

def refresh():
    return get_devices()

def rename(args,devices,router): # mac , description
    if len(args)<2:
        error("not enough arguments (2 arguments needed)")
        return
    mac=args[0]
    des=args[1]
    cond=False
    for device in devices:
        if device.mac==mac:
            device.desc=des
            cond=True
            break
    if cond:
        save_mac(mac,des)
        success("rename done")    
    else:
        error("the mac address you provided isnt of any device in your network do you want to force-save it ? (y/n) :")
        res=input(">>>>>")
        if res=="y" or res=="Y" or res=="yes" or res=="YES":
            save_mac(mac,des)
        else : 
            error("wasnt saved")

            
            
def block(targets,devices,router):
    targets=parse_targets(targets,devices)
    if len(targets):
        block_devices(targets,router)
    else : 
        error("no devices were chosen")
        return
def show(devices):

    for i,device in enumerate(devices):
        print(i," : ",str(device))


def save(devices):
    write_logs(devices)

    

    