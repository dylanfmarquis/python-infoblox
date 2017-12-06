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
        self._ref_ = self._ref()
        self.zone = None

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
        resp = self.infoblox_.get('record:rpz:cname?name~={0}&_return_fields=canonical,comment,disable,name,rp_zone,ttl,view,zone'.format(self.name))
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
        kwargs = {
                  "name": self.name + '.' + rp_zone,
                  "canonical": canonical,
                  "rp_zone": rp_zone,
                  "comment": comment,
                  "ttl": ttl,
                  "view": view
                 }
        d = {key: kwargs[key] for key in kwargs if kwargs[key]}
        payload = json.dumps(d)

        resp = self.infoblox_.post('record:rpz:cname', payload)

        if resp.status_code != 201:
            try:
                return self.infoblox_.__caller__(
                    'Could not create CNAME record for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code

        # If we added successfully, set the zone
        self.zone = rp_zone
        self._ref_ = self._ref()

        return 0

    def delete(self):
        """
        delete - Delete RPZ CNAME record

        input   void (void)
        output  0 (int)                 Success
        """
        resp = self.infoblox_.delete(self._ref_)
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not delete RPZ CNAME record for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0

    def update(self, name=None, canonical=None,
               comment="", ttl=None, view=None):
        """
        add - Create RPZ CNAME record

        input   canonical (string)      Optional: Canonical address for CNAME
                                                  record
                rp_zone (string)        Optional: Response policy zone name
                comment (string)        Optional: An optional comment
                ttl (int)               Optional: Time to live
                view (string)           Optional: The view where the record is
        output  0 (int)                 Success
        """

        kwargs = {
                  "name": (name + '.' + self.zone if name is not None and
                                                    self.zone is not None
                                                  else None),
                  "canonical": canonical,
                  "comment": comment,
                  "ttl": ttl,
                  "view": view
                 }
        d = {key: kwargs[key] for key in kwargs if kwargs[key]}
        payload = json.dumps(d)

        resp = self.infoblox_.put(self._ref_, payload)

        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not create CNAME record for {0} - Status {1}'
                    .format(self.name, resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0
