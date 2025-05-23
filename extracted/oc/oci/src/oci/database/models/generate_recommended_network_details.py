# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20160918


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class GenerateRecommendedNetworkDetails(object):
    """
    Generates a recommended VM cluster network configuration for an Exadata Cloud@Customer system. Applies to Exadata Cloud@Customer instances only.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new GenerateRecommendedNetworkDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this GenerateRecommendedNetworkDetails.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this GenerateRecommendedNetworkDetails.
        :type display_name: str

        :param db_servers:
            The value to assign to the db_servers property of this GenerateRecommendedNetworkDetails.
        :type db_servers: list[str]

        :param scan_listener_port_tcp:
            The value to assign to the scan_listener_port_tcp property of this GenerateRecommendedNetworkDetails.
        :type scan_listener_port_tcp: int

        :param scan_listener_port_tcp_ssl:
            The value to assign to the scan_listener_port_tcp_ssl property of this GenerateRecommendedNetworkDetails.
        :type scan_listener_port_tcp_ssl: int

        :param dr_scan_listener_port_tcp:
            The value to assign to the dr_scan_listener_port_tcp property of this GenerateRecommendedNetworkDetails.
        :type dr_scan_listener_port_tcp: int

        :param networks:
            The value to assign to the networks property of this GenerateRecommendedNetworkDetails.
        :type networks: list[oci.database.models.InfoForNetworkGenDetails]

        :param dns:
            The value to assign to the dns property of this GenerateRecommendedNetworkDetails.
        :type dns: list[str]

        :param ntp:
            The value to assign to the ntp property of this GenerateRecommendedNetworkDetails.
        :type ntp: list[str]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this GenerateRecommendedNetworkDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this GenerateRecommendedNetworkDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'display_name': 'str',
            'db_servers': 'list[str]',
            'scan_listener_port_tcp': 'int',
            'scan_listener_port_tcp_ssl': 'int',
            'dr_scan_listener_port_tcp': 'int',
            'networks': 'list[InfoForNetworkGenDetails]',
            'dns': 'list[str]',
            'ntp': 'list[str]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }
        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'db_servers': 'dbServers',
            'scan_listener_port_tcp': 'scanListenerPortTcp',
            'scan_listener_port_tcp_ssl': 'scanListenerPortTcpSsl',
            'dr_scan_listener_port_tcp': 'drScanListenerPortTcp',
            'networks': 'networks',
            'dns': 'dns',
            'ntp': 'ntp',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }
        self._compartment_id = None
        self._display_name = None
        self._db_servers = None
        self._scan_listener_port_tcp = None
        self._scan_listener_port_tcp_ssl = None
        self._dr_scan_listener_port_tcp = None
        self._networks = None
        self._dns = None
        self._ntp = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this GenerateRecommendedNetworkDetails.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this GenerateRecommendedNetworkDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this GenerateRecommendedNetworkDetails.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this GenerateRecommendedNetworkDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this GenerateRecommendedNetworkDetails.
        The user-friendly name for the VM cluster network. The name does not need to be unique.


        :return: The display_name of this GenerateRecommendedNetworkDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this GenerateRecommendedNetworkDetails.
        The user-friendly name for the VM cluster network. The name does not need to be unique.


        :param display_name: The display_name of this GenerateRecommendedNetworkDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def db_servers(self):
        """
        Gets the db_servers of this GenerateRecommendedNetworkDetails.
        The list of Db server Ids to configure network.


        :return: The db_servers of this GenerateRecommendedNetworkDetails.
        :rtype: list[str]
        """
        return self._db_servers

    @db_servers.setter
    def db_servers(self, db_servers):
        """
        Sets the db_servers of this GenerateRecommendedNetworkDetails.
        The list of Db server Ids to configure network.


        :param db_servers: The db_servers of this GenerateRecommendedNetworkDetails.
        :type: list[str]
        """
        self._db_servers = db_servers

    @property
    def scan_listener_port_tcp(self):
        """
        Gets the scan_listener_port_tcp of this GenerateRecommendedNetworkDetails.
        The SCAN TCPIP port. Default is 1521.


        :return: The scan_listener_port_tcp of this GenerateRecommendedNetworkDetails.
        :rtype: int
        """
        return self._scan_listener_port_tcp

    @scan_listener_port_tcp.setter
    def scan_listener_port_tcp(self, scan_listener_port_tcp):
        """
        Sets the scan_listener_port_tcp of this GenerateRecommendedNetworkDetails.
        The SCAN TCPIP port. Default is 1521.


        :param scan_listener_port_tcp: The scan_listener_port_tcp of this GenerateRecommendedNetworkDetails.
        :type: int
        """
        self._scan_listener_port_tcp = scan_listener_port_tcp

    @property
    def scan_listener_port_tcp_ssl(self):
        """
        Gets the scan_listener_port_tcp_ssl of this GenerateRecommendedNetworkDetails.
        The SCAN TCPIP SSL port. Default is 2484.


        :return: The scan_listener_port_tcp_ssl of this GenerateRecommendedNetworkDetails.
        :rtype: int
        """
        return self._scan_listener_port_tcp_ssl

    @scan_listener_port_tcp_ssl.setter
    def scan_listener_port_tcp_ssl(self, scan_listener_port_tcp_ssl):
        """
        Sets the scan_listener_port_tcp_ssl of this GenerateRecommendedNetworkDetails.
        The SCAN TCPIP SSL port. Default is 2484.


        :param scan_listener_port_tcp_ssl: The scan_listener_port_tcp_ssl of this GenerateRecommendedNetworkDetails.
        :type: int
        """
        self._scan_listener_port_tcp_ssl = scan_listener_port_tcp_ssl

    @property
    def dr_scan_listener_port_tcp(self):
        """
        Gets the dr_scan_listener_port_tcp of this GenerateRecommendedNetworkDetails.
        The DR SCAN TCPIP port. Default is 1521.


        :return: The dr_scan_listener_port_tcp of this GenerateRecommendedNetworkDetails.
        :rtype: int
        """
        return self._dr_scan_listener_port_tcp

    @dr_scan_listener_port_tcp.setter
    def dr_scan_listener_port_tcp(self, dr_scan_listener_port_tcp):
        """
        Sets the dr_scan_listener_port_tcp of this GenerateRecommendedNetworkDetails.
        The DR SCAN TCPIP port. Default is 1521.


        :param dr_scan_listener_port_tcp: The dr_scan_listener_port_tcp of this GenerateRecommendedNetworkDetails.
        :type: int
        """
        self._dr_scan_listener_port_tcp = dr_scan_listener_port_tcp

    @property
    def networks(self):
        """
        **[Required]** Gets the networks of this GenerateRecommendedNetworkDetails.
        List of parameters for generation of the client and backup networks.


        :return: The networks of this GenerateRecommendedNetworkDetails.
        :rtype: list[oci.database.models.InfoForNetworkGenDetails]
        """
        return self._networks

    @networks.setter
    def networks(self, networks):
        """
        Sets the networks of this GenerateRecommendedNetworkDetails.
        List of parameters for generation of the client and backup networks.


        :param networks: The networks of this GenerateRecommendedNetworkDetails.
        :type: list[oci.database.models.InfoForNetworkGenDetails]
        """
        self._networks = networks

    @property
    def dns(self):
        """
        Gets the dns of this GenerateRecommendedNetworkDetails.
        The list of DNS server IP addresses. Maximum of 3 allowed.


        :return: The dns of this GenerateRecommendedNetworkDetails.
        :rtype: list[str]
        """
        return self._dns

    @dns.setter
    def dns(self, dns):
        """
        Sets the dns of this GenerateRecommendedNetworkDetails.
        The list of DNS server IP addresses. Maximum of 3 allowed.


        :param dns: The dns of this GenerateRecommendedNetworkDetails.
        :type: list[str]
        """
        self._dns = dns

    @property
    def ntp(self):
        """
        Gets the ntp of this GenerateRecommendedNetworkDetails.
        The list of NTP server IP addresses. Maximum of 3 allowed.


        :return: The ntp of this GenerateRecommendedNetworkDetails.
        :rtype: list[str]
        """
        return self._ntp

    @ntp.setter
    def ntp(self, ntp):
        """
        Sets the ntp of this GenerateRecommendedNetworkDetails.
        The list of NTP server IP addresses. Maximum of 3 allowed.


        :param ntp: The ntp of this GenerateRecommendedNetworkDetails.
        :type: list[str]
        """
        self._ntp = ntp

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this GenerateRecommendedNetworkDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this GenerateRecommendedNetworkDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this GenerateRecommendedNetworkDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this GenerateRecommendedNetworkDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this GenerateRecommendedNetworkDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this GenerateRecommendedNetworkDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this GenerateRecommendedNetworkDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this GenerateRecommendedNetworkDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
