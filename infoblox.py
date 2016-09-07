"""
    python-infoblox - Infoblox WAPI module
    Copyright (C) 2016

    Author: Dylan F Marquis (dylanfmarquis@dylanfmarquis.com)
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__version__ = '0.2'
__author__ = 'Dylan F Marquis'


import requests
import base64
import getpass
import re
import warnings
import json
from time import strftime as date


# Infoblox Network Management
class infoblox(object):

    def __caller__(self, error, errno):
        """
        __caller__ - Wrapper for error callback function

        input   error (string)      Error description to provide to callback
                errno (int)         Status code of API call
        output  callback (funct)    Calls callback function and passes error string
                errno (int)         Status code of API call (if no callback is specified)
        """
        if self.callback is not None:
            return self.callback(error)
        return int(errno)


    def __init__(self, callback=None, auth={}, vers='v1.7.1'):
        """
        class constructor - Automatically called on class instantiation

        input   callback (funct)    An optional callback can be passed at instantiation for error
                                    and logging purposes
        output  void (void)
        """
        self.callback = callback
        self.vers = vers
        l_ret = self.auth(auth)
        self.url = l_ret[0]
        self.creds = l_ret[1]


    def __del__(self):
        """
        class destructor - Invalidates the cookie on Infoblox side to effectively logout the user
        input   void (void)
        output  void (void)
        """
        self.post('logout','')


    def auth(self, auth):
        """
        auth - Authenticate to the Infoblox WAPI

        input   void (void)
        output  ret (list)  elements
                                0 - Infoblox WAPI URL
                                1 - Base64 encoded Infoblox username and password
        """
        while(1):
            if auth.get('url'):
                url = auth['url']
            else:
                url = raw_input('Infoblox URL: ')
            if auth.get('user'):
                user = auth['user']
            else:
                user = raw_input('Infoblox Username: ')
            if auth.get('passwd'):
                passwd = auth['passwd']
            else:
                passwd = getpass.getpass()
            creds = base64.b64encode('{0}:{1}'.format(user, passwd))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                resp = requests.get('https://{0}/wapi/{1}/record:host?name~={0}'\
                                    .format(url, self.vers),
                                    headers={'Authorization': 'Basic {0}'.format(creds),
                                             'Accept': 'application/xml'},
                                    verify=False)
                if resp.status_code == 200:
                    ret = []
                    ret.append(url)
                    ret.append(creds)
                    return ret
                else:
                    print('\nInvalid credentials\n')


    def get(self, query):
        """
        get - Send GET request to Infoblox WAPI

        input   query (string)  Directory location of API call - path after /api/ in URL
        output  resp (struct)   API HTTP response, including status code
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return requests.get('https://{0}/wapi/{1}/{2}'\
                                .format(self.url, self.vers, query),
                                headers={'Authorization' : 'Basic {0}'.format(self.creds),
                                         'Accept' :'application/json'},
                                verify=False)


    def post(self, api_function, payload):
        """
        post - Send POST request to Infoblox WAPI

        input   api_function (string)   Function to call in WAPI
                payload (string)        Payload for the POST request
        output  resp (struct)           WAPI HTTP response, including status code
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return requests.post('https://{0}/wapi/{1}/{2}'\
                                 .format(self.url, self.vers, api_function),
                                 data=payload, headers={'Authorization' : 'Basic {0}'\
                                .format(self.creds)},
                                 verify=False)


    def put(self, api_function, payload):
        """
        put - Send PUT request to Infoblox WAPI

        input   api_function (string)   Function to call in WAPI
                payload (string)        Payload for the PUT request
        output  resp (struct)           WAPI HTTP response, including status code
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return requests.put('https://{0}/wapi/{1}/{2}'\
                                .format(self.url, self.vers, api_function),
                                data=payload, headers={'Authorization' : 'Basic {0}'\
                                .format(self.creds)},
                                verify=False)


    def delete(self, api_function):
        """
        delete - Send DELETE request to Infoblox WAPI

        input   api_function (string)   Function to call in WAPI
        output  resp (struct)           WAPI HTTP response, including status code
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return requests.delete('https://{0}/wapi/{1}/{2}'\
                                   .format(self.url, self.vers, api_function),
                                   headers={'Authorization' : 'Basic {0}'.format(self.creds)},
                                   verify=False)


    def host(self, hostname=None):
        """
        host - host object

        input   hostname (string)   DNS name for host record
        output  handle (handle)     Reference to host object
        """
        handle = self._host(self, hostname)
        return handle


    def grid(self):
        """
        grid - grid object

        input   void (void)
        output  handle (handle)     Reference to grid object
        """
        handle = self._grid(self)
        return handle


    def subnet(self, subnet=None):
        """
        subnet - subnet object

        input   subnet (string)     Specified subnet
        output  handle (handle)     Reference to subnet object
        """
        handle = self._subnet(self, subnet)
        return handle


    def lease(self, address):
        """
        lease - lease object

        input   address (string)    IP address of lease
        output  handle (handle)     Reference to lease object
        """
        handle = self._lease(self, address)
        return handle


    def a(self, name):
        """
        a - A record object

        input   name (string)       DNS name of an A record
        output  handle (handle)     Reference to A record object
        """
        handle = self._a(self, name)
        return handle


    def cname(self, name):
        """
        cname - CNAME record object

        input   name (string)       Domain name of CNAME
        output  handle (handle)     Reference to CNAME object
        """
        handle = self._cname(self, name)
        return handle

    
    def mx(self, name):
        """
        mx - MX record (Mail Exchanger) object

        input   name (string)       Domain name of MX record
        output  handle (handle)     Reference to record:mx object
        """
        handle = self._mx(self, name)
        return handle

    def srv(self, name, port):
        """
        srv - SRV record object

        input   name (string)       Domain name of SRV
                port (int)          Port number of service
        output  handle (handle)     Reference to SRV record object
        """
        handle = self._srv(self, name, port)
        return handle


    class _host(object):


        def __init__(self, infoblox_, hostname):
            """
            class constructor - Automatically called on class instantiation

            input   hostname (string)   Hostname to specify Infoblox host record
                    infoblox_ (object)  Parent class object
            output  void (void)
            """
            self.infoblox_ = infoblox_
            if hostname != None:
                self.hostname = hostname
                self._ref = self._ref()


        def _ref(self):
            """
            _ref - Get _ref for a specified host record

            input   void (void)
            output  host _ref           _ref ID for a host record
            """
            try:
                return self.fetch()['_ref']
            except Exception as e:
                return None


        def fetch(self):
            """
            fetch - Retrieve all information from a specified host record

            input   void (void)
            output  resp (parsed json)  Parsed JSON response
            """
            resp = self.infoblox_.get('record:host?name~={0}'.format(self.hostname))
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__('Could not retrieve host _ref for {0}'\
                                                     ' - Status {1}'\
                                                     .format(self.hostname, resp.status_code),
                                                     resp.status_code)
                except Exception as e:
                    return resp.status_code
            try:
                return json.loads(resp.text)[0]

            except(ValueError,IndexError) as e:
                return None


        def add(self, ip, mac=None):
            """
            add - Create a host record within Infoblox

            input   ip (string)         IP address to create host record
                    mac (string)        MAC address to attach to host record
            output  0 (int)             Successful creation
                    errno (int)         Error code of API call
            """
            if mac != None:
                payload = '{{"name":"{0}", "ipv4addrs":[ {{"ipv4addr":"{1}","mac":"{2}"}}]}}'\
                          .format(self.hostname, ip, mac)
            else:
                payload = '{{"name":"{0}", "ipv4addrs":[ {{"ipv4addr":"{1}"}}]}}'\
                          .format(self.hostname, ip, mac)
            resp = self.infoblox_.post('record:host',payload)
            if resp.status_code != 201:
                try:
                    return self.infoblox_.__caller__('Error creating host record {0} for {1}'\
                                                     ' - Status: {2}'\
                                                     .format(ip, self.hostname, resp.status_code),
                                                     resp.status_code)
                except Exception as e:
                    return resp.status_code
            return 0


        def delete(self):
            """
            del - Delete a host record within Infoblox

            input   void (void)
            output  0 (int)             Successful creation
                    errno (int)         Error code of API call
            """
            resp = self.infoblox_.delete(self._ref)
            if resp.status_code != 201:
                try:
                    return self.infoblox_.__caller__('Error creating host record {0} for {1}'\
                                                     ' - Status: {2}'\
                                                     .format(self.hostname, resp.status_code),
                                                     resp.status_code)
                except Exception as e:
                    return resp.status_code
            return 0


        def update(self,ip=None,mac=None,ttl=None):
            """
            update - Update a Host record with new attributes

            input   ip (string)         Optional: IP address of a host record
                    ttl (int)           Optional: MAC address of a host record
            output  0 (int)             Success
            """
            if ttl != None:
                payload = '{{"ttl": {0}}}'.format(ttl)
                resp = self.infoblox_.put(self._ref, payload)
                if resp.status_code != 200:
                    try:
                        return self.infoblox_.__caller__('Error updating host record {0}'\
                                                         '- Status: {1}'\
                                                         .format(self.hostname, resp.status_code),
                                                         resp.status_code)
                    except Exception as e:
                        return resp.status_code
            if ip != None and mac == None:
                try:
                    mac = self.fetch()['ipv4addrs'][0]['mac']
                except Exception as e:
                    pass
                if re.match('(?:[0-9a-fA-F]:?){12}',mac):
                    payload = '{{"ipv4addrs":[{{"ipv4addr":"{0}","mac":"{1}"}}]}}'.format(ip, mac)
                else:
                    payload = '{{"ipv4addrs":[{{"ipv4addr":"{0}"}}]}}'.format(ip)
            if mac != None and ip == None:
                payload = '{{"ipv4addrs":[{{"ipv4addr":"{0}","mac":"{1}"}}]}}'\
                        .format(self.fetch()['ipv4addrs'][0]['ipv4addr'], mac)
            if mac != None and ip != None:
                payload = '{{"ipv4addrs":[{{"ipv4addr":"{0}","mac":"{1}"}}]}}'.format(ip, mac)
            resp = self.infoblox_.put(self._ref, payload)
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__('Error updating host record {0} - Status: {1}'\
                                                     .format(self.hostname, resp.status_code),
                                                     resp.status_code)
                except Exception as e:
                    return resp.status_code
            return 0


        def alias(self):
            """
             alias - alias object

            input   void (void)
            output  handle (handle)     Reference to lease object
            """
            handle = self._alias(self,self.infoblox_)
            return handle


        class _alias(object):


            def __init__(self, host_, infoblox_):
                """
                class constructor - Automatically called on class instantiation

                input   host_ (object)      Host class object
                        infoblox_ (object)  Infoblox class object
                output  void (void)
                """
                self.infoblox_ = infoblox_
                self.host_ = host_


            def fetch(self):
                """
                fetch - Get a list of aliases for a given hostname

                input   void (void)
                output  aliases (list)      list of infoblox aliases
                """
                resp = self.infoblox_.get('record:host?_return_fields%2B=aliases&name={0}'\
                                          .format(self.host_.hostname))
                if resp.status_code != 200:
                    try:
                        return self.infoblox_.__caller__('Could not retrieve aliases for {0}'\
                                                         '- Status {1}'\
                                                         .format(self.host_.hostname,
                                                                 resp.status_code),
                                                         resp.status_code)
                    except Exception as e:
                        return resp.status_code
                try:
                    return json.loads(resp.text)[0]['aliases']
                except Exception as e:
                    return []


            def add(self, new_alias):
                """
                add - Create an alias in a given host record

                input   new_alias (string)  new alias to attach to host record
                output  0 (int)             Success
                """
                aliases = self.fetch()
                str_alias = ''
                for alias in aliases:
                    str_alias += ('"{0}",'.format(alias))
                str_alias += '"{0}"'.format(str(new_alias))
                payload = '{{"aliases":[{0}]}}'.format(str_alias)
                resp = self.infoblox_.put('{0}'.format(self.host_._ref), payload)
                if resp.status_code != 200:
                    try:
                        return self.infoblox_.__caller__(
                            'Could not set aliases for {0} - Status {1}'\
                            .format(self.host_.hostname, resp.status_code), resp.status_code)
                    except Exception as e:
                        return resp.status_code
                return 0


            def delete(self, rm_alias):
                """
                delete - Remove an alias from a given host record

                input   rm_alias (string)   alias to remove from a host record
                output  0 (int)             Success
                """
                aliases = self.fetch()
                str_alias = ''
                for alias in aliases:
                    if rm_alias not in alias:
                        str_alias += ('"{0}",'.format(alias))
                str_alias = str_alias[:-1]
                payload = '{{"aliases":[{0}]}}'.format(str_alias)
                resp = self.infoblox_.put('{0}'.format(self.host_._ref), payload)
                if resp.status_code != 200:
                    try:
                        return self.infoblox_.__caller__(
                            'Could not unset aliases for {0} - Status {1}'\
                            .format(self.host_.hostname, resp.status_code), resp.status_code)
                    except Exception as e:
                        return resp.status_code
                return 0


    class _grid(object):


        def __init__(self, infoblox_):
            """
            class constructor - Automatically called on class instantiation

            input   infoblox_ (object)      Parent class object
            output  void (void)
            """
            self.infoblox_ = infoblox_
            self._ref = self._ref()


        def _ref(self):
            """
            _ref - Get ID of the current gridmaster

            input   void (void)
            output  grid_ref (string)       Hash ID of the current Infoblox gridmaster
                    1 (int)                 Failed ot get grid _ref ID
            """
            resp = self.infoblox_.get('grid')
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not get grid _ref - Status {0}'\
                        .format(resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            return json.loads(resp.text)[0]['_ref']


        def restart(self):
            """
            grid_restart - Restart the Infoblox gridmaster, required to save changes to host records

            input   void (void)
            output  0 (int)                 Success
                    1 (int)                 Failure
            """
            resp = self.infoblox_.post('{0}?_function=restartservices&member_order=SEQUENTIALLY'\
                                       '&sequential_delay=10&service_option=ALL'\
                                       '&restart_option=FORCE_RESTART'\
                                       .format(self._ref), '')
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not restart Infoblox gridmaster - Status {0}'\
                        .format(resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            return 0


    class _subnet(object):


        def __init__(self, infoblox_, subnet):
            """
            class constructor - Automatically called on class instantiation

            input   infoblox_ (object)      Parent class object
                    subnet (string)         Specified subnet
            output  void (void)
            """
            self.infoblox_ = infoblox_
            if subnet == None:
                self.subnet = self.prompt()[0]
            else:
                self.subnet=subnet
            self._ref = self._ref()


        def _ref(self):
            """
            _ref - Get _ref for a specified subnet

            input   void (void)
            output  subnet_ref (string)     _ref ID for a subnet
            """
            resp = self.infoblox_.get('network?network={0}'.format(self.subnet))
            if resp.status_code !=200:
                try:
                    return self.infoblox_.__caller__(
                        'Error getting subnet ID for subnet {0} - Status {1}'\
                        .format(self.subnet, resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            return json.loads(resp.text)[0]['_ref']


        def next_available_ip(self, offset=2):
            """
            next_available_ip - Get the next available IP address in a subnet.
                                The first results is always the gateway.

            input   offset (int)            Optional arg to provide address offset for
                                            networking gear/etc not accounted in IPAM
            output  ip_addr (string)        IP address
                    None (null)             No free IP addresses
            """
            payload = '{{"num":{0}}}'.format(offset)
            resp = self.infoblox_.post(
                        '{0}?_function=next_available_ip'\
                        .format(self._ref), payload)
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Error retrieving next available address - Status {0}'\
                        .format(resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            try:
                return json.loads(resp.text)['ips'][offset-1]
            except Exception as e:
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
            subnet_format_check - Checks to make sure the subnet is properly formatted
                                  in CIDR notation

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

    class _mx(object):


        def __init__(self, infoblox_, mail_exchanger):
            """
            class constructor - Automatically called on class instantiation

            input   infoblox_ (object)      Parent class object
                    address (string)        IP address of lease
            output  void (void)
            """
            self.infoblox_ = infoblox_
            self.mail_exchanger = mail_exchanger

        def fetch(self):
            """
            fetch - Retrieve all information from a specified host record

            input   void (void)
            output  resp (parsed json)  Parsed JSON response
            """
            resp = self.infoblox_.get('record:mx?mail_exchanger~={0}'.format(self.mail_exchanger))
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__('Could not retrieve host _ref for {0}'\
                                                     ' - Status {1}'\
                                                     .format(self.hostname, resp.status_code),
                                                     resp.status_code)
                except Exception as e:
                    return resp.status_code
            try:
                return json.loads(resp.text)[0]

            except(ValueError,IndexError) as e:
                return None

    class _lease(object):


        def __init__(self, infoblox_, address):
            """
            class constructor - Automatically called on class instantiation

            input   infoblox_ (object)      Parent class object
                    address (string)        IP address of lease
            output  void (void)
            """
            self.infoblox_ = infoblox_
            self.address = address


        def fetch(self, return_fields):
            """
            fetch - Fetch specified fields of a lease object

            input   return_fields (string)  Fields desired for a query against a lease
            output  resp (parsed json)      Parsed JSON response
            """
            resp = self.infoblox_.get(
                'lease?address<={0}&_return_fields={1}'.format(self.address,return_fields))
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Error fetching data from least {0} - Status {1}'\
                        .format(self.address, resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            return json.loads(resp.text)


    class _a(object):

        def __init__(self, infoblox_, name):
            """
            class constructor - Automatically called on class instantiation

            input   infoblox_ (object)      Parent class object
                    name (string)           DNS name of A Record
            output  void (void)
            """
            self.infoblox_ = infoblox_
            self.name = name
            self._ref = self._ref()


        def _ref(self):
            """
            _ref - Get _ref for a specified host record

            input   void (void)
            output  host _ref               _ref ID for A record
            """
            try:
                return self.fetch()['_ref']
            except Exception as e:
                return None


        def fetch(self):
            """
            fetch - Retrieve all information from a specified A record

            input   void (void)
            output  resp (parsed json)      Parsed JSON response
            """
            resp = self.infoblox_.get('record:a?name~={0}'.format(self.name))
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not retrieve A record _ref for {0} - Status {1}'\
                        .format(self.name, resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            try:
                return json.loads(resp.text)[0]

            except (ValueError,IndexError) as e:
                return None


        def add(self, ip, ttl=None):
            """
            add - Create A record

            input   ip (string)             IP Address of A Record
                    ttl (int)               Optional: Time to live
            output  0 (int)                 Success
            """
            if ttl != None:
                payload = '{{"name":"{0}","ipv4addr":"{1}","ttl":{2}}}'.format(self.name, ip,ttl)
            else:
                payload = '{{"name":"{0}","ipv4addr":"{1}"}}'.format(self.name, ip)
            resp = self.infoblox_.post('record:a',payload)
            if resp.status_code != 201:
                try:
                    return self.infoblox_.__caller__(
                        'Could not create A record for {0} - Status {1}'\
                        .format(self.name,resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            return 0


        def delete(self):
            """
            delete - Delete A record

            input   void (void)
            output  0 (int)                 Success
            """
            resp = self.infoblox_.delete(self._ref)
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not delete A record for {0} - Status {1}'\
                        .format(self.name,resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            return 0


        def update(self, ip=None, ttl=None):
            """
            update - Update a CNAME record with new attributes

            input   ip (string)             Optional: IP Address of A Record
                    ttl (int)               Optional: Time to live
            output  0 (int)                 Success
            """
            if ip != None:
                payload = '{{"ipv4addr":"{0}"}}'.format(ip)
            if ttl != None:
                payload = '{{"ttl":{0}}}'.format(ttl)
            resp = self.infoblox_.put(self._ref,payload)
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not update A record for {0} - Status {1}'\
                        .format(self.name,resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            return 0


    class _cname(object):


        def __init__(self, infoblox_, name):
            """
            class constructor - Automatically called on class instantiation

            input   infoblox_ (object)      Parent class object
                    name (string)           DNS name of CNAME
            output  void (void)
            """
            self.infoblox_ = infoblox_
            self.name = name
            self._ref = self._ref()


        def _ref(self):
            """
            _ref - Get _ref for a specified CNAME record

            input   void (void)
            output  host _ref               _ref ID for CNAME record
            """
            try:
                return self.fetch()['_ref']
            except Exception as e:
                return None


        def fetch(self):
            """
            fetch - Retrieve all information from a specified CNAME record

            input   void (void)
            output  resp (parsed json)      Parsed JSON response
            """
            resp = self.infoblox_.get('record:cname?name~={0}'.format(self.name))
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not retrieve CNAME _ref for {0} - Status {1}'\
                        .format(self.name, resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            try:
                return json.loads(resp.text)[0]

            except (ValueError,IndexError) as e:
                return None


        def add(self, canonical, ttl=None):
            """
            add - Create CNAME record

            input   canonical (string)      Canonical address for CNAME record
                    ttl (int)               Optional: Time to live
            output  0 (int)                 Success
            """
            if ttl != None:
                payload = '{{"name":"{0}","canonical":"{1}","ttl":{2}}}'\
                          .format(self.name, canonical,ttl)
            else:
                payload = '{{"name":"{0}","canonical":"{1}"}}'.format(self.name, canonical)
            resp = self.infoblox_.post('record:cname',payload)
            if resp.status_code != 201:
                try:
                    return self.infoblox_.__caller__(
                        'Could not create CNAME record for {0} - Status {1}'\
                        .format(self.name,resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            return 0


        def delete(self):
            """
            delete - Delete CNAME record

            input   void (void)
            output  0 (int)                 Success
            """
            resp = self.infoblox_.delete(self._ref)
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not delete CNAME record for {0} - Status {1}'\
                        .format(self.name,resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            return 0


        def update(self, canonical=None, ttl=None):
            """ update - Update a CNAME record with new attributes

            input   canonical (string)      Optional: Canonical address for CNAME record
                    ttl (int)               Optional: Time to live
            output  0 (int)                 Success
            """
            if canonical != None:
                payload = '{{"canonical":"{0}"}}'.format(canonical)
            if ttl != None:
                payload = '{{"ttl":{0}}}'.format(ttl)
            resp = self.infoblox_.put(self._ref,payload)
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not update CNAME record for {0} - Status {1}'\
                        .format(self.name,resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            return 0

    class _srv(object):


        def __init__(self, infoblox_, name, port):
            """
            class constructor - Automatically called on class instantiation

            input   infoblox_ (object)      Parent class object
                    name (string)           DNS name of CNAME
            output  void (void)
            """
            self.infoblox_ = infoblox_
            self.name = name
            self.port = port
            self._ref = self._ref()


        def _ref(self):
            """
            _ref - Get _ref for a specified CNAME record

            input   void (void)
            output  host _ref               _ref ID for CNAME record
            """
            try:
                return self.fetch()['_ref']
            except Exception as e:
                return None

        def fetch(self):
            """
            fetch - Retrieve all information from a specified SRV record

            input   void (void)
            output  resp (parsed json)      Parsed JSON response
            """
            resp = self.infoblox_.get('record:srv?name~={0}'.format(self.name))
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not retrieve SRV _ref for {0} - Status {1}'\
                        .format(self.name, resp.status_code), resp.status_code)
                except Exception as e:
                    return resp.status_code
            try:
                return json.loads(resp.text)[0]

            except (ValueError,IndexError) as e:
                return None

        def add(self, target, weight=0, priority=0):
            """
            add - add target to srv record

            input   target (string)     DNS target for srv record
            output  0 (int)             Target successfully added
            """
            payload = '{{"target": "{0}", "weight": {1}, "name": "{2}", "priority": {3}'\
                      ',"port": {4}}}'\
                      .format(target, weight, self.name, priority, self.port)
            resp = self.infoblox_.post('record:srv',payload)                                       
            if resp.status_code != 201:                                                             
                try:                                                                                
                    return self.infoblox_.__caller__('Error creating srv record {0} for {1}'\
                                                     ' - Status: {2}'\
                                                     .format(ip, self.name, resp.status_code),  
                                                     resp.status_code)                              
                except Exception as e:                                                              
                    return resp.status_code                                                         
            return 0  

        def delete(self):                                                                           
            """                                                                                     
            del - Delete a SRV record within Infoblox                                              
                                                                                                    
            input   void (void)                                                                     
            output  0 (int)             Successful deletion                                        
                    errno (int)         Error code of API call                                      
            """                                                                                     
            resp = self.infoblox_.delete(self._ref)                                                 
            if resp.status_code != 201:                                                             
                try:                                                                                
                    return self.infoblox_.__caller__('Error deleting SRV record {0} for {1}'\
                                                     ' - Status: {2}'\
                                                     .format(self.name, resp.status_code),      
                                                     resp.status_code)                              
                except Exception as e:                                                              
                    return resp.status_code                                                         
            return 0

        def update(self, target=None, weight=None, priority=None):
            """
            add - add target to srv record

            input   target (string)     DNS target for srv record
            output  0 (int)             Target successfully added
            """
            rec = self.fetch()
            if target is None:
                target = rec['target']
            if weight is None:
                weight = rec['weight']
            if priority is None:
                priority = rec['priority']
            payload = '{{"target": "{0}", "weight": {1}, "name": "{2}", "priority": {3}'\
                      ',"port": {4}}}'\
                      .format(target, weight, self.name, priority, self.port)
            print payload
            resp = self.infoblox_.put(self._ref, payload)                                       
            if resp.status_code != 201:                                                             
                try:                                                                                
                    return self.infoblox_.__caller__('Error creating srv record {0} for {1}'\
                                                     ' - Status: {2}'\
                                                     .format(ip, self.name, resp.status_code),  
                                                     resp.status_code)                              
                except Exception as e:                                                              
                    return resp.status_code                                                         
            return 0 
