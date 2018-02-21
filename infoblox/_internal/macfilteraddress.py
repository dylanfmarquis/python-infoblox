import json

class _macfilteraddress(object):
    """
    Class for interfacing with WAPI for macaddressfilter
    No refs needed for this class
    """

    def __init__(self, infoblox_):
        """
        class constructor - Automatically called on class instantiation

        input   infoblox_ (object)          Parent class object
        output  void (void)
        """
        self.infoblox_ = infoblox_

    def add(self, filter_name, mac, kwargs={}):
        """
        add - Adds a MAC address to an already existing macfilter

        input   filter_name (string)        Name of macfilter (required)
                mac (string)                MAC to add to macfilter (required)
                kwargs (dict)                 Python dict of optional fields
                                            Can be of the following:
                                            authentication_time (Timestamp)
                                            comment (string)
                                            expiration_time (Timestamp)
                                            extattrs (Extattr)
                                            fingerprint (string)
                                            guest_custom_field1 (string)
                                            guest_custom_field2 (string)
                                            guest_custom_field3 (string)
                                            guest_custom_field4 (string)
                                            guest_email (string)
                                            guest_first_name (string)
                                            guest_last_name (string)
                                            guest_middle_name (string)
                                            guest_phone (string)
                                            is_registered_user (Bool)
                                            never_expires (Bool)
                                            reserved_for_Infoblox (string)
                                            username (string)

        output void (void)
        """

        # Create dict for payload
        d = {key: kwargs[key] for key in kwargs if kwargs[key]}
        d["mac"] = mac
        d["filter"] = filter_name

        # Create payload dict
        payload = json.dumps(d)

        # Try to post it
        resp = self.infoblox_.post('macfilteraddress', payload)

        if resp.status_code != 201:
            try:
                return self.infoblox_.__caller__(
                    'Could not create macfilteraddress for {0} - Status {1} - Reason {2}'
                    .format(d['mac'], resp.status_code, resp.reason), resp.status_code)
            except Exception:
                return resp.status_code

        return 0
