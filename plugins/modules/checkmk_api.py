#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from collections import namedtuple
import ast
import requests


class WebAPI(object):
    def __init__(self, session):
        self.url = session.url
        self.username = session.username
        self.secret = session.secret
        self.verify = session.verify

        self.header = {
            'request_format': 'python',
            'output_format': 'python',
            '_username': self.username,
            '_secret': self.secret,
            }

    def query(self, action, request=None):
        payload = self.header.copy()
        payload['action'] = action
        if request:
            payload['request'] = repr(request)

        try:
            response = requests.get(self.url, params=payload, verify=self.verify, timeout=30)
            return ast.literal_eval(response.text)
        except:
            raise

    @property
    def result(self):
        return self.result

    @property
    def result_code(self):
        return self.result_code


class DataTuple(object):
    def __init__(self, url, username, secret, verify=True):
        name = namedtuple('name', ['url', 'username', 'secret', 'verify'])
        self.data = name(url, username, secret, verify)


class Hosts(object):
    def __init__(self, url, username, secret, verify=True, hostname=None):
        url = "%s/check_mk/webapi.py" % url.rstrip('/')
        session = DataTuple(url, username, secret, verify)
        self.session = WebAPI(session.data)
        self.hostname = hostname

    def _prepare_hostname(self, hostname=None):
        if hostname:
            self.hostname = hostname

    def pre_call(name):
        def _build_payload(fn):
            def _decorator(self, **kwargs):
                self._prepare_hostname(kwargs.get('hostname', None))
                if not self.hostname:
                    return fn(self, payload=None)

                if kwargs.get('payload', None):
                    payload = kwargs['payload']
                else: # we need to build the payload manually
                    payload = {'hostname': self.hostname}
                    if name == 'get':
                        payload['effective_attributes'] = kwargs.get('effective_attributes', 0)
                    if name in ['add', 'edit'] and kwargs.get('attributes', None):
                        payload['attributes'] = kwargs['attributes']
                    if name == 'add':
                        payload['folder'] = kwargs.get('folder', '')

                return fn(self, payload=payload)
            return _decorator
        return _build_payload

    @pre_call('get')
    def get(self, hostname=None, effective_attributes=None, payload=None):
        return self.session.query('get_host', payload)

    @pre_call('add')
    def add(self, hostname=None, folder=None, attributes=None, payload=None):
        return self.session.query('add_host', payload)

    @pre_call('delete')
    def delete(self, hostname=None, payload=None):
        return self.session.query('delete_host', payload)

    @pre_call('edit')
    def edit(self, hostname=None, attributes=None, payload=None):
        return self.session.query('edit_host', payload)


class Services(object):
    def __init__(self, url, username, secret, verify=True, hostname=None):
        url = "%s/check_mk/webapi.py" % url.rstrip('/')
        session = DataTuple(url, username, secret, verify)
        self.session = WebAPI(session.data)
        self.hostname = hostname


    def _prepare_hostname(self, hostname=None):
        if hostname:
            self.hostname = hostname

    def pre_call(fn):
        def _decorator(self, *args, **kwargs):
            self._prepare_hostname(kwargs.get('hostname', None))
            if not self.hostname:
                return fn(self, payload=None)

            if kwargs.get('payload', None):
                payload = kwargs['payload']
            else:
                payload = {'hostname': self.hostname}
                if kwargs.get('mode', None):
                    payload['mode'] = kwargs['mode']

            return fn(self, payload=payload)
        return _decorator

    @pre_call
    def discover(self, hostname=None, mode=None, payload=None):
        return self.session.query('discover_services', payload)


class Changes(object):
    def __init__(self, url, username, secret, verify=True):
        url = "%s/check_mk/webapi.py" % url.rstrip('/')
        session = DataTuple(url, username, secret, verify)
        self.session = WebAPI(session.data)

    def pre_call(fn):
        def _decorator(self, **kwargs):
            if kwargs.get('payload', None):
                payload = kwargs['payload']
            else:
                payload = {}
                if kwargs.get('sites', None):
                    payload['mode'] = 'specific'
                    payload['sites'] = list(kwargs['sites'])
                if kwargs.get('allow_foreign_changes', None):
                    payload['allow_foreign_changes'] = str(kwargs['allow_foreign_changes'])
                if kwargs.get('comment', None):
                    payload['comment'] = str(kwargs['comment'])
            return fn(self, payload=payload)
        return _decorator

    @pre_call
    def activate(self, sites=None, allow_foreign_changes=None, comment=None, payload=None):
        return self.session.query('activate_changes', payload)
