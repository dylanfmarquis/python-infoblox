python-infoblox
====
Python module for interfacing with Infoblox using the Infoblox WAPI.

Dependancies
----
requests

Setup
----
```bash
export PYTHONPATH=$PYTHONPATH:/home/foo/python-infoblox
```
Initialization
----
```python

from infoblox import *
#Auth with cmd prompt
iblox = infoblox()

#Specify Credentials
iblox = infoblox(auth={'url':'infoblox.example.com','user':'myuser','passwd':'Secret123'})
```
Callback
----
```python
#The module can be instatiated with a callback for logging/debugging
def callback(error):
    print error

iblox = infoblox(callback=callback)
```
Host Record 
----
```python
#Create a host record
foo = iblox.host('foo.example.com')
foo.add('10.1.1.12')
iblox.host(foo2.example.com).add('10.1.1.13',mac='aa:bb:cc:dd:ee')

#Add an alias
foo.alias().add('bar.example.com')

#Delete an alias
foo.alias().delete('bar.example.com')

#Update TTL
foo.update(ttl=500)

#Update MAC
foo.update(mac='aa:bb:cc:dd:ee')

#Delete host record
foo.delete()
```
Grid
----
```python
#Grid Restart
iblox.grid().restart()
```
Subnet
----
```python
#Query next available IP for a given subnet.
ip = iblox.subnet(10.1.1.1/24).next_available_ip()
```
Lease
----
```python
#Query discovered data for a lease
print iblox.lease('10.1.1.14').fetch('discovered_data')
```
A Record
----
```python
#Create A Record
a = iblox.a('foo.example.com')
a.add('10.1.1.12')

#Update IP/MAC
a.update(ip='10.1.1.13')
a.update(mac='aa:bb:cc:dd:ee')

#Delete A Record
a.delete()
```
CNAME Record
----
```python
#Add CNAME
cname = iblox.cname('c.example.com')
cname.add('con.example.com')

#Update TTL/Canonical
cname.update(ttl=600)
cname.update(canonical='foo.example.com')

#Delete CNAME
cname.delete()
```
