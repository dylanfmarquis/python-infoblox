import re
import json


class _host(object):

    def __init__(self, infoblox_, hostname):
        """
        class constructor - Automatically called on class instantiation

        input   hostname (string)   Hostname to specify Infoblox host record
                infoblox_ (object)  Parent class object
        output  void (void)
        """
        self.infoblox_ = infoblox_
        if hostname is not None:
            self.hostname = hostname
            self._ref_ = self._ref()

    def _ref(self):
        """
        _ref - Get _ref for a specified host record

        input   void (void)
        output  host _ref           _ref ID for a host record
        """
        try:
            return self.fetch()['_ref']
        except Exception:
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
                return self.infoblox_.__caller__('Could not retrieve host _ref'
                                                 ' for {0} - Status {1}'
                                                 .format(self.hostname,
                                                         resp.status_code),
                                                 resp.status_code)
            except Exception:
                return resp.status_code
        try:
            return json.loads(resp.text)[0]

        except(ValueError, IndexError):
            return None

    def add(self, ip, mac=None):
        """
        add - Create a host record within Infoblox

        input   ip (string)         IP address to create host record
                mac (string)        MAC address to attach to host record
        output  0 (int)             Successful creation
                errno (int)         Error code of API call
        """
        if mac is not None:
            payload = '{{"name":"{0}", "ipv4addrs":[ {{"ipv4addr":"{1}","mac":"{2}"}}]}}'\
                      .format(self.hostname, ip, mac)
        else:
            payload = '{{"name":"{0}", "ipv4addrs":[ {{"ipv4addr":"{1}"}}]}}'\
                      .format(self.hostname, ip, mac)
        resp = self.infoblox_.post('record:host', payload)
        if resp.status_code != 201:
            try:
                return self.infoblox_.__caller__('Error creating host record '
                                                 '{0} for {1}'
                                                 ' - Status: {2}'
                                                 .format(ip, self.hostname,
                                                         resp.status_code),
                                                 resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def delete(self):
        """
        del - Delete a host record within Infoblox

        input   void (void)
        output  0 (int)             Successful creation
                errno (int)         Error code of API call
        """
        resp = self.infoblox_.delete(self._ref_)
        if resp.status_code != 201:
            try:
                return self.infoblox_.__caller__('Error creating host record '
                                                 '{0} for {1} - Status: {2}'
                                                 .format(self.hostname,
                                                         resp.status_code),
                                                 resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def update(self, ip=None, mac=None, ttl=None):
        """
        update - Update a Host record with new attributes

        input   ip (string)         Optional: IP address of a host record
                ttl (int)           Optional: MAC address of a host record
        output  0 (int)             Success
        """
        if ttl is not None:
            payload = '{{"ttl": {0}}}'.format(ttl)
            resp = self.infoblox_.put(self._ref_, payload)
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__('Error updating host '
                                                     'record {0}'
                                                     '- Status: {1}'
                                                     .format(self.hostname,
                                                             resp.status_code),
                                                     resp.status_code)
                except Exception:
                    return resp.status_code
        if ip is not None and mac is None:
            try:
                mac = self.fetch()['ipv4addrs'][0]['mac']
            except Exception:
                pass
            if re.match('(?:[0-9a-fA-F]:?){12}', mac):
                payload = '{{"ipv4addrs":[{{"ipv4addr":"{0}","mac":"{1}"}}]}}'.format(ip, mac)
            else:
                payload = '{{"ipv4addrs":[{{"ipv4addr":"{0}"}}]}}'.format(ip)
        if mac is not None and ip is None:
            payload = '{{"ipv4addrs":[{{"ipv4addr":"{0}","mac":"{1}"}}]}}'\
                    .format(self.fetch()['ipv4addrs'][0]['ipv4addr'], mac)
        if mac is not None and ip is not None:
            payload = '{{"ipv4addrs":[{{"ipv4addr":"{0}","mac":"{1}"}}]}}'.format(ip, mac)
        resp = self.infoblox_.put(self._ref_, payload)
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__('Error updating host record '
                                                 '{0} - Status: {1}'
                                                 .format(self.hostname,
                                                         resp.status_code),
                                                 resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def alias(self):
        """
         alias - alias object

        input   void (void)
        output  handle (handle)     Reference to lease object
        """
        handle = self._alias(self, self.infoblox_)
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
            resp = self.infoblox_.get(
                'record:host?_return_fields%2B=aliases&name={0}'.format(
                    self.host_.hostname))
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not retrieve aliases for {0} - Status {1}'
                        .format(self.host_.hostname, resp.status_code),
                        resp.status_code)
                except Exception:
                    return resp.status_code
            try:
                return json.loads(resp.text)[0]['aliases']
            except Exception:
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
            resp = self.infoblox_.put('{0}'.format(self.host_._ref_), payload)
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not set aliases for {0} - Status {1}'
                        .format(self.host_.hostname, resp.status_code),
                        resp.status_code)
                except Exception:
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
            resp = self.infoblox_.put('{0}'.format(self.host_._ref_), payload)
            if resp.status_code != 200:
                try:
                    return self.infoblox_.__caller__(
                        'Could not unset aliases for {0} - Status {1}'
                        .format(self.host_.hostname, resp.status_code),
                        resp.status_code)
                except Exception:
                    return resp.status_code
            return 0
