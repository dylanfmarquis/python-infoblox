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
import warnings

from _internal import _a, _cname, _grid, _host, _lease, _mx, _srv, _subnet


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
        self.post('logout', '')

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
                                headers={'Authorization': 'Basic {0}'.format(self.creds),
                                         'Accept': 'application/json'},
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
                                 data=payload, headers={'Authorization': 'Basic {0}'\
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
                                data=payload, headers={'Authorization': 'Basic {0}'\
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
                                   headers={'Authorization': 'Basic {0}'.format(self.creds)},
                                   verify=False)

    def host(self, hostname=None):
        """
        host - host object

        input   hostname (string)   DNS name for host record
        output  handle (handle)     Reference to host object
        """
        handle = _host(self, hostname)
        return handle

    def grid(self):
        """
        grid - grid object

        input   void (void)
        output  handle (handle)     Reference to grid object
        """
        handle = _grid(self)
        return handle

    def subnet(self, subnet=None):
        """
        subnet - subnet object

        input   subnet (string)     Specified subnet
        output  handle (handle)     Reference to subnet object
        """
        handle = _subnet(self, subnet)
        return handle

    def lease(self, address):
        """
        lease - lease object

        input   address (string)    IP address of lease
        output  handle (handle)     Reference to lease object
        """
        handle = _lease(self, address)
        return handle

    def a(self, name):
        """
        a - A record object

        input   name (string)       DNS name of an A record
        output  handle (handle)     Reference to A record object
        """
        handle = _a(self, name)
        return handle

    def cname(self, name):
        """
        cname - CNAME record object

        input   name (string)       Domain name of CNAME
        output  handle (handle)     Reference to CNAME object
        """
        handle = _cname(self, name)
        return handle

    def mx(self, name):
        """
        mx - MX record (Mail Exchanger) object

        input   name (string)       Domain name of MX record
        output  handle (handle)     Reference to record:mx object
        """
        handle = _mx(self, name)
        return handle

    def srv(self, name, port):
        """
        srv - SRV record object

        input   name (string)       Domain name of SRV
                port (int)          Port number of service
        output  handle (handle)     Reference to SRV record object
        """
        handle = _srv(self, name, port)
        return handle
