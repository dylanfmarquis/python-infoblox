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
