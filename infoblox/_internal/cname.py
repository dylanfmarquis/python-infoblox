import json


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
        self._ref_ = self._ref()

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
        fetch - Retrieve all information from a specified CNAME record

        input   void (void)
        output  resp (parsed json)      Parsed JSON response
        """
        resp = self.infoblox_.get('record:cname?name~={0}'.format(self.name))
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not retrieve CNAME _ref for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        try:
            return json.loads(resp.text)[0]

        except (ValueError, IndexError):
            return None

    def add(self, canonical, ttl=None):
        """
        add - Create CNAME record

        input   canonical (string)      Canonical address for CNAME record
                ttl (int)               Optional: Time to live
        output  0 (int)                 Success
        """
        if ttl is not None:
            payload = '{{"name":"{0}","canonical":"{1}","ttl":{2}}}'\
                      .format(self.name, canonical, ttl)
        else:
            payload = '{{"name":"{0}","canonical":"{1}"}}'.format(self.name,
                                                                  canonical)

        resp = self.infoblox_.post('record:cname', payload)
        if resp.status_code != 201:
            try:
                return self.infoblox_.__caller__(
                    'Could not create CNAME record for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def delete(self):
        """
        delete - Delete CNAME record

        input   void (void)
        output  0 (int)                 Success
        """
        resp = self.infoblox_.delete(self._ref_)
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not delete CNAME record for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def update(self, canonical=None, ttl=None):
        """ update - Update a CNAME record with new attributes

        input   canonical (string)      Optional: Canonical address for
                                                  CNAME record
                ttl (int)               Optional: Time to live
        output  0 (int)                 Success
        """
        if canonical is not None:
            payload = '{{"canonical":"{0}"}}'.format(canonical)
        if ttl is not None:
            payload = '{{"ttl":{0}}}'.format(ttl)
        resp = self.infoblox_.put(self._ref_, payload)
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not update CNAME record for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0
