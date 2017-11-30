import json


class _grid(object):

    def __init__(self, infoblox_):
        """
        class constructor - Automatically called on class instantiation

        input   infoblox_ (object)      Parent class object
        output  void (void)
        """
        self.infoblox_ = infoblox_
        self._ref_ = self._ref()

    def _ref(self):
        """
        _ref - Get ID of the current gridmaster

        input   void (void)
        output  grid_ref (string)       Hash ID of the current Infoblox
                                        gridmaster
                1 (int)                 Failed ot get grid _ref ID
        """
        resp = self.infoblox_.get('grid')
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not get grid _ref - Status {0}'
                    .format(resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return json.loads(resp.text)[0]['_ref']

    def restart(self):
        """
        grid_restart - Restart the Infoblox gridmaster, required to save
                       changes to host records

        input   void (void)
        output  0 (int)                 Success
                1 (int)                 Failure
        """
        resp = self.infoblox_.post('{0}?_function=restartservices&member_order=SEQUENTIALLY'
                                   '&sequential_delay=10&service_option=ALL'
                                   '&restart_option=RESTART_IF_NEEDED'
                                   .format(self._ref_), '')
        if resp.status_code != 200:
            try:
                return self.infoblox_.__caller__(
                    'Could not restart Infoblox gridmaster - Status {0}'
                    .format(resp.status_code), resp.status_code)
            except Exception:
                return resp.status_code
        return 0
