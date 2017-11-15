import re
import unittest
import infoblox


class InfobloxTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def _callback(error):
            TEST_LOG = './unittests.log'
            log = open(TEST_LOG, 'a')
            log.write('{0}\n'.format(error))
            log.close()

        cls.iblox = infoblox.infoblox(callback=_callback)
        cls.TEST_IP = '10.4.19.232'
        cls.TEST_IP_1 = '10.4.19.233'
        cls.TEST_SUBNET = '10.4.19.0/24'
        cls.TEST_HOST_RECORD = 'python-infoblox.example.com'
        cls.TEST_HOST_RECORD_1 = 'python-infoblox1.example.com'
        cls.TEST_CNAME = 'python-infoblox2.example.com'
        cls.TEST_MAC = 'aa:bb:cc:dd:ee:ff'
        cls.TEST_SRV = '_pytest._tcp.example.com'

    @classmethod
    def tearDownClass(cls):
        del(cls.iblox)

    def test_host(self):
        # Test host add
        host = self.iblox.host(self.TEST_HOST_RECORD)
        self.assertTrue(host.add(self.TEST_IP) == 0)

        # Test host update
        host = self.iblox.host(self.TEST_HOST_RECORD)
        self.assertTrue(host.update(ttl=500) == 0)
        self.assertTrue(host.update(mac=self.TEST_MAC) == 0)
        self.assertTrue(host.update(ip=self.TEST_IP_1) == 0)
        self.assertTrue(host.update(ip=self.TEST_IP, mac=self.TEST_MAC) == 0)

        # Test host alias
        host = self.iblox.host(self.TEST_HOST_RECORD)
        self.assertTrue(host.alias().add(self.TEST_CNAME) == 0)
        self.assertTrue(host.alias().delete(self.TEST_CNAME) == 0)

        # Test host delete
        host = self.iblox.host(self.TEST_HOST_RECORD)
        self.assertTrue(host.delete() == 200)

    def test_subnet_query(self):
        matches = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
                           self.iblox.subnet(self.TEST_SUBNET)
                               .next_available_ip(offset=1))
        next_ip = (self.iblox.subnet(self.TEST_SUBNET)
                       .next_available_ip(offset=1) is None)
        self.assertTrue(matches or next_ip)

    def test_lease_query(self):
        d = 'discovered_data'
        self.assertTrue(isinstance(self.iblox.lease(self.TEST_IP).fetch(d),
                                   list))

    def test_a(self):
        # Test a add
        self.assertTrue(
            self.iblox.a(self.TEST_HOST_RECORD).add(self.TEST_IP) == 0)

        # Test a update
        a = self.iblox.a(self.TEST_HOST_RECORD)
        self.assertTrue(a.update(ttl=700) == 0)
        self.assertTrue(a.update(ip=self.TEST_IP_1) == 0)

        # Test cname add
        cname = self.iblox.cname(self.TEST_CNAME)
        self.assertTrue(cname.add(self.TEST_HOST_RECORD) == 0)

        # Test cname update

        # This call is preparation for the next calls
        self.iblox.host(self.TEST_HOST_RECORD_1).add(self.TEST_IP)

        # Test cname update
        cname = self.iblox.cname(self.TEST_CNAME)
        self.assertTrue(cname.update(canonical=self.TEST_HOST_RECORD_1) == 0)
        self.assertTrue(cname.update(ttl=600) == 0)

        # Test cname delete
        cname = self.iblox.cname(self.TEST_CNAME)
        self.assertTrue(cname.delete() == 0)

        # Test a delete
        a = self.iblox.a(self.TEST_HOST_RECORD)
        self.assertTrue(a.delete() == 0)

        # Test host add mac
        host = self.iblox.host(self.TEST_HOST_RECORD)
        self.assertTrue(host.add(self.TEST_IP, mac=self.TEST_MAC) == 0)

        # Cleanup
        self.iblox.host(self.TEST_HOST_RECORD_1).delete()
        self.iblox.host(self.TEST_HOST_RECORD).delete()
        self.iblox.grid().restart()

    def test_srv(self):
        # Preparation for calls
        self.iblox.host(self.TEST_HOST_RECORD).add(self.TEST_IP)
        self.iblox.host(self.TEST_HOST_RECORD_1).add(self.TEST_IP_1)

        # Test srv add
        srv = self.iblox.srv(self.TEST_SRV, 5555)
        self.assertTrue(srv.add(self.TEST_HOST_RECORD) == 0)

        # Test srv update
        srv = self.iblox.srv(self.TEST_SRV, 5555)
        self.assertTrue(srv.update(weight=1) == 0)

        srv = self.iblox.srv(self.TEST_SRV, 5555)
        self.assertTrue(srv.update(priority=1) == 0)

        srv = self.iblox.srv(self.TEST_SRV, 5555)
        self.assertTrue(srv.update(target=self.TEST_HOST_RECORD_1) == 0)

        # Test srv delete
        srv = self.iblox.srv(self.TEST_SRV, 5555)
        self.assertTrue(srv.delete() == 0)

        # Cleanup
        self.iblox.host(self.TEST_HOST_RECORD).delete()
        self.iblox.host(self.TEST_HOST_RECORD_1).delete()
        self.iblox.grid().restart()

    def test_grid_restart(self):
        self.assertTrue(self.iblox.grid().restart() == 0)

    def test_rpz_cname(self):
        # TODO: Write unittests
        pass


if __name__ == "__main__":
    unittest.main()
