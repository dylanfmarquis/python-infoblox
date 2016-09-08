import sys
import re
import time
sys.path.append('.')
sys.path.append('../')
from infoblox import infoblox

def callback(error):
    log = open(TEST_LOG, 'a')
    log.write('{0}\n'.format(error))
    log.close()


TEST_IP = '10.4.19.234'
TEST_IP_1 = '10.4.19.233'
TEST_SUBNET = '10.4.19.0/24'
TEST_LOG = './unittests.log'
TEST_HOST_RECORD = 'python-infoblox.example.com'
TEST_HOST_RECORD_1 = 'python-infoblox1.example.com'
TEST_CNAME = 'python-infoblox2.example.com'
TEST_MAC = 'aa:bb:cc:dd:ee:ff'
TEST_SRV = '_pytest._tcp.example.com'

iblox = infoblox(callback=callback)

def test_host_add():
    count = 0
    host = iblox.host(TEST_HOST_RECORD)
    if host.add(TEST_IP) == 0:
        print("Host record creation: PASSED")
    else:
        print("Host record creation: FAILED")
        count += 1
    return count

def test_host_add_mac():
    count = 0
    host = iblox.host(TEST_HOST_RECORD)
    if host.add(TEST_IP,mac=TEST_MAC) == 0:
        print("Host record IP/MAC creation: PASSED")
    else:
        print("Host record IP/MAC creation: FAILED")
        count += 1
    return count

def test_host_update():
    count = 0
    host = iblox.host(TEST_HOST_RECORD)
    if host.update(ttl=500) == 0:
        print("Host record TTL mod: PASSED")
    else:
        print("Host record TTL mod: FAILED")
        count += 1

    if host.update(mac=TEST_MAC) == 0:
        print("Host record MAC mod: PASSED")
    else:
        print("Host record MAC mod: FAILED")
        count += 1

    if host.update(ip=TEST_IP_1) == 0:
        print("Host record IP mod: PASSED")
    else:
        print("Host record IP mod: FAILED")
        count += 1

    if host.update(ip=TEST_IP,mac=TEST_MAC) == 0:
        print("Host record IP/MAC mod: PASSED")
    else:
        print("Host record IP/MAC mod: FAILED")
        count += 1
    return count

def test_host_alias():
    count = 0
    host = iblox.host(TEST_HOST_RECORD)
    if host.alias().add(TEST_CNAME) == 0:
        print("Host record Alias add: PASSED")
    else:
        print("Host record Alias add: FAILED")
        count += 1

    if host.alias().delete(TEST_CNAME) == 0:
        print("Host record Alias delete: PASSED")
    else:
        print("Host record Alias delete: FAILED")
        count += 1
    return count

def test_host_delete():
    count = 0
    host = iblox.host(TEST_HOST_RECORD)
    if host.delete() == 200:
        print("Host record deletion: PASSED")
    else:
        print("Host record deletion: FAILED")
        count += 1
    return count

def test_grid_restart():
    count = 0
    if iblox.grid().restart() == 0:
        print("Grid restart: PASSED")
    else:
        print("Grid restart: FAILED")
        count += 1
    return count

def test_subnet_query():
    count = 0
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",iblox.subnet(TEST_SUBNET)\
                .next_available_ip(offset=1))\
                or iblox.subnet(TEST_SUBNET).next_available_ip(offset=1) is None:
        print("Subnet query: PASSED")
    else:
        print("Subnet query: FAILED")
        count += 1
    return count

def test_lease_query():
    count = 0
    if type(iblox.lease(TEST_IP).fetch('discovered_data')) == type([]):
        print("Lease query: PASSED")
    else:
        print("Lease query: FAILED")
        count += 1
    return count

def test_a_add():
    count =0
    if iblox.a(TEST_HOST_RECORD).add(TEST_IP) == 0:
        print("A record creation: PASSED")
    else:
        print("A record creation: FAILED")
        count += 1
    return count

def test_a_update():
    count = 0
    a = iblox.a(TEST_HOST_RECORD)
    if a.update(ttl=700) == 0:
        print("A record TTL mod: PASSED")
    else:
        print("A record TTL mod: FAILED")
        count += 1

    if a.update(ip=TEST_IP_1) == 0:
        print("A record IP mod: PASSED")
    else:
        print("A record IP mod: FAILED")
        count += 1
    return count

def test_a_delete():
    count = 0
    a = iblox.a(TEST_HOST_RECORD)
    if a.delete() == 0:
        print("A record deletion: PASSED")
    else:
        print("A record deletion: FAILED")
        count += 1
    return count

def test_cname_add():
    count = 0
    cname = iblox.cname(TEST_CNAME)
    if cname.add(TEST_HOST_RECORD) == 0:
        print("CNAME record creation: PASSED")
    else:
        print("CNAME record creation: FAILED")
        count += 1
    return count

def test_cname_update():
    count = 0
    cname = iblox.cname(TEST_CNAME)
    if cname.update(canonical=TEST_HOST_RECORD_1) == 0:
        print("CNAME record IP mod: PASSED")
    else:
        print("CNAME record IP mod: FAILED")
        count += 1

    if cname.update(ttl=600) == 0:
        print("CNAME record TTL mod: PASSED")
    else:
        print("CNAME record TTL mod: FAILED")
        count += 1
    return count

def test_cname_delete():
    count = 0
    cname = iblox.cname(TEST_CNAME)
    if cname.delete() == 0:
        print("CNAME record deletion: PASSED")
    else:
        print("CNAME record deletion: FAILED")
        count += 1
    return count

def test_srv_add():
    count = 0
    srv = iblox.srv(TEST_SRV, 5555)
    if srv.add(TEST_HOST_RECORD) == 0:
        print("SRV record creation: PASSED")
    else:
        print("SRV record creation: FAILED")
        count += 1
    return count

def test_srv_update():
    count = 0
    srv = iblox.srv(TEST_SRV, 5555)
    iblox.grid().restart()
    if srv.update(weight=1) == 0:
        print("SRV record weight mod: PASSED")
    else:
        print("SRV record weight mod: FAILED")
        count += 1

    srv = iblox.srv(TEST_SRV, 5555)
    if srv.update(priority=1) == 0:
        print("SRV record priority mod: PASSED")
    else:
        print("SRV record priority mod: FAILED")
        count += 1

    srv = iblox.srv(TEST_SRV, 5555)
    if srv.update(target=TEST_HOST_RECORD_1) == 0:
        print("SRV record target mod: PASSED")
    else:
        print("SRV record target mod: FAILED")
        count += 1
    return count

def test_srv_delete():
    count =0
    srv = iblox.srv(TEST_SRV, 5555)
    if srv.delete() == 0:
        print("SRV record deletion: PASSED")
    else:
        print("SRV record deletion: FAILED")
        count += 1
    return count

print('\nStarting python-infoblox Unit Test...\n')
count = 0
count += test_host_add()
count += test_host_update()
count += test_host_alias()
count += test_host_delete()
count += test_subnet_query()
count += test_lease_query()
count += test_a_add()
count += test_a_update()
count += test_cname_add()
iblox.host(TEST_HOST_RECORD_1).add(TEST_IP)
count += test_cname_update()
count += test_cname_delete()
count += test_a_delete()
count += test_host_add_mac()
iblox.host(TEST_HOST_RECORD_1).delete()
iblox.host(TEST_HOST_RECORD).delete()
iblox.grid().restart()
iblox.host(TEST_HOST_RECORD).add(TEST_IP)
iblox.host(TEST_HOST_RECORD_1).add(TEST_IP_1)
count += test_srv_add() 
count += test_srv_update() 
count += test_srv_delete()
iblox.host(TEST_HOST_RECORD).delete()
iblox.host(TEST_HOST_RECORD_1).delete()
count += test_grid_restart()
print('\nTEST COMPLETED WITH {0} ERRORS\n'.format(count))
