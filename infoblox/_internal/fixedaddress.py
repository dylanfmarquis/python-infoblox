import json

class _fixedaddress(object):
    """
    Class for interfacing with WAPI for fixedaddress
    No refs needed on init
    """

    def __init__(self, infoblox_):
        """
        Class constructor - Automatically called on class instantiation

        input   infoblox_ (object)          Parent class object
        output  void (void)
        """
        self.infoblox_ = infoblox_

    def add(self, ip, kwargs):
        """
        add - Adds a fixed address

        input -     ip      (string)        IP address to fix
                    kwargs  (dict)          Python dict of data to be put into
                                            fixed address. Requires one of the
                                            following:
                                            agent_circuit_id
                                            agent_remote_id
                                            dhcp_client_identifier
                                            mac *typically used
        output      void (void)
        """

        # Generate data dict
        d = {key: kwargs[key] for key in kwargs if kwargs[key]}
        d["ipv4addr"] = ip

        # Create payload
        payload = json.dumps(d)

        # Try to post
        resp = self.infoblox_.post('fixedaddress', payload)

        if resp.status_code != 201:
            try:
                return self.infoblox_.__caller__(
                    'Could not create fixed fixedaddress for {0} - Status {1} - Reason {2}'
                    .format(d['ipv4addr'], resp.status_code, resp.reason), resp.status_code)
            except Exception:
                return resp.status_code

        return 0
