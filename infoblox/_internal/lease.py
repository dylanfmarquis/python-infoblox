import json


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
        self._ref_ = self._ref()

    def _ref(self):
        """
        _ref - Get _ref for a specified CNAME record

        input   void (void)
        output  host _ref               _ref ID for CNAME record
        """
        try:
            return self.fetch('')['_ref']
        except Exception:
            return None

    def fetch(self, return_fields):
        """
        fetch - Fetch specified fields of a lease object

        input   return_fields (string)  Fields desired for a query against
                                        a lease
        output  resp (parsed json)      Parsed JSON response
        """
        resp = self.infoblox_.get(
            'lease?address~={0}&_return_fields={1}'.format(self.address,
                                                           return_fields))
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Error fetching data from least {0} - Status {1}'
                    .format(self.address, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return json.loads(resp.text)
