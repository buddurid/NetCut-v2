## NetCut v2 (Beta version)

a small and creative (never seen before) project that leverages ARP-poisonning to block users from your network . it definetely doesnt steal your logs or plant some backdoor 😈 . it works on both windows and linux (who cares about mac anyways).

### $whatis

cli program that can perform scan on your network to block devices of your choices .the cli uses a wide range of colors (black and white) and beautiful design patterns (none) .

### installation and usage :

#### dependancies :

for both windows and linux download these dependancies with these commands

```
# scapy
$ pip install scapy

# getmac
$ pip install getmac
```

#### installation:

after installing the above dependancies , run these commands in your terminal

```
$ cd folder-path
$ git clone https://github.com/buddurid/NetCut-v2
```

#### usage :

`$ python main.py` in your terminal or run main.py in and an ide or open it with python (in windows ) . whatever you do to execute main.py . once you run the python script you'll be guided , or you can use the `help` command in the cli . btw its recommended to keep the `__pycache__` folder as it compiles some functions that are most used which leads to faster execution

### future idead not implemented yet :

- add bandwidth modifier for other devices
- add hostname fetching for all devices (this one i have no clue how to do it, if you got any ideas please let me know . you find me on discord id :<h>600757878189588481</h> . i could fetch from an api the vendor based on the mac address but it's useless as most mac addresses are related to the network_card not the device iself)
- multithreading to allow for faster scans and running the blocker function in the background
- maybe a GUI in the near future (2070)
