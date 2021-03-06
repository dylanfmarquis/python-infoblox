python-infoblox
====
Python module for interfacing with Infoblox using the Infoblox WAPI.

Dependancies
----
requests - http://python-requests.org

Setup
----
```bash
pip install python-infoblox
```
Initialization
----
```python

from infoblox import *
#Auth with cmd prompt, specifying the specific version
iblox = infoblox(vers='v2.6.1')

#Specify Credentials
iblox = infoblox(auth={'url':'infoblox.example.com','user':'myuser','passwd':'Secret123'}, vers='v2.6.1')

#Partial credentials can be specified as well
iblox = infoblox(auth={'url':'infoblox.example.com'})
iblox = infoblox(auth={'url':'infoblox.example.com','user':'myuser'})
```
Callback
----
```python
#The module can be instantiated with a callback for logging/debugging
def callback(error):
    print error

iblox = infoblox(callback=callback)
```
Host Record
----
```python
#Create a host record
h = iblox.host('foo.example.com')
h.add('10.1.1.12')
iblox.host('foo2.example.com').add('10.1.1.13',mac='aa:bb:cc:dd:ee')

#Query information on a specified host record
print h.fetch()

#Add an alias
h.alias().add('bar.example.com')

#Delete an alias
h.alias().delete('bar.example.com')

#Update TTL
h.update(ttl=500)

#Update MAC
h.update(mac='aa:bb:cc:dd:ee')

#Delete host record
h.delete()
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
ip = iblox.subnet('10.1.1.0/24').next_available_ip()

# Get the subnet for a particular IP address
subnet = iblox.subnet_from_ip('10.1.1.0/24')
```
Lease
----
```python
#Query discovered data for a lease
print iblox.lease('10.1.1.14').fetch(discovered_data=True)
```
A Record
----
```python
#Create A Record
a = iblox.a('foo.example.com')
a.add('10.1.1.12')

#Query information on a specified A record
print a.fetch(dns_name=True, ipv4addr=True)

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

#Query information on a specified CNAME record
print cname.fetch()

#Update TTL/Canonical
cname.update(ttl=600)
cname.update(canonical='foo.example.com')

#Delete CNAME
cname.delete()
```
MX Record
----
```python
mx = iblox.mx('mail.example.com')

#Query information on a specified MX record
print mx.fetch()
```
SRV Record
----
```python
#Add SRV record for a service that uses port 80
srv = iblox.srv('_service._tcp.example.com',80)
srv.add('server.example.com')

#Update the target of a SRV record
srv.update(target='server2.example.com')

#Update the weight and priority of a SRV record
srv.update(weight=1, priority=1)

#Delete a SRV record
srv.delete()
```
Record:RPZ:CNAME
----
```python
# Create a CNAME object to direct python-infoblox.example.com to other.example.com
cname = iblox.rpz_cname("python-infoblox.example.com")
cname.add("other.example.com",
          "zone.example.local",
          comment="This is a comment",
          view="default')

# Update the canonical name to be yetanother.example.com
cname.update(canonical="yetanother.example.com")

# Update the comment
cname.update(comment="Updated comment")

# Delete
cname.delete()
```
Unittests
----
To run the unittests, first, copy `infoblox/test/sample.config.py` to `infoblox/test/config.py`.
Then, modify the values to work for your organization.
Then, simply run the following command from inside the repository.
```bash
python -m unittest discover
```
