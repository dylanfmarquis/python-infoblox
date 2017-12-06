import re
import unittest
import infoblox
import infoblox.test.config as config


class InfobloxTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def _callback(error):
            TEST_LOG = './unittests.log'
            log = open(TEST_LOG, 'a')
            log.write('{0}\n'.format(error))
            log.close()

        auth = {
                "url": config.URL,
                "user": config.USERNAME,
                "passwd": config.PASSWORD
               }
        cls.iblox = infoblox.infoblox(auth=auth,
                                      vers=config.VERSION,
                                      callback=_callback)

    @classmethod
    def tearDownClass(cls):
        del(cls.iblox)

    def test_host(self):
        # Test host add
        host = self.iblox.host(config.TEST_HOST_RECORD)
        self.assertTrue(host.add(config.TEST_IP) == 0)

        # Test host update
        host = self.iblox.host(config.TEST_HOST_RECORD)
        self.assertTrue(host.update(ttl=500) == 0)
        self.assertTrue(host.update(mac=config.TEST_MAC) == 0)
        self.assertTrue(host.update(ip=config.TEST_IP_1) == 0)
        self.assertTrue(host.update(ip=config.TEST_IP,
                                    mac=config.TEST_MAC) == 0)

        # Test host alias
        host = self.iblox.host(config.TEST_HOST_RECORD)
        self.assertTrue(host.alias().add(config.TEST_CNAME) == 0)
        self.assertTrue(host.alias().delete(config.TEST_CNAME) == 0)

        # Test host delete
        host = self.iblox.host(config.TEST_HOST_RECORD)
        self.assertTrue(host.delete() == 200)

    def test_subnet_query(self):
        matches = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
                           self.iblox.subnet(config.TEST_SUBNET)
                               .next_available_ip(offset=1))
        next_ip = (self.iblox.subnet(config.TEST_SUBNET)
                       .next_available_ip(offset=1) is None)
        self.assertTrue(matches or next_ip)

    def test_lease_query(self):
        d = 'discovered_data'
        lease = self.iblox.lease(config.TEST_DHCP_LEASE_IP)
        self.assertTrue(isinstance(lease.fetch(d), list))
        net = lease.fetch("network")
        self.assertTrue(net[0]['network'] == config.TEST_DHCP_LEASE_SUBNET)

    def test_a(self):
        # Test a add
        self.assertTrue(
            self.iblox.a(config.TEST_HOST_RECORD).add(config.TEST_IP) == 0)

        # Test a update
        a = self.iblox.a(config.TEST_HOST_RECORD)
        self.assertTrue(a.update(ttl=700) == 0)
        self.assertTrue(a.update(ip=config.TEST_IP_1) == 0)

        # Test cname add
        cname = self.iblox.cname(config.TEST_CNAME)
        self.assertTrue(cname.add(config.TEST_HOST_RECORD) == 0)

        # Test cname update

        # This call is preparation for the next calls
        self.iblox.host(config.TEST_HOST_RECORD_1).add(config.TEST_IP)

        # Test cname update
        cname = self.iblox.cname(config.TEST_CNAME)
        self.assertTrue(cname.update(canonical=config.TEST_HOST_RECORD_1) == 0)
        self.assertTrue(cname.update(ttl=600) == 0)

        # Test cname delete
        cname = self.iblox.cname(config.TEST_CNAME)
        self.assertTrue(cname.delete() == 0)

        # Test a delete
        a = self.iblox.a(config.TEST_HOST_RECORD)
        self.assertTrue(a.delete() == 0)

        # Test host add mac
        host = self.iblox.host(config.TEST_HOST_RECORD)
        self.assertTrue(host.add(config.TEST_IP, mac=config.TEST_MAC) == 0)

        # Cleanup
        self.iblox.host(config.TEST_HOST_RECORD_1).delete()
        self.iblox.host(config.TEST_HOST_RECORD).delete()

    def test_srv(self):
        # Preparation for calls
        self.iblox.host(config.TEST_HOST_RECORD).add(config.TEST_IP)
        self.iblox.host(config.TEST_HOST_RECORD_1).add(config.TEST_IP_1)

        # Test srv add
        srv = self.iblox.srv(config.TEST_SRV, 5555)
        self.assertTrue(srv.add(config.TEST_HOST_RECORD) == 0)

        # Test srv update
        srv = self.iblox.srv(config.TEST_SRV, 5555)
        self.assertTrue(srv.update(weight=1) == 0)

        srv = self.iblox.srv(config.TEST_SRV, 5555)
        self.assertTrue(srv.update(priority=1) == 0)

        srv = self.iblox.srv(config.TEST_SRV, 5555)
        self.assertTrue(srv.update(target=config.TEST_HOST_RECORD_1) == 0)

        # Test srv delete
        srv = self.iblox.srv(config.TEST_SRV, 5555)
        self.assertTrue(srv.delete() == 0)

        # Cleanup
        self.iblox.host(config.TEST_HOST_RECORD).delete()
        self.iblox.host(config.TEST_HOST_RECORD_1).delete()

    def test_grid_restart(self):
        self.assertTrue(self.iblox.grid().restart() == 0)

    def test_rpz_cname(self):
        # Test to make sure we can make an object; implicitly check fetch
        # method
        cname = self.iblox.rpz_cname(config.TEST_RPZ_CNAME)
        self.assertTrue(cname)
        self.assertTrue(cname.name == config.TEST_RPZ_CNAME)
        # Test to make sure that we can add data to the cname
        self.assertTrue(cname.add(config.TEST_RPZ_CANONICAL,
                                  config.TEST_RP_ZONE,
                                  comment="python-infoblox unittest",
                                  view=config.TEST_RPZ_VIEW) == 0)
        # Check to make sure everything was added properly
        j = cname.fetch()
        self.assertTrue(j['view'] == config.TEST_RPZ_VIEW)
        self.assertTrue(j['name'] ==
                        config.TEST_RPZ_CNAME + '.' + config.TEST_RP_ZONE)
        self.assertTrue(j['canonical'] == config.TEST_RPZ_CANONICAL)
        self.assertTrue(j['comment'] == 'python-infoblox unittest')

        # Check to make sure that we can update things
        self.assertTrue(cname.update(name=config.TEST_RPZ_CNAME,
                                     canonical=config.TEST_RPZ_CANONICAL_1,
                                     comment="python-infoblox unittest2") == 0)
        j = cname.fetch()
        self.assertTrue(j['view'] == config.TEST_RPZ_VIEW)
        self.assertTrue(j['name'] ==
                        config.TEST_RPZ_CNAME + '.' + config.TEST_RP_ZONE)
        self.assertTrue(j['canonical'] == config.TEST_RPZ_CANONICAL_1)
        self.assertTrue(j['comment'] == "python-infoblox unittest2")

        self.assertTrue(cname.delete() == 0)

    def test_mx(self):
        mx = self.iblox.mx(config.TEST_MX)
        self.assertTrue(mx.mail_exchanger == config.TEST_MX)


if __name__ == "__main__":
    unittest.main()
