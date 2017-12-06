import json


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
        fetch - Retrieve all information from a specified SRV record

        input   void (void)
        output  resp (parsed json)      Parsed JSON response
        """
        resp = self.infoblox_.get('record:srv?name~={0}'.format(self.name))
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not retrieve SRV _ref for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        try:
            return json.loads(resp.text)[0]

        except (ValueError, IndexError):
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
        resp = self.infoblox_.post('record:srv', payload)
        if resp.status_code != 201:
            try:
                return self.infoblox_.__caller__('Error creating srv record '
                                                 '{0} - Status: {1}'
                                                 .format(self.name,
                                                         resp.status_code),
                                                 resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def delete(self):
        """
        del - Delete a SRV record within Infoblox

        input   void (void)
        output  0 (int)             Successful deletion
                errno (int)         Error code of API call
        """
        resp = self.infoblox_.delete(self._ref_)
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__('Error deleting SRV record '
                                                 '{0} for {1} - Status: {2}'
                                                 .format(self.name,
                                                         resp.status_code),
                                                 resp.status_code)
            except Exception:
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
        resp = self.infoblox_.put(self._ref_, payload)
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__('Error updating srv record '
                                                 '{0} - Status: {1}'
                                                 .format(self.name,
                                                         resp.status_code),
                                                 resp.status_code)
            except Exception:
                return resp.status_code
        return 0
