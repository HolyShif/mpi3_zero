#Kyle Shiflett
#Scans for available wifi, and returns the list of SSIDs
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
