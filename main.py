import string
import wifi

wi_name = wifi.scan()
print wi_name

#wpa_f = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r+')
wpa_f = open('/home/pi/mpi3_zero/wpa_tst.conf', 'r+')
data = wpa_f.read()

#print data
print (string.count(data,"SR Wireless"))

wpa_f.close()
