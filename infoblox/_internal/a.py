import json


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
        self._ref_ = self._ref()

    def _ref(self):
        """
        _ref - Get _ref for a specified host record

        input   void (void)
        output  host _ref               _ref ID for A record
        """
        try:
            return self.fetch()['_ref']
        except Exception:
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
                    'Could not retrieve A record _ref for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        try:
            return json.loads(resp.text)[0]

        except (ValueError, IndexError):
            return None

    def add(self, ip, ttl=None):
        """
        add - Create A record

        input   ip (string)             IP Address of A Record
                ttl (int)               Optional: Time to live
        output  0 (int)                 Success
        """
        if ttl is not None:
            payload = '{{"name":"{0}","ipv4addr":"{1}","ttl":{2}}}'.format(
                self.name, ip, ttl)
        else:
            payload = '{{"name":"{0}","ipv4addr":"{1}"}}'.format(self.name, ip)
        resp = self.infoblox_.post('record:a', payload)
        if resp.status_code != 201:
            try:
                return self.infoblox_.__caller__(
                    'Could not create A record for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def delete(self):
        """
        delete - Delete A record

        input   void (void)
        output  0 (int)                 Success
        """
        resp = self.infoblox_.delete(self._ref_)
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not delete A record for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def update(self, ip=None, ttl=None):
        """
        update - Update a CNAME record with new attributes

        input   ip (string)             Optional: IP Address of A Record
                ttl (int)               Optional: Time to live
        output  0 (int)                 Success
        """
        if ip is not None:
            payload = '{{"ipv4addr":"{0}"}}'.format(ip)
        if ttl is not None:
            payload = '{{"ttl":{0}}}'.format(ttl)
        resp = self.infoblox_.put(self._ref_, payload)
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not update A record for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0
