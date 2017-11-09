import json


class _rpz_cname(object):

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
        except Exception:
            return None

    def fetch(self):
        """
        fetch - Retrieve all information from a specified RPZ CNAME record

        input   void (void)
        output  resp (parsed json)      Parsed JSON response
        """
        resp = self.infoblox_.get('record:rpz:cname?name~={0}'.format(self.name))
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not retrieve CNAME _ref for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp
        try:
            return json.loads(resp.text)[0]

        except (ValueError, IndexError):
            return None

    def add(self, canonical, rp_zone, comment="", ttl=None, view=None):
        """
        add - Create RPZ CNAME record

        input   canonical (string)      Canonical address for CNAME record
                rp_zone (string)        Response policy zone name
                comment (string)        Optional: An optional comment
                ttl (int)               Optional: Time to live
                view (string)           Optional: The view where the record is
        output  0 (int)                 Success
        """
        # pass
        # TODO: Build payload
        # TODO: Make _POST request
        # TODO: Check status code and return/error out
        payload = '{"name":"%s", "canonical":"%s", "rp_zone":"%s"' % (self.name+'.'+rp_zone, canonical, rp_zone)
        if comment is not None:
            payload += ', "comment":"%s"' % (comment)
        if ttl is not None:
            payload += ', "ttl":%s' % (ttl)
        if view is not None:
            payload += ', "view":"%s"' % (view)

        payload += '}'

        resp = self.infoblox_.post('record:rpz:cname', payload)

        if resp.status_code != 201:
            print(resp.json())
            print(resp.status_code)
            try:
                return self.infoblox_.__caller__(
                    'Could not create CNAME record for {0} - Status {1}'\
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def delete(self):
        """
        delete - Delete RPZ CNAME record

        input   void (void)
        output  0 (int)                 Success
        """
        resp = self.infoblox_.delete(self._ref)
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not delete RPZ CNAME record for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def update(self, name, rp_zone, comment="", TTL=None, view=None):
        """
        add - Create RPZ CNAME record

        input   canonical (string)      Canonical address for CNAME record
                rp_zone (string)        Response policy zone name
                comment (string)        Optional: An optional comment
                ttl (int)               Optional: Time to live
                view (string)           Optional: The view where the record is
        output  0 (int)                 Success
        """
        pass
        # TODO: Build payload
        # TODO: Make _PUT request
        # TODO: Check status code and return/error out
