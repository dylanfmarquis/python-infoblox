import json


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
        fetch - Retrieve all information from a specified host record

        input   void (void)
        output  resp (parsed json)  Parsed JSON response
        """
        resp = self.infoblox_.get(
            'record:mx?mail_exchanger~={0}'.format(self.mail_exchanger))
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
