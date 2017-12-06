"""
python-infoblox - Infoblox WAPI module
Copyright (C) 2016 Dylan F. Marquis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
import base64
import getpass
import warnings
# For input purposes
from builtins import input, bytes

try:
    from infoblox import _internal
except ImportError:
    import _internal

__version__ = '0.4'
__author__  = "Dylan F. Marquis"
__author__  = "Drew Monroe"

# Infoblox Network Management
class infoblox(object):

    def __caller__(self, error, errno):
        """
        __caller__ - Wrapper for error callback function

        input   error (string)      Error description to provide to callback
                errno (int)         Status code of API call
        output  callback (funct)    Calls callback function and passes
                                    error string
                errno (int)         Status code of API call (if no callback
                                    is specified)
        """
        if self.callback is not None:
            return self.callback(error)
        return int(errno)

    def __init__(self, callback=None, auth={}, vers='v2.6.1'):
        """
        class constructor - Automatically called on class instantiation

        input   callback (funct)    An optional callback can be passed at
                                    instantiation for error and logging
                                    purposes
        output  void (void)
        """
        self.callback = callback
        self.vers = vers
        l_ret = self.auth(auth)
        self.url = l_ret[0]
        self.creds = l_ret[1]

    def __del__(self):
        """
        class destructor - Invalidates the cookie on Infoblox side to
                           effectively logout the user
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
                                1 - Base64 encoded Infoblox username
                                    and password
        """
        while(1):
            if auth.get('url'):
                url = auth['url']
            else:
                url = input('Infoblox URL: ')
            if auth.get('user'):
                user = auth['user']
            else:
                user = input('Infoblox Username: ')
            if auth.get('passwd'):
                passwd = auth['passwd']
            else:
                passwd = getpass.getpass()
            creds = (base64.b64encode(
                        bytes('{0}:{1}'.format(user, passwd), "utf-8"))
                     .decode("utf-8"))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                resp = requests.get('https://{0}/wapi/{1}/record:host?name~={0}'
                                    .format(url, self.vers),
                                    headers={'Authorization': 'Basic {0}'
                                                              .format(creds),
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

        input   query (string)  Directory location of API call - path after
                                /api/ in URL
        output  resp (struct)   API HTTP response, including status code
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return requests.get('https://{0}/wapi/{1}/{2}'
                                .format(self.url, self.vers, query),
                                headers={'Authorization': 'Basic {0}'
                                                          .format(self.creds),
                                         'Accept': 'application/json'},
                                verify=False)

    def post(self, api_function, payload):
        """
        post - Send POST request to Infoblox WAPI

        input   api_function (string)   Function to call in WAPI
                payload (string)        Payload for the POST request
        output  resp (struct)           WAPI HTTP response, including
                                        status code
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return requests.post('https://{0}/wapi/{1}/{2}'
                                 .format(self.url, self.vers, api_function),
                                 data=payload,
                                 headers={
                                          'Authorization': 'Basic {0}'
                                                           .format(self.creds)
                                         },
                                 verify=False)

    def put(self, api_function, payload):
        """
        put - Send PUT request to Infoblox WAPI

        input   api_function (string)   Function to call in WAPI
                payload (string)        Payload for the PUT request
        output  resp (struct)           WAPI HTTP response, including
                                        status code
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return requests.put('https://{0}/wapi/{1}/{2}'
                                .format(self.url, self.vers, api_function),
                                data=payload,
                                headers={'Authorization': 'Basic {0}'
                                                          .format(self.creds)},
                                verify=False)

    def delete(self, api_function):
        """
        delete - Send DELETE request to Infoblox WAPI

        input   api_function (string)   Function to call in WAPI
        output  resp (struct)           WAPI HTTP response, including
                                        status code
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return requests.delete('https://{0}/wapi/{1}/{2}'
                                   .format(self.url, self.vers, api_function),
                                   headers={
                                            'Authorization': 'Basic {0}'
                                                             .format(self.creds)
                                           },
                                   verify=False)

    def host(self, hostname=None):
        """
        host - host object

        input   hostname (string)   DNS name for host record
        output  handle (handle)     Reference to host object
        """
        handle = _internal._host(self, hostname)
        return handle

    def grid(self):
        """
        grid - grid object

        input   void (void)
        output  handle (handle)     Reference to grid object
        """
        handle = _internal._grid(self)
        return handle

    def subnet(self, subnet=None):
        """
        subnet - subnet object

        input   subnet (string)     Specified subnet
        output  handle (handle)     Reference to subnet object
        """
        handle = _internal._subnet(self, subnet)
        return handle

    def lease(self, address):
        """
        lease - lease object

        input   address (string)    IP address of lease
        output  handle (handle)     Reference to lease object
        """
        handle = _internal._lease(self, address)
        return handle

    def a(self, name):
        """
        a - A record object

        input   name (string)       DNS name of an A record
        output  handle (handle)     Reference to A record object
        """
        handle = _internal._a(self, name)
        return handle

    def cname(self, name):
        """
        cname - CNAME record object

        input   name (string)       Domain name of CNAME
        output  handle (handle)     Reference to CNAME object
        """
        handle = _internal._cname(self, name)
        return handle

    def mx(self, name):
        """
        mx - MX record (Mail Exchanger) object

        input   name (string)       Domain name of MX record
        output  handle (handle)     Reference to record:mx object
        """
        handle = _internal._mx(self, name)
        return handle

    def srv(self, name, port):
        """
        srv - SRV record object

        input   name (string)       Domain name of SRV
                port (int)          Port number of service
        output  handle (handle)     Reference to SRV record object
        """
        handle = _internal._srv(self, name, port)
        return handle

    def rpz_cname(self, name):
        """
        rpz_cname - A record:rpz:cname object

        input   name (string)       Domain name of the record
        output  handle (handle)     Reference to record:rpz:cname object
        """
        return _internal._rpz_cname(self, name)
