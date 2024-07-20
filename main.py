from helper import *
from cli import *

router=None
devices=None

if  __name__ == '__main__':
    try :
        devices,router=start(devices,router)
        while True:

            command , * args= get_command()
            match command:
                case "help":
                    help()
                case "refresh":
                    devices=refresh()
                case "rename":
                    rename(args,devices,router)
                case "block":
                    block(args,devices,router)
                case "show":
                    show(devices)
                case "save":
                    save(devices)  
                case "exit":
                    printcolor("bye bye")
                    write_logs(devices)
                    exit()
    except KeyboardInterrupt:
        printcolor("bye bye")
        write_logs(devices)
        exit()
    finally :
        error("error occured , please restart the program , dont worry the devices are saved")
        write_logs(devices)
        exit()
        
        