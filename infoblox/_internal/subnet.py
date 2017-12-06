import json
import re


class _subnet(object):

    def __init__(self, infoblox_, subnet):
        """
        class constructor - Automatically called on class instantiation

        input   infoblox_ (object)      Parent class object
                subnet (string)         Specified subnet
        output  void (void)
        """
        self.infoblox_ = infoblox_
        if subnet is None:
            self.subnet = self.prompt()[0]
        else:
            self.subnet = subnet
        self._ref_ = self._ref()

    def _ref(self):
        """
        _ref - Get _ref for a specified subnet

        input   void (void)
        output  subnet_ref (string)     _ref ID for a subnet
        """
        resp = self.infoblox_.get('network?network={0}'.format(self.subnet))
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Error getting subnet ID for subnet {0} - Status {1}'
                    .format(self.subnet, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return json.loads(resp.text)[0]['_ref']

    def next_available_ip(self, offset=2):
        """
        next_available_ip - Get the next available IP address in a subnet.
                            The first results is always the gateway.

        input   offset (int)            Optional arg to provide address
                                        offset for
                                        networking gear/etc not accounted
                                        in IPAM
        output  ip_addr (string)        IP address
                None (null)             No free IP addresses
        """
        payload = '{{"num":{0}}}'.format(offset)
        resp = self.infoblox_.post(
                    '{0}?_function=next_available_ip'
                    .format(self._ref_), payload)
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Error retrieving next available address - Status {0}'
                    .format(resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        try:
            return json.loads(resp.text)['ips'][offset-1]
        except Exception:
            return None

    def prompt(self):
        """
        prompt - Prompt the user for a list of allowed subnets to assign
                 IP Adresses for sandboxes

        input   void (void)
        output  l_subnets (list)        list of subnets in CIDR notation
        """
        while(1):
            resp = raw_input('Enter subnet in CIDR notation (10.4.19.0/24): ')
            l_subnets = resp.split(',')
            if self.subnet_format_check(l_subnets):
                return l_subnets

    def subnet_format_check(self, l_subnets):
        """
        subnet_format_check - Checks to make sure the subnet is properly
                              formatted in CIDR notation

        input   l_subnets (list)        list of subnets in CIDR notation
        output  True (bool)             Subnets are properly formatted
                False (bool)            Subnets are not properly formatted
        """
        ip_rex = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}$")
        for subnet in l_subnets:
            if not ip_rex.match(subnet):
                print('\n{0} is not in the proper format\n'.format(subnet))
                return False
        return True
