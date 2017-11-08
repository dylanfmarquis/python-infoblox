import sys
import re
import unittest

from infoblox import infoblox

TEST_LOG = './unittests.log'
TEST_IP = '10.4.19.232'
TEST_IP_1 = '10.4.19.233'
TEST_SUBNET = '10.4.19.0/24'
TEST_HOST_RECORD = 'python-infoblox.example.com'
TEST_HOST_RECORD_1 = 'python-infoblox1.example.com'
TEST_CNAME = 'python-infoblox2.example.com'
TEST_MAC = 'aa:bb:cc:dd:ee:ff'
TEST_SRV = '_pytest._tcp.example.com'


def _callback(error):
    log = open(TEST_LOG, 'a')
    log.write('{0}\n'.format(error))
    log.close()


iblox = infoblox(callback=_callback)


class InfobloxTest(unittest.TestCase):
    def test_host(self):
        # Test host add
        host = iblox.host(TEST_HOST_RECORD)
        self.assertTrue(host.add(TEST_IP) == 0)

        # Test host update
        host = iblox.host(TEST_HOST_RECORD)
        self.assertTrue(host.update(ttl=500) == 0)
        self.assertTrue(host.update(mac=TEST_MAC) == 0)
        self.assertTrue(host.update(ip=TEST_IP_1) == 0)
        self.assertTrue(host.update(ip=TEST_IP, mac=TEST_MAC) == 0)

        # Test host alias
        host = iblox.host(TEST_HOST_RECORD)
        self.assertTrue(host.alias().add(TEST_CNAME) == 0)
        self.assertTrue(host.alias().delete(TEST_CNAME) == 0)

        # Test host delete
        host = iblox.host(TEST_HOST_RECORD)
        self.assertTrue(host.delete() == 200)

    def test_subnet_query(self):
        matches = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
                           iblox.subnet(TEST_SUBNET)
                                .next_available_ip(offset=1))
        next_ip = (iblox.subnet(TEST_SUBNET)
                        .next_available_ip(offset=1) is None)
        self.assertTrue(matches or next_ip)

    def test_lease_query(self):
        d = 'discovered_data'
        self.assertTrue(isinstance(iblox.lease(TEST_IP).fetch(d), list))

    def test_a(self):
        # Test a add
        self.assertTrue(
            iblox.a(TEST_HOST_RECORD).add(TEST_IP) == 0)

        # Test a update
        a = iblox.a(TEST_HOST_RECORD)
        self.assertTrue(a.update(ttl=700) == 0)
        self.assertTrue(a.update(ip=TEST_IP_1) == 0)

        # Test cname add
        cname = iblox.cname(TEST_CNAME)
        self.assertTrue(cname.add(TEST_HOST_RECORD) == 0)

        # Test cname update

        # This call is preparation for the next calls
        iblox.host(TEST_HOST_RECORD_1).add(TEST_IP)

        # Test cname update
        cname = iblox.cname(TEST_CNAME)
        self.assertTrue(cname.update(canonical=TEST_HOST_RECORD_1) == 0)
        self.assertTrue(cname.update(ttl=600) == 0)

        # Test cname delete
        cname = iblox.cname(TEST_CNAME)
        self.assertTrue(cname.delete() == 0)

        # Test a delete
        a = iblox.a(TEST_HOST_RECORD)
        self.assertTrue(a.delete() == 0)

        # Test host add mac
        host = iblox.host(TEST_HOST_RECORD)
        self.assertTrue(host.add(TEST_IP, mac=TEST_MAC) == 0)

        # Cleanup
        iblox.host(TEST_HOST_RECORD_1).delete()
        iblox.host(TEST_HOST_RECORD).delete()
        iblox.grid().restart()

    def test_srv(self):
        # Preparation for calls
        iblox.host(TEST_HOST_RECORD).add(TEST_IP)
        iblox.host(TEST_HOST_RECORD_1).add(TEST_IP_1)

        # Test srv add
        srv = iblox.srv(TEST_SRV, 5555)
        self.assertTrue(srv.add(TEST_HOST_RECORD) == 0)

        # Test srv update
        srv = iblox.srv(TEST_SRV, 5555)
        self.assertTrue(srv.update(weight=1) == 0)

        srv = iblox.srv(TEST_SRV, 5555)
        self.assertTrue(srv.update(priority=1) == 0)

        srv = iblox.srv(TEST_SRV, 5555)
        self.assertTrue(srv.update(target=TEST_HOST_RECORD_1) == 0)

        # Test srv delete
        srv = iblox.srv(TEST_SRV, 5555)
        self.assertTrue(srv.delete() == 0)

        # Cleanup
        iblox.host(TEST_HOST_RECORD).delete()
        iblox.host(TEST_HOST_RECORD_1).delete()
        iblox.grid().restart()

    def test_grid_restart(self):
        self.assertTrue(iblox.grid().restart() == 0)

    def test_rpz_cname(self):
        # TODO: Write unittests
        pass


if __name__ == "__main__":
    unittest.main()
