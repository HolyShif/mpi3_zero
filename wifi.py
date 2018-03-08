#Kyle Shiflett
#file for scanning, adding, removing, and changing wifi networks in the wpa_supplicant.conf file
#assumes WPA or WPA2

import subprocess
def scan():
	p1 = subprocess.Popen(["iwlist","wlan0","scan"],stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["grep", "-oP", "SSID:\"\K[^\"]+"],stdin=p1.stdout,stdout=subprocess.PIPE)

	p1.stdout.close()
	out,err = p2.communicate()
	essid = out.splitlines()	#split the string by line into list (each ssid on own line)
	essid = list(set(essid))	#cast as a set to remove duplicates, then back as list
	#print(essid)
	#print(len(essid))

	return essid

#bash command
#sudo iwlist wlan0 scan | grep -oP 'SSID:"\K[^"]+'

def remove(ssid):
	#wpa_f = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r+')
	try:
		wpa_f = open('/home/pi/mpi3_zero/wpa_tst.conf', 'r+')
	except:
		return -1
	#data = wpa_f.read()
	data = wpa_f.readlines()
	#print data
	
	target = '\tssid=\"' + ssid + '\"\n'	#ensures if ssid is substring of another ssid, no unintentional delete will occur
	#print target

	if not (target in data):	#if ssid not in file, return 0
		return 0
	
	st_target = "network={\n"
	end_target = "}\n"

	tar_i = 0;
	st_i = 0;
	end_i = 0;
	index = 0;

	for line in data:
        	if line == st_target:
                	st_i = index
                	#print st_i

        	#if target in data[index]:
                if line == target:
			tar_i = index
                	#print tar_i

        	if line == end_target:
                	end_i = index
                	#print end_i

        	if (st_i < tar_i) and (tar_i < end_i):
                	break

        	index += 1

	if data[st_i-1] == '\n':        #remove blank space above
        	st_i -= 1

	wpa_f.seek(0)   #reposition to start of file
	index = 0

	for line in data:
        	if (index < st_i) or (index > end_i):
                	wpa_f.write(data[index])
                	#print data[index]
        	index +=1

	wpa_f.truncate()
	wpa_f.close()
	return 1	#return success

def add(ssid, password):
	try:
                wpa_f = open('/home/pi/mpi3_zero/wpa_tst.conf', 'a+')
        except:
                return -1

	data = wpa_f.read()
	target = '\tssid=\"' + ssid + '\"\n'
	
	if target in data:        #ssid already in file, nothing to add
                return 0

	netw = ('\nnetwork={\n' + target + '\tpks=\"' + password + '\"\n' + 
		'\tkey_mgmt=WPA-PSK\n}\n')

	#print netw
	wpa_f.write(netw)
	wpa_f.close()
	return 1
