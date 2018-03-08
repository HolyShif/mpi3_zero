import string
import wifi

wi_name = wifi.scan()
print wi_name

print wifi.remove("SR Wireless Test")
print wifi.remove("Fake")
