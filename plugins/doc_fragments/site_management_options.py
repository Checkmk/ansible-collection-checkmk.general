from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
    options:
        state:
            description:
                - The desired state of this site connection.
            type: str
            choices: ['present', 'absent', 'login', 'logout']
            default: present
        site_id:
            description:
                - The site ID.
            required: true
            type: str
        site_connection:
            description:
                - The settings of the site.
            type: dict
            suboptions:
                login_data:
                    description:
                        - The authentication data for a configuration connection.
                        - Only required when the state is "login".
                    type: dict
                    suboptions:
                        remote_username:
                            description:
                                - An administrative user's username.
                            type: str
                        remote_password:
                            description:
                                - The password for the username given.
                            type: str
                site_config:
                    description:
                        - A site's connection.
                        - Only required when that state is "present".
                    type: dict
                    suboptions:
                        status_connection:
                            description:
                                - A site's status connection.
                            type: dict
                            suboptions:
                                connection:
                                    description:
                                        - When connecting to remote site please make sure that
                                        - Livestatus over TCP is activated there.
                                        - You can use UNIX sockets to connect to foreign sites on
                                        - localhost.
                                    type: dict
                                    suboptions:
                                        socket_type:
                                            description:
                                                - The connection name. This can be
                                                - tcp, tcp6, unix or local.
                                            type: str
                                            choices: ['tcp', 'tcp6', 'unix', 'local']
                                        port:
                                            description:
                                                - The TCP port to connect to.
                                            type: int
                                        encrypted:
                                            description:
                                                - To enable an encrypted connection.
                                            type: bool
                                        verify:
                                            description:
                                                - Verify server certificate.
                                            type: bool
                                        host:
                                            description:
                                                - The IP or domain name of the host.
                                            type: str
                                        path:
                                            description:
                                                - When the connection name is unix,
                                                - this is the path to the unix socket.
                                            type: str
                                proxy:
                                    description:
                                        - The Livestatus proxy daemon configuration attributes.
                                    type: dict
                                    suboptions:
                                        use_livestatus_daemon:
                                            description:
                                                - Use livestatus daemon with direct connection
                                                - or with livestatus proxy.
                                            type: str
                                            choices: [with_proxy, direct]
                                        global_settings:
                                            description:
                                                - When use_livestatus_daemon is set to 'with_proxy',
                                                - you can set this to True to use global setting or
                                                - False to use custom parameters.
                                            type: bool
                                        tcp:
                                            description:
                                                - Allow access via TCP configuration.
                                            type: dict
                                            suboptions:
                                                port:
                                                    description:
                                                        - The TCP port to connect to.
                                                    type: int
                                                only_from:
                                                    description:
                                                        - Restrict access to these IP addresses.
                                                    type: list
                                                    elements: str
                                                tls:
                                                    description:
                                                        - Encrypt TCP Livestatus connections.
                                                    type: bool
                                                    default: false
                                        params:
                                            description:
                                                - The live status proxy daemon parameters.
                                            type: dict
                                            suboptions:
                                                channels:
                                                    description:
                                                        - The number of channels to keep open.
                                                    type: int
                                                    default: 5
                                                heartbeat:
                                                    description:
                                                        - The heartbeat interval and timeout
                                                        - configuration.
                                                    type: dict
                                                    suboptions:
                                                        interval:
                                                            description:
                                                                - The heartbeat interval
                                                                - for the TCP connection.
                                                            type: int
                                                            default: 5
                                                        timeout:
                                                            description:
                                                                - The heartbeat timeout
                                                                - for the TCP connection.
                                                            type: int
                                                            default: 2
                                                channel_timeout:
                                                    description:
                                                        - The timeout waiting for a free channel.
                                                    type: int
                                                    default: 3
                                                query_timeout:
                                                    description:
                                                        - The total query timeout.
                                                    type: int
                                                    default: 120
                                                connect_retry:
                                                    description:
                                                        - The cooling period after failed
                                                        - connect/heartbeat.
                                                    type: int
                                                    default: 4
                                                cache:
                                                    description:
                                                        - Enable caching.
                                                    type: bool
                                                    default: true
                                connect_timeout:
                                    description:
                                        - The time that the GUI waits for a connection to the site
                                        - to be established before the site is considered to be
                                        - unreachable.
                                    type: int
                                    default: 2
                                persistent_connection:
                                    description:
                                        - If you enable persistent connections then Multisite
                                        - will try to keep open the connection to the remote sites.
                                    type: bool
                                    default: false
                                url_prefix:
                                    description:
                                        - The URL prefix will be prepended to links of addons like
                                        - NagVis when a link to such applications points to a host
                                        - or service on that site.
                                    type: str
                                status_host:
                                    description:
                                        - By specifying a status host for each non-local connection
                                        - you prevent Multisite from running into timeouts when
                                        - remote sites do not respond.
                                    type: dict
                                    suboptions:
                                        status_host_set:
                                            description:
                                                - enabled for 'use the following status host' and
                                                - disabled for 'no status host'
                                            type: str
                                            choices: [enabled, disabled]
                                            default: disabled
                                        site:
                                            description:
                                                - The site ID of the status host.
                                            type: str
                                        host:
                                            description:
                                                - The host name of the status host.
                                            type: str
                                disable_in_status_gui:
                                    description:
                                        - If you disable a connection, then no data of this site will
                                        - be shown in the status GUI. The replication is not affected
                                        - by this, however.
                                    type: bool
                                    default: false
                        configuration_connection:
                            description:
                                - A site's configurationstatus connection.
                            type: dict
                            suboptions:
                                enable_replication:
                                    description:
                                        - Replication allows you to manage several monitoring sites
                                        - with a logically centralized setup.
                                        - Remote sites receive their configuration
                                        - from the central sites.
                                    type: bool
                                    default: false
                                url_of_remote_site:
                                    description:
                                        - URL of the remote Checkmk including /check_mk/.
                                        - This URL is in many cases the same as the URL-Prefix
                                        - but with check_mk/ appended, but it must always be
                                        - an absolute URL.
                                        - Unfortunately, this field is required by the REST API,
                                        - even if there is no configuration connection enabled.
                                    type: str
                                    default: http://localhost/nonexistant/check_mk/
                                disable_remote_configuration:
                                    description:
                                        - It is a good idea to disable access to Setup completely on
                                        - the remote site. Otherwise a user who does not now about
                                        - the replication could make local changes that are overridden
                                        - at the next configuration activation.
                                    type: bool
                                    default: true
                                ignore_tls_errors:
                                    description:
                                        - This might be needed to make the synchronization accept
                                        - problems with SSL certificates when using an SSL secured
                                        - connection.
                                    type: bool
                                    default: false
                                direct_login_to_web_gui_allowed:
                                    description:
                                        - When enabled, this site is marked for synchronisation every
                                        - time a web GUI related option is changed and users are
                                        - allowed to login to the web GUI of this site.
                                    type: bool
                                    default: true
                                user_sync:
                                    description:
                                        - By default the users are synchronized automatically in
                                        - the interval configured in the connection. For example
                                        - the LDAP connector synchronizes the users every five minutes
                                        - by default. The interval can be changed for each connection
                                        - individually in the connection settings. Please note that
                                        - the synchronization is only performed on the master site
                                        - in distributed setups by default.
                                    type: dict
                                    suboptions:
                                        sync_with_ldap_connections:
                                            description:
                                                - Sync with ldap connections. The options are
                                                - ldap, all, disabled.
                                            type: str
                                            choices: ['ldap', 'all', 'disabled']
                                            default: all
                                        ldap_connections:
                                            description:
                                                - A list of ldap connections.
                                            type: list
                                            elements: str
                                replicate_event_console:
                                    description:
                                        - This option enables the distribution of global settings and
                                        - rules of the Event Console to the remote site. Any change in
                                        - the local Event Console settings will mark the site as need
                                        - sync. A synchronization will automatically reload
                                        - the Event Console of the remote site.
                                    type: bool
                                    default: true
                                replicate_extensions:
                                    description:
                                        - If you enable the replication of MKPs then during each
                                        - Activate Changes MKPs that are installed on your central site
                                        - and all other files below the ~/local/ directory will be also
                                        - transferred to the remote site. All other MKPs and
                                        - files below ~/local/ on the remote site will be removed.
                                    type: bool
                                    default: true
                        secret:
                            description:
                                - The shared secret used by the central site to authenticate with the
                                - remote site for configuring Checkmk.
                            type: str
                            default:
                        basic_settings:
                            description:
                                - A site's basic settings.
                            type: dict
                            suboptions:
                                alias:
                                    description:
                                        - The alias of the site.
                                    type: str
                                customer:
                                    description:
                                        - The customer of the site (Checkmk Managed Edition - CME only).
                                    type: str
                                site_id:
                                    description:
                                        - The site ID.
                                    type: str
    """
