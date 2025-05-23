"""If the following ENV VAR were available, many end-to-end test cases would run.
LAB_OBO_CLIENT_SECRET=...
LAB_APP_CLIENT_ID=...
LAB_APP_CLIENT_CERT_PFX_PATH=...
LAB_OBO_PUBLIC_CLIENT_ID=...
LAB_OBO_CONFIDENTIAL_CLIENT_ID=...
"""
try:
    from dotenv import load_dotenv  # Use this only in local dev machine
    load_dotenv()  # take environment variables from .env.
except:
    pass
import base64
import logging
import os
import json
import time
import unittest
from urllib.parse import urlparse, parse_qs
import sys
try:
    from unittest.mock import patch, ANY
except:
    from mock import patch, ANY

import requests

import msal
from tests.http_client import MinimalHttpClient, MinimalResponse
from msal.oauth2cli import AuthCodeReceiver
from msal.oauth2cli.oidc import decode_part
from tests.broker_util import is_pymsalruntime_installed


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG if "-v" in sys.argv else logging.INFO)

try:
    from dotenv import load_dotenv  # Use this only in local dev machine
    load_dotenv()  # take environment variables from .env.
except ImportError:
    logger.warn("Run pip install -r requirements.txt for optional dependency")

_PYMSALRUNTIME_INSTALLED = is_pymsalruntime_installed()
_AZURE_CLI = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"

def _get_app_and_auth_code(
        client_id,
        client_secret=None,
        authority="https://login.microsoftonline.com/common",
        port=44331,
        scopes=["https://graph.microsoft.com/.default"],  # Microsoft Graph
        **kwargs):
    from msal.oauth2cli.authcode import obtain_auth_code
    if client_secret:
        app = msal.ConfidentialClientApplication(
            client_id,
            client_credential=client_secret,
            authority=authority, http_client=MinimalHttpClient())
    else:
        app = msal.PublicClientApplication(
            client_id, authority=authority, http_client=MinimalHttpClient())
    redirect_uri = "http://localhost:%d" % port
    ac = obtain_auth_code(port, auth_uri=app.get_authorization_request_url(
        scopes, redirect_uri=redirect_uri, **kwargs))
    assert ac is not None
    return (app, ac, redirect_uri)

def _render(url, description=None):
    # Render a url in html if description is available, otherwise return url as-is
    return "<a href='{url}' target=_blank>{description}</a>".format(
        url=url, description=description) if description else url


def _get_hint(html_mode=None, username=None, lab_name=None, username_uri=None):
    return "Sign in with {user} whose password is available from {lab}".format(
        user=("<b>{}</b>".format(username) if html_mode else username)
            if username
            else "the upn from {}".format(_render(
                username_uri, description="here" if html_mode else None)),
        lab=_render(
            "https://aka.ms/GetLabSecret?Secret=" + (lab_name or "msidlabXYZ"),
            description="this password api" if html_mode else None,
            ),
        )


@unittest.skipIf(os.getenv("TRAVIS_TAG"), "Skip e2e tests during tagged release")
class E2eTestCase(unittest.TestCase):

    def assertLoosely(self, response, assertion=None,
            skippable_errors=("invalid_grant", "interaction_required")):
        if response.get("error") in skippable_errors:
            logger.debug("Response = %s", response)
            # Some of these errors are configuration issues, not library issues
            raise unittest.SkipTest(response.get("error_description"))
        else:
            if assertion is None:
                assertion = lambda: self.assertIn(
                    "access_token", response,
                    "{error}: {error_description}".format(
                        # Do explicit response.get(...) rather than **response
                        error=response.get("error"),
                        error_description=response.get("error_description")))
            assertion()

    def assertCacheWorksForUser(
            self, result_from_wire, scope, username=None, data=None, auth_scheme=None):
        logger.debug(
            "%s: cache = %s, id_token_claims = %s",
            self.id(),
            json.dumps(self.app.token_cache._cache, indent=4),
            json.dumps(result_from_wire.get("id_token_claims"), indent=4),
            )
        # You can filter by predefined username, or let end user to choose one
        accounts = self.app.get_accounts(username=username)
        self.assertNotEqual(0, len(accounts))
        account = accounts[0]
        if ("scope" not in result_from_wire  # This is the usual case
                or  # Authority server could return different set of scopes
                set(scope) <= set(result_from_wire["scope"].split(" "))
                ):
            # Going to test acquire_token_silent(...) to locate an AT from cache
            silent_result = self.app.acquire_token_silent(
                scope, account=account, data=data or {}, auth_scheme=auth_scheme)
            self.assertIsNotNone(silent_result)
            self.assertIsNone(
                silent_result.get("refresh_token"), "acquire_token_silent() should return no RT")
            if auth_scheme:
                self.assertNotEqual(
                    self.app._TOKEN_SOURCE_CACHE, silent_result[self.app._TOKEN_SOURCE])
            else:
                self.assertEqual(
                    self.app._TOKEN_SOURCE_CACHE, silent_result[self.app._TOKEN_SOURCE])

        if "refresh_token" in result_from_wire:
            assert auth_scheme is None
            # Going to test acquire_token_silent(...) to obtain an AT by a RT from cache
            self.app.token_cache._cache["AccessToken"] = {}  # A hacky way to clear ATs
            silent_result = self.app.acquire_token_silent(
                scope, account=account, data=data or {})
            self.assertIsNotNone(silent_result,
                "We should get a result from acquire_token_silent(...) call")
            self.assertEqual(
                # We used to assert it this way:
                #   result_from_wire['access_token'] != silent_result['access_token']
                # but ROPC in B2C tends to return the same AT we obtained seconds ago.
                # Now looking back, "refresh_token grant would return a brand new AT"
                # was just an empirical observation but never a commitment in specs,
                # so we adjust our way to assert here.
                self.app._TOKEN_SOURCE_IDP, silent_result[self.app._TOKEN_SOURCE])

    def assertCacheWorksForApp(self, result_from_wire, scope):
        logger.debug(
            "%s: cache = %s, id_token_claims = %s",
            self.id(),
            json.dumps(self.app.token_cache._cache, indent=4),
            json.dumps(result_from_wire.get("id_token_claims"), indent=4),
            )
        self.assertIsNone(
            self.app.acquire_token_silent(scope, account=None),
            "acquire_token_silent(..., account=None) shall always return None")
        # Going to test acquire_token_for_client(...) to locate an AT from cache
        silent_result = self.app.acquire_token_for_client(scope)
        self.assertIsNotNone(silent_result)
        self.assertEqual(self.app._TOKEN_SOURCE_CACHE, silent_result[self.app._TOKEN_SOURCE])

    @classmethod
    def _build_app(cls,
            client_id,
            client_credential=None,
            authority="https://login.microsoftonline.com/common",
            oidc_authority=None,
            scopes=["https://graph.microsoft.com/.default"],  # Microsoft Graph
            http_client=None,
            azure_region=None,
            **kwargs):
        if client_credential:
            return msal.ConfidentialClientApplication(
                client_id,
                client_credential=client_credential,
                authority=authority,
                oidc_authority=oidc_authority,
                azure_region=azure_region,
                http_client=http_client or MinimalHttpClient(),
            )
        else:
            # Reuse same test cases, by running them with and without PyMsalRuntime installed
            return msal.PublicClientApplication(
                client_id,
                authority=authority,
                oidc_authority=oidc_authority,
                http_client=http_client or MinimalHttpClient(),
                enable_broker_on_windows=_PYMSALRUNTIME_INSTALLED,
                enable_broker_on_mac=_PYMSALRUNTIME_INSTALLED,
                )

    def _test_username_password(self,
            authority=None, client_id=None, username=None, password=None, scope=None,
            oidc_authority=None,
            client_secret=None,  # Since MSAL 1.11, confidential client has ROPC too
            azure_region=None,
            http_client=None,
            auth_scheme=None,
            **ignored):
        assert client_id and username and password and scope and (
            authority or oidc_authority)
        self.app = self._build_app(
            client_id, authority=authority, oidc_authority=oidc_authority,
            http_client=http_client,
            azure_region=azure_region,  # Regional endpoint does not support ROPC.
                # Here we just use it to test a regional app won't break ROPC.
            client_credential=client_secret)
        self.assertEqual(
            self.app.get_accounts(username=username), [], "Cache starts empty")
        result = self.app.acquire_token_by_username_password(
            username, password, scopes=scope, auth_scheme=auth_scheme)
        self.assertLoosely(result)
        self.assertCacheWorksForUser(
            result, scope,
            username=username,  # Our implementation works even when "profile" scope was not requested, or when profile claims is unavailable in B2C
            auth_scheme=auth_scheme,
            )
        return result

    @unittest.skipIf(
        os.getenv("TRAVIS"),  # It is set when running on TravisCI or Github Actions
        "Although it is doable, we still choose to skip device flow to save time")
    def _test_device_flow(
        self,
        *,
        client_id=None, authority=None, oidc_authority=None, scope=None,
        **ignored
    ):
        assert client_id and scope and (authority or oidc_authority)
        self.app = self._build_app(
            client_id, authority=authority, oidc_authority=oidc_authority)
        flow = self.app.initiate_device_flow(scopes=scope)
        assert "user_code" in flow, "DF does not seem to be provisioned: %s".format(
            json.dumps(flow, indent=4))
        logger.info(flow["message"])

        duration = 60
        logger.info("We will wait up to %d seconds for you to sign in" % duration)
        flow["expires_at"] = min(  # Shorten the time for quick test
            flow["expires_at"], time.time() + duration)
        result = self.app.acquire_token_by_device_flow(flow)
        self.assertLoosely(  # It will skip this test if there is no user interaction
            result,
            assertion=lambda: self.assertIn('access_token', result),
            skippable_errors=self.app.client.DEVICE_FLOW_RETRIABLE_ERRORS)
        if "access_token" not in result:
            self.skipTest("End user did not complete Device Flow in time")
        self.assertCacheWorksForUser(result, scope, username=None)
        result["access_token"] = result["refresh_token"] = "************"
        logger.info(
            "%s obtained tokens: %s", self.id(), json.dumps(result, indent=4))

    @unittest.skipIf(os.getenv("TRAVIS"), "Browser automation is not yet implemented")
    def _test_acquire_token_interactive(
            self, *, client_id=None, authority=None, scope=None, port=None,
            oidc_authority=None,
            username=None, lab_name=None,
            username_uri="",  # Unnecessary if you provided username and lab_name
            data=None,  # Needed by ssh-cert feature
            prompt=None,
            enable_msa_passthrough=None,
            auth_scheme=None,
            **ignored):
        assert client_id and scope and (authority or oidc_authority)
        self.app = self._build_app(
            client_id, authority=authority, oidc_authority=oidc_authority)
        logger.info(_get_hint(  # Useful when testing broker which shows no welcome_template
            username=username, lab_name=lab_name, username_uri=username_uri))
        result = self.app.acquire_token_interactive(
            scope,
            login_hint=username,
            prompt=prompt,
            timeout=120,
            port=port,
            parent_window_handle=self.app.CONSOLE_WINDOW_HANDLE,  # This test app is a console app
            enable_msa_passthrough=enable_msa_passthrough,  # Needed when testing MSA-PT app
            welcome_template=  # This is an undocumented feature for testing
                """<html><body><h1>{id}</h1><ol>
    <li>{hint}</li>
    <li><a href="$auth_uri">Sign In</a> or <a href="$abort_uri">Abort</a></li>
    </ol></body></html>""".format(id=self.id(), hint=_get_hint(
                html_mode=True,
                username=username, lab_name=lab_name, username_uri=username_uri)),
            auth_scheme=auth_scheme,
            data=data or {},
            )
        self.assertIn(
            "access_token", result,
            "{error}: {error_description}".format(
                # Note: No interpolation here, cause error won't always present
                error=result.get("error"),
                error_description=result.get("error_description")))
        if username and result.get("id_token_claims", {}).get("preferred_username"):
            self.assertEqual(
                username, result["id_token_claims"]["preferred_username"],
                "You are expected to sign in as account {}, but tokens returned is for {}".format(
                    username, result["id_token_claims"]["preferred_username"]))
        self.assertCacheWorksForUser(
            result, scope, username=None, data=data or {}, auth_scheme=auth_scheme)
        return result  # For further testing


@unittest.skipUnless(
    msal.application._is_running_in_cloud_shell(),
    "Manually run this test case from inside Cloud Shell")
class CloudShellTestCase(E2eTestCase):
    scope_that_requires_no_managed_device = "https://management.core.windows.net/"  # Scopes came from https://msazure.visualstudio.com/One/_git/compute-CloudShell?path=/src/images/agent/env/envconfig.PROD.json&version=GBmaster&_a=contents

    def setUpClass(cls):
        # Doing it here instead of as a class member,
        # otherwise its overhead incurs even when running other cases
        cls.app = msal.PublicClientApplication("client_id")

    def test_access_token_should_be_obtained_for_a_supported_scope(self):
        result = self.app.acquire_token_interactive(
            [self.scope_that_requires_no_managed_device], prompt="none")
        self.assertEqual(
            "Bearer", result.get("token_type"), "Unexpected result: %s" % result)
        self.assertIsNotNone(result.get("access_token"))


THIS_FOLDER = os.path.dirname(__file__)
CONFIG = os.path.join(THIS_FOLDER, "config.json")
@unittest.skipUnless(os.path.exists(CONFIG), "Optional %s not found" % CONFIG)
class FileBasedTestCase(E2eTestCase):
    # This covers scenarios that are not currently available for test automation.
    # So they mean to be run on maintainer's machine for semi-automated tests.

    @classmethod
    def setUpClass(cls):
        with open(CONFIG) as f:
            cls.config = json.load(f)

    def skipUnlessWithConfig(self, fields):
        for field in fields:
            if field not in self.config:
                self.skipTest('Skipping due to lack of configuration "%s"' % field)

    def test_username_password(self):
        self.skipUnlessWithConfig(["client_id", "username", "password", "scope"])
        self._test_username_password(**self.config)

    def _get_app_and_auth_code(self, scopes=None, **kwargs):
        return _get_app_and_auth_code(
            self.config["client_id"],
            client_secret=self.config.get("client_secret"),
            authority=self.config.get("authority"),
            port=self.config.get("listen_port", 44331),
            scopes=scopes or self.config["scope"],
            **kwargs)

    def _test_auth_code(self, auth_kwargs, token_kwargs):
        self.skipUnlessWithConfig(["client_id", "scope"])
        (self.app, ac, redirect_uri) = self._get_app_and_auth_code(**auth_kwargs)
        result = self.app.acquire_token_by_authorization_code(
            ac, self.config["scope"], redirect_uri=redirect_uri, **token_kwargs)
        logger.debug("%s.cache = %s",
            self.id(), json.dumps(self.app.token_cache._cache, indent=4))
        self.assertIn(
            "access_token", result,
            "{error}: {error_description}".format(
                # Note: No interpolation here, cause error won't always present
                error=result.get("error"),
                error_description=result.get("error_description")))
        self.assertCacheWorksForUser(result, self.config["scope"], username=None)

    def test_auth_code(self):
        self._test_auth_code({}, {})

    def test_auth_code_with_matching_nonce(self):
        self._test_auth_code({"nonce": "foo"}, {"nonce": "foo"})

    def test_auth_code_with_mismatching_nonce(self):
        self.skipUnlessWithConfig(["client_id", "scope"])
        (self.app, ac, redirect_uri) = self._get_app_and_auth_code(nonce="foo")
        with self.assertRaises(ValueError):
            self.app.acquire_token_by_authorization_code(
                ac, self.config["scope"], redirect_uri=redirect_uri, nonce="bar")

    def test_client_secret(self):
        self.skipUnlessWithConfig(["client_id", "client_secret"])
        self.app = msal.ConfidentialClientApplication(
            self.config["client_id"],
            client_credential=self.config.get("client_secret"),
            authority=self.config.get("authority"),
            http_client=MinimalHttpClient())
        scope = self.config.get("scope", [])
        result = self.app.acquire_token_for_client(scope)
        self.assertIn('access_token', result)
        self.assertCacheWorksForApp(result, scope)

    def test_client_certificate(self):
        self.skipUnlessWithConfig(["client_id", "client_certificate"])
        client_cert = self.config["client_certificate"]
        assert "private_key_path" in client_cert and "thumbprint" in client_cert
        with open(os.path.join(THIS_FOLDER, client_cert['private_key_path'])) as f:
            private_key = f.read()  # Should be in PEM format
        self.app = msal.ConfidentialClientApplication(
            self.config['client_id'],
            {"private_key": private_key, "thumbprint": client_cert["thumbprint"]},
            http_client=MinimalHttpClient())
        scope = self.config.get("scope", [])
        result = self.app.acquire_token_for_client(scope)
        self.assertIn('access_token', result)
        self.assertCacheWorksForApp(result, scope)

    def test_subject_name_issuer_authentication(self):
        self.skipUnlessWithConfig(["client_id", "client_certificate"])
        client_cert = self.config["client_certificate"]
        assert "private_key_path" in client_cert and "thumbprint" in client_cert
        if not "public_certificate" in client_cert:
            self.skipTest("Skipping SNI test due to lack of public_certificate")
        with open(os.path.join(THIS_FOLDER, client_cert['private_key_path'])) as f:
            private_key = f.read()  # Should be in PEM format
        with open(os.path.join(THIS_FOLDER, client_cert['public_certificate'])) as f:
            public_certificate = f.read()
        self.app = msal.ConfidentialClientApplication(
            self.config['client_id'], authority=self.config["authority"],
            client_credential={
                "private_key": private_key,
                "thumbprint": self.config["thumbprint"],
                "public_certificate": public_certificate,
                },
            http_client=MinimalHttpClient())
        scope = self.config.get("scope", [])
        result = self.app.acquire_token_for_client(scope)
        self.assertIn('access_token', result)
        self.assertCacheWorksForApp(result, scope)

    def test_client_assertion(self):
        self.skipUnlessWithConfig(["client_id", "client_assertion"])
        self.app = msal.ConfidentialClientApplication(
            self.config['client_id'], authority=self.config["authority"],
            client_credential={"client_assertion": self.config["client_assertion"]},
            http_client=MinimalHttpClient())
        scope = self.config.get("scope", [])
        result = self.app.acquire_token_for_client(scope)
        self.assertIn('access_token', result)
        self.assertCacheWorksForApp(result, scope)

@unittest.skipUnless(os.path.exists(CONFIG), "Optional %s not found" % CONFIG)
class DeviceFlowTestCase(E2eTestCase):  # A leaf class so it will be run only once
    @classmethod
    def setUpClass(cls):
        with open(CONFIG) as f:
            cls.config = json.load(f)

    def test_device_flow(self):
        self._test_device_flow(**self.config)


def get_lab_app(
        env_client_id="LAB_APP_CLIENT_ID",
        env_name2="LAB_APP_CLIENT_SECRET",  # A var name that hopefully avoids false alarm
        env_client_cert_path="LAB_APP_CLIENT_CERT_PFX_PATH",
        authority="https://login.microsoftonline.com/"
            "72f988bf-86f1-41af-91ab-2d7cd011db47",  # Microsoft tenant ID
        timeout=None,
        **kwargs):
    """Returns the lab app as an MSAL confidential client.

    Get it from environment variables if defined, otherwise fall back to use MSI.
    """
    logger.info(
        "Reading ENV variables %s and %s for lab app defined at "
        "https://docs.msidlab.com/accounts/confidentialclient.html",
        env_client_id, env_name2)
    if os.getenv(env_client_id) and os.getenv(env_client_cert_path):
        # id came from https://docs.msidlab.com/accounts/confidentialclient.html
        client_id = os.getenv(env_client_id)
        client_credential = {
            "private_key_pfx_path":
                # Cert came from https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Certificate/https://msidlabs.vault.azure.net/certificates/LabAuth
                os.getenv(env_client_cert_path),
            "public_certificate": True,  # Opt in for SNI
            }
    elif os.getenv(env_client_id) and os.getenv(env_name2):
        # Data came from here
        # https://docs.msidlab.com/accounts/confidentialclient.html
        client_id = os.getenv(env_client_id)
        client_credential = os.getenv(env_name2)
    else:
        logger.info("ENV variables are not defined. Fall back to MSI.")
        # See also https://microsoft.sharepoint-df.com/teams/MSIDLABSExtended/SitePages/Programmatically-accessing-LAB-API's.aspx
        raise unittest.SkipTest("MSI-based mechanism has not been implemented yet")
    return msal.ConfidentialClientApplication(
            client_id,
            client_credential=client_credential,
            authority=authority,
            http_client=MinimalHttpClient(timeout=timeout),
            **kwargs)

class LabTokenError(RuntimeError):
    pass

def get_session(lab_app, scopes):  # BTW, this infrastructure tests the confidential client flow
    logger.info("Creating session")
    result = lab_app.acquire_token_for_client(scopes)
    if not result.get("access_token"):
        raise LabTokenError(
            "Unable to obtain token for lab. Encountered {}: {}".format(
            result.get("error"), result.get("error_description")
        ))
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer %s" % result["access_token"]})
    session.hooks["response"].append(lambda r, *args, **kwargs: r.raise_for_status())
    return session


class LabBasedTestCase(E2eTestCase):
    _secrets = {}
    adfs2019_scopes = ["placeholder"]  # Need this to satisfy MSAL API surface.
        # Internally, MSAL will also append more scopes like "openid" etc..
        # ADFS 2019 will issue tokens for valid scope only, by default "openid".
        # https://docs.microsoft.com/en-us/windows-server/identity/ad-fs/overview/ad-fs-faq#what-permitted-scopes-are-supported-by-ad-fs

    @classmethod
    def setUpClass(cls):
        # https://docs.msidlab.com/accounts/apiaccess.html#code-snippet
        cls.session = get_session(get_lab_app(), [
                "https://request.msidlab.com/.default",  # A lab change since June 10, 2024
            ])

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    @classmethod
    def get_lab_app_object(cls, client_id=None, **query):  # https://msidlab.com/swagger/index.html
        url = "https://msidlab.com/api/app/{}".format(client_id or "")
        resp = cls.session.get(url, params=query)
        result = resp.json()[0]
        result["scopes"] = [  # Raw data has extra space, such as "s1, s2"
            s.strip() for s in result["defaultScopes"].split(',')]
        return result

    @classmethod
    def get_lab_user_secret(cls, lab_name="msidlab4"):
        lab_name = lab_name.lower()
        if lab_name not in cls._secrets:
            logger.info("Querying lab user password for %s", lab_name)
            url = "https://msidlab.com/api/LabSecret?secret=%s" % lab_name
            resp = cls.session.get(url)
            cls._secrets[lab_name] = resp.json()["value"]
        return cls._secrets[lab_name]

    @classmethod
    def get_lab_user(cls, **query):  # https://docs.msidlab.com/labapi/userapi.html
        resp = cls.session.get("https://msidlab.com/api/user", params=query)
        result = resp.json()[0]
        assert result.get("upn"), "Found no test user but {}".format(
            json.dumps(result, indent=2))
        _env = query.get("azureenvironment", "").lower()
        authority_base = {
            "azureusgovernment": "https://login.microsoftonline.us/"
            }.get(_env, "https://login.microsoftonline.com/")
        scope = {
            "azureusgovernment": ["https://graph.microsoft.us/.default"],
            }.get(_env, ["https://graph.microsoft.com/.default"])
        return {  # Mapping lab API response to our simplified configuration format
            "authority": authority_base + result["tenantID"],
            "client_id": result["appId"],
            "username": result["upn"],
            "lab_name": result["labName"],
            "scope": scope,
            }

    @unittest.skipIf(os.getenv("TRAVIS"), "Browser automation is not yet implemented")
    def _test_acquire_token_by_auth_code(
            self, client_id=None, authority=None, port=None, scope=None,
            **ignored):
        assert client_id and authority and port and scope
        (self.app, ac, redirect_uri) = _get_app_and_auth_code(
            client_id, authority=authority, port=port, scopes=scope)
        result = self.app.acquire_token_by_authorization_code(
            ac, scope, redirect_uri=redirect_uri)
        logger.debug(
            "%s: cache = %s, id_token_claims = %s",
            self.id(),
            json.dumps(self.app.token_cache._cache, indent=4),
            json.dumps(result.get("id_token_claims"), indent=4),
            )
        self.assertIn(
            "access_token", result,
            "{error}: {error_description}".format(
                # Note: No interpolation here, cause error won't always present
                error=result.get("error"),
                error_description=result.get("error_description")))
        self.assertCacheWorksForUser(result, scope, username=None)

    @unittest.skipIf(os.getenv("TRAVIS"), "Browser automation is not yet implemented")
    def _test_acquire_token_by_auth_code_flow(
            self, client_id=None, authority=None, port=None, scope=None,
            username=None, lab_name=None,
            username_uri="",  # Optional if you provided username and lab_name
            **ignored):
        assert client_id and authority and scope
        self.app = msal.ClientApplication(
            client_id, authority=authority, http_client=MinimalHttpClient())
        with AuthCodeReceiver(port=port) as receiver:
            flow = self.app.initiate_auth_code_flow(
                scope,
                redirect_uri="http://localhost:%d" % receiver.get_port(),
                )
            auth_response = receiver.get_auth_response(
                auth_uri=flow["auth_uri"], state=flow["state"], timeout=60,
                welcome_template="""<html><body><h1>{id}</h1><ol>
    <li>{hint}</li>
    <li><a href="$auth_uri">Sign In</a> or <a href="$abort_uri">Abort</a></li>
    </ol></body></html>""".format(id=self.id(), hint=_get_hint(
                    html_mode=True,
                    username=username, lab_name=lab_name, username_uri=username_uri)),
                )
        if auth_response is None:
            self.skipTest("Timed out. Did not have test settings in hand? Prepare and retry.")
        self.assertIsNotNone(
            auth_response.get("code"), "Error: {}, Detail: {}".format(
                auth_response.get("error"), auth_response))
        result = self.app.acquire_token_by_auth_code_flow(flow, auth_response)
        logger.debug(
            "%s: cache = %s, id_token_claims = %s",
            self.id(),
            json.dumps(self.app.token_cache._cache, indent=4),
            json.dumps(result.get("id_token_claims"), indent=4),
            )
        self.assertIn(
            "access_token", result,
            "{error}: {error_description}".format(
                # Note: No interpolation here, cause error won't always present
                error=result.get("error"),
                error_description=result.get("error_description")))
        if username and result.get("id_token_claims", {}).get("preferred_username"):
            self.assertEqual(
                username, result["id_token_claims"]["preferred_username"],
                "You are expected to sign in as account {}, but tokens returned is for {}".format(
                    username, result["id_token_claims"]["preferred_username"]))
        self.assertCacheWorksForUser(result, scope, username=None)

    def _test_acquire_token_obo(self, config_pca, config_cca,
            azure_region=None,  # Regional endpoint does not really support OBO.
                # Here we just test regional apps won't adversely break OBO
            http_client=None,
            ):
        if "client_secret" not in config_pca:
            # 1.a An app obtains a token representing a user, for our mid-tier service
            result = msal.PublicClientApplication(
                config_pca["client_id"], authority=config_pca["authority"],
                azure_region=azure_region,
                http_client=http_client or MinimalHttpClient(),
                ).acquire_token_by_username_password(
                    config_pca["username"], config_pca["password"],
                    scopes=config_pca["scope"],
                )
        else:  # We repurpose the config_pca to contain client_secret for cca app 1
            # 1.b An app obtains a token representing itself, for our mid-tier service
            result = msal.ConfidentialClientApplication(
                config_pca["client_id"], authority=config_pca["authority"],
                client_credential=config_pca["client_secret"],
                azure_region=azure_region,
                http_client=http_client or MinimalHttpClient(),
                ).acquire_token_for_client(scopes=config_pca["scope"])
        assertion = result.get("access_token")
        self.assertIsNotNone(assertion, "First app failed to get AT. {}".format(
            json.dumps(result, indent=2)))

        # 2. Our mid-tier service uses OBO to obtain a token for downstream service
        cca = msal.ConfidentialClientApplication(
            config_cca["client_id"],
            client_credential=config_cca["client_secret"],
            authority=config_cca["authority"],
            azure_region=azure_region,
            http_client=http_client or MinimalHttpClient(),
            # token_cache= ...,  # Default token cache is all-tokens-store-in-memory.
                # That's fine if OBO app uses short-lived msal instance per session.
                # Otherwise, the OBO app need to implement a one-cache-per-user setup.
            )
        cca_result = cca.acquire_token_on_behalf_of(assertion, config_cca["scope"])
        self.assertIsNotNone(cca_result.get("access_token"), "OBO call failed: {}".format(
            json.dumps(cca_result, indent=2)))

        # 3. Now the OBO app can simply store downstream token(s) in same session.
        #    Alternatively, if you want to persist the downstream AT, and possibly
        #    the RT (if any) for prolonged access even after your own AT expires,
        #    now it is the time to persist current cache state for current user.
        #    Assuming you already did that (which is not shown in this test case),
        #    the following part shows one of the ways to obtain an AT from cache.
        username = cca_result.get("id_token_claims", {}).get("preferred_username")
        accounts = cca.get_accounts(username=username)
        if username is not None:  # It means CCA have requested an IDT w/ "profile" scope
            assert config_cca["username"] == username, "Incorrect test case configuration"
            self.assertEqual(1, len(accounts), "App is supposed to partition token cache per user")
        account = accounts[0]  # Alternatively, cca app could just loop through each account
        result = cca.acquire_token_silent(config_cca["scope"], account)
        self.assertTrue(
            result and result.get("access_token") == cca_result["access_token"],
            "CCA should hit an access token from cache: {}".format(
                json.dumps(cca.token_cache._cache, indent=2)))
        if "refresh_token" in cca_result:
            result = cca.acquire_token_silent(
                config_cca["scope"], account=account, force_refresh=True)
            self.assertTrue(
                result and "access_token" in result,
                "CCA should get an AT silently, but we got this instead: {}".format(result))
            self.assertNotEqual(
                result["access_token"], cca_result["access_token"],
                "CCA should get a new AT")
        else:
            logger.info("AAD did not issue a RT for OBO flow")

    def _test_acquire_token_by_client_secret(
            self, client_id=None, client_secret=None, authority=None, scope=None,
            oidc_authority=None,
            **ignored):
        assert client_id and client_secret and scope and (
            authority or oidc_authority)
        self.app = msal.ConfidentialClientApplication(
            client_id, client_credential=client_secret, authority=authority,
            oidc_authority=oidc_authority,
            http_client=MinimalHttpClient())
        result = self.app.acquire_token_for_client(scope)
        self.assertIsNotNone(result.get("access_token"), "Got %s instead" % result)
        self.assertCacheWorksForApp(result, scope)


class PopWithExternalKeyTestCase(LabBasedTestCase):
    def _test_service_principal(self):
        app = get_lab_app()  # Any SP can obtain an ssh-cert. Here we use the lab app.
        result = app.acquire_token_for_client(self.SCOPE, data=self.DATA1)
        self.assertIsNotNone(result.get("access_token"), "Encountered {}: {}".format(
            result.get("error"), result.get("error_description")))
        self.assertEqual(self.EXPECTED_TOKEN_TYPE, result["token_type"])
        self.assertEqual(result["token_source"], "identity_provider")

        # Test cache hit
        cached_result = app.acquire_token_for_client(self.SCOPE, data=self.DATA1)
        self.assertIsNotNone(
            cached_result.get("access_token"), "Encountered {}: {}".format(
            cached_result.get("error"), cached_result.get("error_description")))
        self.assertEqual(self.EXPECTED_TOKEN_TYPE, cached_result["token_type"])
        self.assertEqual(cached_result["token_source"], "cache")

        # refresh_token grant can fetch an ssh-cert bound to a different key
        refreshed_result = app.acquire_token_for_client(self.SCOPE, data=self.DATA2)
        self.assertIsNotNone(
            refreshed_result.get("access_token"), "Encountered {}: {}".format(
            refreshed_result.get("error"), refreshed_result.get("error_description")))
        self.assertEqual(self.EXPECTED_TOKEN_TYPE, refreshed_result["token_type"])
        self.assertEqual(refreshed_result["token_source"], "identity_provider")

    def _test_user_account(self):
        lab_user = self.get_lab_user(usertype="cloud")
        result = self._test_acquire_token_interactive(
            client_id="04b07795-8ddb-461a-bbee-02f9e1bf7b46",  # Azure CLI is one
                # of the only 2 clients that are PreAuthz to use ssh cert feature
            authority="https://login.microsoftonline.com/common",
            scope=self.SCOPE,
            data=self.DATA1,
            username=lab_user["username"],
            lab_name=lab_user["lab_name"],
            prompt="none" if msal.application._is_running_in_cloud_shell() else None,
            )   # It already tests reading AT from cache, and using RT to refresh
                # acquire_token_silent() would work because we pass in the same key
        self.assertIsNotNone(result.get("access_token"), "Encountered {}: {}".format(
            result.get("error"), result.get("error_description")))
        self.assertEqual(self.EXPECTED_TOKEN_TYPE, result["token_type"])
        self.assertEqual(result["token_source"], "identity_provider")
        logger.debug("%s.cache = %s",
            self.id(), json.dumps(self.app.token_cache._cache, indent=4))

        # refresh_token grant can hit an ssh-cert bound to the same key
        account = self.app.get_accounts()[0]
        cached_result = self.app.acquire_token_silent(
            self.SCOPE, account=account, data=self.DATA1)
        self.assertIsNotNone(cached_result)
        self.assertEqual(self.EXPECTED_TOKEN_TYPE, cached_result["token_type"])
        ## Actually, the self._test_acquire_token_interactive() already contained
        ## a built-in refresh test, so the token in cache has been refreshed already.
        ## Therefore, the following line won't pass, which is expected.
        #self.assertEqual(result["access_token"], cached_result['access_token'])
        self.assertEqual(cached_result["token_source"], "cache")

        # refresh_token grant can fetch an ssh-cert bound to a different key
        account = self.app.get_accounts()[0]
        refreshed_result = self.app.acquire_token_silent(
            self.SCOPE, account=account, data=self.DATA2)
        self.assertIsNotNone(refreshed_result)
        self.assertEqual(self.EXPECTED_TOKEN_TYPE, refreshed_result["token_type"])
        self.assertNotEqual(result["access_token"], refreshed_result['access_token'])
        self.assertEqual(refreshed_result["token_source"], "identity_provider")


class SshCertTestCase(PopWithExternalKeyTestCase):
    EXPECTED_TOKEN_TYPE = "ssh-cert"
    _JWK1 = """{"kty":"RSA", "n":"2tNr73xwcj6lH7bqRZrFzgSLj7OeLfbn8216uOMDHuaZ6TEUBDN8Uz0ve8jAlKsP9CQFCSVoSNovdE-fs7c15MxEGHjDcNKLWonznximj8pDGZQjVdfK-7mG6P6z-lgVcLuYu5JcWU_PeEqIKg5llOaz-qeQ4LEDS4T1D2qWRGpAra4rJX1-kmrWmX_XIamq30C9EIO0gGuT4rc2hJBWQ-4-FnE1NXmy125wfT3NdotAJGq5lMIfhjfglDbJCwhc8Oe17ORjO3FsB5CLuBRpYmP7Nzn66lRY3Fe11Xz8AEBl3anKFSJcTvlMnFtu3EpD-eiaHfTgRBU7CztGQqVbiQ", "e":"AQAB"}"""
    _JWK2 = """{"kty":"RSA", "n":"72u07mew8rw-ssw3tUs9clKstGO2lvD7ZNxJU7OPNKz5PGYx3gjkhUmtNah4I4FP0DuF1ogb_qSS5eD86w10Wb1ftjWcoY8zjNO9V3ph-Q2tMQWdDW5kLdeU3-EDzc0HQeou9E0udqmfQoPbuXFQcOkdcbh3eeYejs8sWn3TQprXRwGh_TRYi-CAurXXLxQ8rp-pltUVRIr1B63fXmXhMeCAGwCPEFX9FRRs-YHUszUJl9F9-E0nmdOitiAkKfCC9LhwB9_xKtjmHUM9VaEC9jWOcdvXZutwEoW2XPMOg0Ky-s197F9rfpgHle2gBrXsbvVMvS0D-wXg6vsq6BAHzQ", "e":"AQAB"}"""
    DATA1 = {"token_type": "ssh-cert", "key_id": "key1", "req_cnf": _JWK1}
    DATA2 = {"token_type": "ssh-cert", "key_id": "key2", "req_cnf": _JWK2}
    _SCOPE_USER = ["https://pas.windows.net/CheckMyAccess/Linux/user_impersonation"]
    _SCOPE_SP = ["https://pas.windows.net/CheckMyAccess/Linux/.default"]
    SCOPE = _SCOPE_SP  # Historically there was a separation, at 2021 it is unified

    def test_service_principal(self):
        self._test_service_principal()

    def test_user_account(self):
        self._test_user_account()


def _data_for_pop(key):
    raw_req_cnf = json.dumps({"kid": key, "xms_ksl": "sw"})
    return {  # Sampled from Azure CLI's plugin connectedk8s
        'token_type': 'pop',
        'key_id': key,
        "req_cnf": base64.urlsafe_b64encode(raw_req_cnf.encode('utf-8')).decode('utf-8').rstrip('='),
            # Note: Sending raw_req_cnf without base64 encoding would result in an http 500 error
    }  # See also https://github.com/Azure/azure-cli-extensions/blob/main/src/connectedk8s/azext_connectedk8s/_clientproxyutils.py#L86-L92


class AtPopWithExternalKeyTestCase(PopWithExternalKeyTestCase):
    EXPECTED_TOKEN_TYPE = "pop"
    DATA1 = _data_for_pop('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA-AAAAAAAA')  # Fake key with a certain format and length
    DATA2 = _data_for_pop('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB-BBBBBBBB')  # Fake key with a certain format and length
    SCOPE = [
        '6256c85f-0aad-4d50-b960-e6e9b21efe35/.default',  # Azure CLI's connectedk8s plugin uses this
            # https://github.com/Azure/azure-cli-extensions/pull/4468/files#diff-a47efa3186c7eb4f1176e07d0b858ead0bf4a58bfd51e448ee3607a5b4ef47f6R116
    ]

    def test_service_principal(self):
        self._test_service_principal()

    def test_user_account(self):
        self._test_user_account()


class WorldWideTestCase(LabBasedTestCase):

    def test_aad_managed_user(self):  # Pure cloud
        config = self.get_lab_user(usertype="cloud")
        config["password"] = self.get_lab_user_secret(config["lab_name"])
        self._test_username_password(**config)

    def test_adfs4_fed_user(self):
        config = self.get_lab_user(usertype="federated", federationProvider="ADFSv4")
        config["password"] = self.get_lab_user_secret(config["lab_name"])
        self._test_username_password(**config)

    @unittest.skip("ADFSv3 is decommissioned in our test environment")
    def test_adfs3_fed_user(self):
        config = self.get_lab_user(usertype="federated", federationProvider="ADFSv3")
        config["password"] = self.get_lab_user_secret(config["lab_name"])
        self._test_username_password(**config)

    @unittest.skip("ADFSv2 is decommissioned in our test environment")
    def test_adfs2_fed_user(self):
        config = self.get_lab_user(usertype="federated", federationProvider="ADFSv2")
        config["password"] = self.get_lab_user_secret(config["lab_name"])
        self._test_username_password(**config)

    def test_adfs2019_fed_user(self):
        try:
            config = self.get_lab_user(usertype="federated", federationProvider="ADFSv2019")
            config["password"] = self.get_lab_user_secret(config["lab_name"])
            self._test_username_password(**config)
        except requests.exceptions.HTTPError:
            if os.getenv("TRAVIS"):
                self.skipTest("MEX endpoint in our test environment tends to fail")
            raise

    def test_cloud_acquire_token_interactive(self):
        self._test_acquire_token_interactive(**self.get_lab_user(usertype="cloud"))

    def test_msa_pt_app_signin_via_organizations_authority_without_login_hint(self):
        """There is/was an upstream bug. See test case full docstring for the details.

        When a MSAL-PT flow that account control is launched, user has 2+ AAD accounts in WAM,
        selects an AAD account that is NOT the default AAD account from the OS,
        it will incorrectly get tokens for default AAD account.
        """
        self._test_acquire_token_interactive(**dict(
            self.get_lab_user(usertype="cloud"),  # This is generally not the current laptop's default AAD account
            authority="https://login.microsoftonline.com/organizations",
            client_id="04b07795-8ddb-461a-bbee-02f9e1bf7b46",  # Azure CLI is an MSA-PT app
            enable_msa_passthrough=True,
            prompt="select_account",  # In MSAL Python, this resets login_hint
            ))

    def test_ropc_adfs2019_onprem(self):
        # Configuration is derived from https://github.com/AzureAD/microsoft-authentication-library-for-dotnet/blob/4.7.0/tests/Microsoft.Identity.Test.Common/TestConstants.cs#L250-L259
        config = self.get_lab_user(usertype="onprem", federationProvider="ADFSv2019")
        config["authority"] = "https://fs.%s.com/adfs" % config["lab_name"]
        config["scope"] = self.adfs2019_scopes
        config["password"] = self.get_lab_user_secret(config["lab_name"])
        self._test_username_password(**config)

    def test_adfs2019_onprem_acquire_token_by_auth_code(self):
        """When prompted, you can manually login using this account:

        # https://msidlab.com/api/user?usertype=onprem&federationprovider=ADFSv2019
        username = "..."  # The upn from the link above
        password="***"  # From https://aka.ms/GetLabSecret?Secret=msidlabXYZ
        """
        config = self.get_lab_user(usertype="onprem", federationProvider="ADFSv2019")
        config["authority"] = "https://fs.%s.com/adfs" % config["lab_name"]
        config["scope"] = self.adfs2019_scopes
        config["port"] = 8080
        self._test_acquire_token_by_auth_code(**config)

    def test_adfs2019_onprem_acquire_token_by_auth_code_flow(self):
        config = self.get_lab_user(usertype="onprem", federationProvider="ADFSv2019")
        self._test_acquire_token_by_auth_code_flow(**dict(
            config,
            authority="https://fs.%s.com/adfs" % config["lab_name"],
            scope=self.adfs2019_scopes,
            port=8080,
            ))

    def test_adfs2019_onprem_acquire_token_interactive(self):
        config = self.get_lab_user(usertype="onprem", federationProvider="ADFSv2019")
        self._test_acquire_token_interactive(**dict(
            config,
            authority="https://fs.%s.com/adfs" % config["lab_name"],
            scope=self.adfs2019_scopes,
            port=8080,
            ))

    @unittest.skipUnless(
        os.getenv("LAB_OBO_CLIENT_SECRET"),
        "Need LAB_OBO_CLIENT_SECRET from https://aka.ms/GetLabSecret?Secret=TodoListServiceV2-OBO")
    @unittest.skipUnless(
        os.getenv("LAB_OBO_CONFIDENTIAL_CLIENT_ID"),
        "Need LAB_OBO_CONFIDENTIAL_CLIENT_ID from https://docs.msidlab.com/flows/onbehalfofflow.html")
    @unittest.skipUnless(
        os.getenv("LAB_OBO_PUBLIC_CLIENT_ID"),
        "Need LAB_OBO_PUBLIC_CLIENT_ID from https://docs.msidlab.com/flows/onbehalfofflow.html")
    def test_acquire_token_obo(self):
        config = self.get_lab_user(usertype="cloud")

        config_cca = {}
        config_cca.update(config)
        config_cca["client_id"] = os.getenv("LAB_OBO_CONFIDENTIAL_CLIENT_ID")
        config_cca["scope"] = ["https://graph.microsoft.com/.default"]
        config_cca["client_secret"] = os.getenv("LAB_OBO_CLIENT_SECRET")

        config_pca = {}
        config_pca.update(config)
        config_pca["client_id"] = os.getenv("LAB_OBO_PUBLIC_CLIENT_ID")
        config_pca["password"] = self.get_lab_user_secret(config_pca["lab_name"])
        config_pca["scope"] = ["api://%s/read" % config_cca["client_id"]]

        self._test_acquire_token_obo(config_pca, config_cca)

    @unittest.skipUnless(
        os.path.exists("tests/sp_obo.pem"),
        "Need a 'tests/sp_obo.pem' private to run OBO for SP test")
    def test_acquire_token_obo_for_sp(self):
        authority = "https://login.windows-ppe.net/f686d426-8d16-42db-81b7-ab578e110ccd"
        with open("tests/sp_obo.pem") as pem:
            client_secret = {
                "private_key": pem.read(),
                "thumbprint": "378938210C976692D7F523B8C4FFBB645D17CE92",
                }
        midtier_app = {
            "authority": authority,
            "client_id": "c84e9c32-0bc9-4a73-af05-9efe9982a322",
            "client_secret": client_secret,
            "scope": ["23d08a1e-1249-4f7c-b5a5-cb11f29b6923/.default"],
            #"username": "OBO-Client-PPE",  # We do NOT attempt locating initial_app by name
            }
        initial_app = {
            "authority": authority,
            "client_id": "9793041b-9078-4942-b1d2-babdc472cc0c",
            "client_secret": client_secret,
            "scope": [midtier_app["client_id"] + "/.default"],
            }
        self._test_acquire_token_obo(initial_app, midtier_app)

    def test_acquire_token_by_client_secret(self):
        # Vastly different than ArlingtonCloudTestCase.test_acquire_token_by_client_secret()
        _app = self.get_lab_app_object(
            publicClient="no", signinAudience="AzureAdMyOrg")
        self._test_acquire_token_by_client_secret(
            client_id=_app["appId"],
            client_secret=self.get_lab_user_secret(
                _app["clientSecret"].split("/")[-1]),
            authority="{}{}.onmicrosoft.com".format(
                _app["authority"], _app["labName"].lower().rstrip(".com")),
            scope=["https://graph.microsoft.com/.default"],
            )

    @unittest.skipUnless(
        os.getenv("LAB_OBO_CLIENT_SECRET"),
        "Need LAB_OBO_CLIENT_SECRET from https://aka.ms/GetLabSecret?Secret=TodoListServiceV2-OBO")
    @unittest.skipUnless(
        os.getenv("LAB_OBO_CONFIDENTIAL_CLIENT_ID"),
        "Need LAB_OBO_CONFIDENTIAL_CLIENT_ID from https://docs.msidlab.com/flows/onbehalfofflow.html")
    def test_confidential_client_acquire_token_by_username_password(self):
        # This approach won't work:
        #       config = self.get_lab_user(usertype="cloud", publicClient="no")
        # so we repurpose the obo confidential app to test ROPC
        config = self.get_lab_user(usertype="cloud")
        config["password"] = self.get_lab_user_secret(config["lab_name"])
        # Swap in the OBO confidential app
        config["client_id"] = os.getenv("LAB_OBO_CONFIDENTIAL_CLIENT_ID")
        config["scope"] = ["https://graph.microsoft.com/.default"]
        config["client_secret"] = os.getenv("LAB_OBO_CLIENT_SECRET")
        self._test_username_password(**config)

    def _build_b2c_authority(self, policy):
        base = "https://msidlabb2c.b2clogin.com/msidlabb2c.onmicrosoft.com"
        return base + "/" + policy  # We do not support base + "?p=" + policy

    def test_b2c_acquire_token_by_auth_code(self):
        """
        When prompted, you can manually login using this account:

            username="b2clocal@msidlabb2c.onmicrosoft.com"
                # This won't work https://msidlab.com/api/user?usertype=b2c
            password="***"  # From https://aka.ms/GetLabSecret?Secret=msidlabb2c
        """
        config = self.get_lab_app_object(azureenvironment="azureb2ccloud")
        self._test_acquire_token_by_auth_code(
            authority=self._build_b2c_authority("B2C_1_SignInPolicy"),
            client_id=config["appId"],
            port=3843,  # Lab defines 4 of them: [3843, 4584, 4843, 60000]
            scope=config["scopes"],
            )

    def test_b2c_acquire_token_by_auth_code_flow(self):
        self._test_acquire_token_by_auth_code_flow(**dict(
            self.get_lab_user(usertype="b2c", b2cprovider="local"),
            authority=self._build_b2c_authority("B2C_1_SignInPolicy"),
            port=3843,  # Lab defines 4 of them: [3843, 4584, 4843, 60000]
            scope=self.get_lab_app_object(azureenvironment="azureb2ccloud")["scopes"],
            ))

    def test_b2c_acquire_token_by_ropc(self):
        config = self.get_lab_app_object(azureenvironment="azureb2ccloud")
        self._test_username_password(
            authority=self._build_b2c_authority("B2C_1_ROPC_Auth"),
            client_id=config["appId"],
            username="b2clocal@msidlabb2c.onmicrosoft.com",
            password=self.get_lab_user_secret("msidlabb2c"),
            scope=config["scopes"],
            )

    def test_b2c_allows_using_client_id_as_scope(self):
        # See also https://learn.microsoft.com/en-us/azure/active-directory-b2c/access-tokens#openid-connect-scopes
        config = self.get_lab_app_object(azureenvironment="azureb2ccloud")
        config["scopes"] = [config["appId"]]
        self._test_username_password(
            authority=self._build_b2c_authority("B2C_1_ROPC_Auth"),
            client_id=config["appId"],
            username="b2clocal@msidlabb2c.onmicrosoft.com",
            password=self.get_lab_user_secret("msidlabb2c"),
            scope=config["scopes"],
            )


class CiamTestCase(LabBasedTestCase):
    # Test cases below show you what scenarios need to be covered for CIAM.
    # Detail test behaviors have already been implemented in preexisting helpers.

    @classmethod
    def setUpClass(cls):
        super(CiamTestCase, cls).setUpClass()
        cls.user = cls.get_lab_user(
            #federationProvider="ciam",  # This line would return ciam2 tenant
            federationProvider="ciamcud", signinAudience="AzureAdMyOrg",  # ciam6
        )
        # FYI: Only single- or multi-tenant CIAM app can have other-than-OIDC
        # delegated permissions on Microsoft Graph.
        cls.app_config = cls.get_lab_app_object(cls.user["client_id"])

    def test_ciam_acquire_token_interactive(self):
        self._test_acquire_token_interactive(
            authority=self.app_config.get("authority"),
            oidc_authority=self.app_config.get("oidc_authority"),
            client_id=self.app_config["appId"],
            scope=self.app_config["scopes"],
            username=self.user["username"],
            lab_name=self.user["lab_name"],
            )

    def test_ciam_acquire_token_for_client(self):
        raw_url = self.app_config["clientSecret"]
        secret_url = urlparse(raw_url)
        if secret_url.query:  # Ciam2 era has a query param Secret=name
            secret_name = parse_qs(secret_url.query)["Secret"][0]
        else:  # Ciam6 era has a URL path that ends with the secret name
            secret_name = secret_url.path.split("/")[-1]
        logger.info('Detected secret name "%s" from "%s"', secret_name, raw_url)
        self._test_acquire_token_by_client_secret(
            client_id=self.app_config["appId"],
            client_secret=self.get_lab_user_secret(secret_name),
            authority=self.app_config.get("authority"),
            oidc_authority=self.app_config.get("oidc_authority"),
            scope=self.app_config["scopes"],  # It shall ends with "/.default"
            )

    def test_ciam_acquire_token_by_ropc(self):
        """CIAM does not officially support ROPC, especially not for external emails.

        We keep this test case for now, because the test data will use a local email.
        """
        # Somehow, this would only work after creating a secret for the test app
        # and enabling "Allow public client flows".
        # Otherwise it would hit AADSTS7000218.
        self._test_username_password(
            authority=self.app_config.get("authority"),
            oidc_authority=self.app_config.get("oidc_authority"),
            client_id=self.app_config["appId"],
            username=self.user["username"],
            password=self.get_lab_user_secret(self.user["lab_name"]),
            scope=self.app_config["scopes"],
            )

    @unittest.skip("""As of Aug 2024, in both ciam2 and ciam6, sign-in fails with
AADSTS500208: The domain is not a valid login domain for the account type.""")
    def test_ciam_device_flow(self):
        self._test_device_flow(
            authority=self.app_config.get("authority"),
            oidc_authority=self.app_config.get("oidc_authority"),
            client_id=self.app_config["appId"],
            scope=self.app_config["scopes"],
            )


class CiamCudTestCase(CiamTestCase):
    @classmethod
    def setUpClass(cls):
        super(CiamCudTestCase, cls).setUpClass()
        cls.app_config["authority"] = None
        cls.app_config["oidc_authority"] = (
            # Derived from https://github.com/AzureAD/microsoft-authentication-library-for-dotnet/blob/4.63.0/tests/Microsoft.Identity.Test.Integration.netcore/HeadlessTests/CiamIntegrationTests.cs#L156
            "https://login.msidlabsciam.com/fe362aec-5d43-45d1-b730-9755e60dc3b9/v2.0")


class WorldWideRegionalEndpointTestCase(LabBasedTestCase):
    region = "westus"
    timeout = 2  # Short timeout makes this test case responsive on non-VM

    def _test_acquire_token_for_client(self, configured_region, expected_region):
        """This is the only grant supported by regional endpoint, for now"""
        self.app = get_lab_app(  # Regional endpoint only supports confidential client

            ## FWIW, the MSAL<1.12 versions could use this to achieve similar result
            #authority="https://westus.login.microsoft.com/microsoft.onmicrosoft.com",
            #validate_authority=False,
            authority="https://login.microsoftonline.com/microsoft.onmicrosoft.com",
            azure_region=configured_region,
            timeout=2,  # Short timeout makes this test case responsive on non-VM
            )
        scopes = ["https://graph.microsoft.com/.default"]

        with patch.object(  # Test the request hit the regional endpoint
                self.app.http_client, "post", return_value=MinimalResponse(
                status_code=400, text='{"error": "mock"}')) as mocked_method:
            self.app.acquire_token_for_client(scopes)
            expected_host = '{}.login.microsoft.com'.format(
                expected_region) if expected_region else 'login.microsoftonline.com'
            mocked_method.assert_called_with(
                'https://{}/{}/oauth2/v2.0/token'.format(
                    expected_host, self.app.authority.tenant),
                params=ANY, data=ANY, headers=ANY)
        result = self.app.acquire_token_for_client(
            scopes,
            params={"AllowEstsRNonMsi": "true"},  # For testing regional endpoint. It will be removed once MSAL Python 1.12+ has been onboard to ESTS-R
            )
        self.assertIn('access_token', result)
        self.assertCacheWorksForApp(result, scopes)

    def test_acquire_token_for_client_should_hit_global_endpoint_by_default(self):
        self._test_acquire_token_for_client(None, None)

    def test_acquire_token_for_client_should_ignore_env_var_region_name_by_default(self):
        os.environ["REGION_NAME"] = "eastus"
        self._test_acquire_token_for_client(None, None)
        del os.environ["REGION_NAME"]

    @patch.dict(os.environ, {"MSAL_FORCE_REGION": "eastus"})
    def test_acquire_token_for_client_should_use_env_var_msal_force_region_by_default(self):
        self._test_acquire_token_for_client(None, "eastus")

    @patch.dict(os.environ, {"MSAL_FORCE_REGION": "eastus"})
    def test_acquire_token_for_client_should_prefer_the_explicit_region(self):
        self._test_acquire_token_for_client("westus", "westus")

    @patch.dict(os.environ, {"MSAL_FORCE_REGION": "eastus"})
    def test_acquire_token_for_client_should_allow_opt_out_env_var_msal_force_region(self):
        self._test_acquire_token_for_client(False, None)

    def test_acquire_token_for_client_should_use_a_specified_region(self):
        self._test_acquire_token_for_client("westus", "westus")

    def test_acquire_token_for_client_should_use_an_env_var_with_short_region_name(self):
        os.environ["REGION_NAME"] = "eastus"
        self._test_acquire_token_for_client(
            msal.ConfidentialClientApplication.ATTEMPT_REGION_DISCOVERY, "eastus")
        del os.environ["REGION_NAME"]

    def test_acquire_token_for_client_should_use_an_env_var_with_long_region_name(self):
        os.environ["REGION_NAME"] = "East Us 2"
        self._test_acquire_token_for_client(
            msal.ConfidentialClientApplication.ATTEMPT_REGION_DISCOVERY, "eastus2")
        del os.environ["REGION_NAME"]

    @unittest.skipUnless(
        os.getenv("LAB_OBO_CLIENT_SECRET"),
        "Need LAB_OBO_CLIENT_SECRET from https://aka.ms/GetLabSecret?Secret=TodoListServiceV2-OBO")
    @unittest.skipUnless(
        os.getenv("LAB_OBO_CONFIDENTIAL_CLIENT_ID"),
        "Need LAB_OBO_CONFIDENTIAL_CLIENT_ID from https://docs.msidlab.com/flows/onbehalfofflow.html")
    @unittest.skipUnless(
        os.getenv("LAB_OBO_PUBLIC_CLIENT_ID"),
        "Need LAB_OBO_PUBLIC_CLIENT_ID from https://docs.msidlab.com/flows/onbehalfofflow.html")
    def test_cca_obo_should_bypass_regional_endpoint_therefore_still_work(self):
        """We test OBO because it is implemented in sub class ConfidentialClientApplication"""
        config = self.get_lab_user(usertype="cloud")

        config_cca = {}
        config_cca.update(config)
        config_cca["client_id"] = os.getenv("LAB_OBO_CONFIDENTIAL_CLIENT_ID")
        config_cca["scope"] = ["https://graph.microsoft.com/.default"]
        config_cca["client_secret"] = os.getenv("LAB_OBO_CLIENT_SECRET")

        config_pca = {}
        config_pca.update(config)
        config_pca["client_id"] = os.getenv("LAB_OBO_PUBLIC_CLIENT_ID")
        config_pca["password"] = self.get_lab_user_secret(config_pca["lab_name"])
        config_pca["scope"] = ["api://%s/read" % config_cca["client_id"]]

        self._test_acquire_token_obo(
            config_pca, config_cca,
            azure_region=self.region,
            http_client=MinimalHttpClient(timeout=self.timeout),
            )

    @unittest.skipUnless(
        os.getenv("LAB_OBO_CLIENT_SECRET"),
        "Need LAB_OBO_CLIENT_SECRET from https://aka.ms/GetLabSecret?Secret=TodoListServiceV2-OBO")
    @unittest.skipUnless(
        os.getenv("LAB_OBO_CONFIDENTIAL_CLIENT_ID"),
        "Need LAB_OBO_CONFIDENTIAL_CLIENT_ID from https://docs.msidlab.com/flows/onbehalfofflow.html")
    def test_cca_ropc_should_bypass_regional_endpoint_therefore_still_work(self):
        """We test ROPC because it is implemented in base class ClientApplication"""
        config = self.get_lab_user(usertype="cloud")
        config["password"] = self.get_lab_user_secret(config["lab_name"])
        # We repurpose the obo confidential app to test ROPC
        # Swap in the OBO confidential app
        config["client_id"] = os.getenv("LAB_OBO_CONFIDENTIAL_CLIENT_ID")
        config["scope"] = ["https://graph.microsoft.com/.default"]
        config["client_secret"] = os.getenv("LAB_OBO_CLIENT_SECRET")
        self._test_username_password(
            azure_region=self.region,
            http_client=MinimalHttpClient(timeout=self.timeout),
            **config)


class ArlingtonCloudTestCase(LabBasedTestCase):
    environment = "azureusgovernment"

    def test_acquire_token_by_ropc(self):
        config = self.get_lab_user(azureenvironment=self.environment)
        config["password"] = self.get_lab_user_secret(config["lab_name"])
        self._test_username_password(**config)

    def test_acquire_token_by_client_secret(self):
        config = self.get_lab_user(usertype="cloud", azureenvironment=self.environment, publicClient="no")
        config["client_secret"] = self.get_lab_user_secret("ARLMSIDLAB1-IDLASBS-App-CC-Secret")
        self._test_acquire_token_by_client_secret(**config)

    def test_acquire_token_obo(self):
        config_cca = self.get_lab_user(
            usertype="cloud", azureenvironment=self.environment, publicClient="no")
        config_cca["scope"] = ["https://graph.microsoft.us/.default"]
        config_cca["client_secret"] = self.get_lab_user_secret("ARLMSIDLAB1-IDLASBS-App-CC-Secret")

        config_pca = self.get_lab_user(usertype="cloud", azureenvironment=self.environment, publicClient="yes")
        obo_app_object = self.get_lab_app_object(
            usertype="cloud", azureenvironment=self.environment, publicClient="no")
        config_pca["password"] = self.get_lab_user_secret(config_pca["lab_name"])
        config_pca["scope"] = ["{app_uri}/files.read".format(app_uri=obo_app_object.get("identifierUris"))]

        self._test_acquire_token_obo(config_pca, config_cca)

    def test_acquire_token_device_flow(self):
        config = self.get_lab_user(usertype="cloud", azureenvironment=self.environment, publicClient="yes")
        config["scope"] = ["user.read"]
        self._test_device_flow(**config)

    def test_acquire_token_silent_with_an_empty_cache_should_return_none(self):
        config = self.get_lab_user(
            usertype="cloud", azureenvironment=self.environment, publicClient="no")
        app = msal.ConfidentialClientApplication(
            config['client_id'], authority=config['authority'],
            http_client=MinimalHttpClient())
        result = app.acquire_token_silent(scopes=config['scope'], account=None)
        self.assertEqual(result, None)
        # Note: An alias in this region is no longer accepting HTTPS traffic.
        #       If this test case passes without exception,
        #       it means MSAL Python is not affected by that.


@unittest.skipUnless(_PYMSALRUNTIME_INSTALLED, "AT POP feature is only supported by using broker")
class PopTestCase(LabBasedTestCase):
    def test_at_pop_should_contain_pop_scheme_content(self):
        auth_scheme = msal.PopAuthScheme(
            http_method=msal.PopAuthScheme.HTTP_GET,
            url="https://www.Contoso.com/Path1/Path2?queryParam1=a&queryParam2=b",
            nonce="placeholder",
            )
        result = self._test_acquire_token_interactive(
            # Lab test users tend to get kicked out from WAM, we use local user to test
            client_id=_AZURE_CLI,
            authority="https://login.microsoftonline.com/organizations",
            scope=["https://management.azure.com/.default"],
            auth_scheme=auth_scheme,
            )   # It also tests assertCacheWorksForUser()
        self.assertEqual(result["token_source"], "broker", "POP is only supported by broker")
        self.assertEqual(result["token_type"], "pop")
        payload = json.loads(decode_part(result["access_token"].split(".")[1]))
        logger.debug("AT POP payload = %s", json.dumps(payload, indent=2))
        self.assertEqual(payload["m"], auth_scheme._http_method)
        self.assertEqual(payload["u"], auth_scheme._url.netloc)
        self.assertEqual(payload["p"], auth_scheme._url.path)
        self.assertEqual(payload["nonce"], auth_scheme._nonce)

    # TODO: Remove this, as ROPC support is removed by Broker-on-Win
    def test_at_pop_via_testingsts_service(self):
        """Based on https://testingsts.azurewebsites.net/ServerNonce"""
        self.skipTest("ROPC support is removed by Broker-on-Win")
        auth_scheme = msal.PopAuthScheme(
            http_method="POST",
            url="https://www.Contoso.com/Path1/Path2?queryParam1=a&queryParam2=b",
            nonce=requests.get(
                # TODO: Could use ".../missing" and then parse its WWW-Authenticate header
                "https://testingsts.azurewebsites.net/servernonce/get").text,
            )
        config = self.get_lab_user(usertype="cloud")
        config["password"] = self.get_lab_user_secret(config["lab_name"])
        result = self._test_username_password(auth_scheme=auth_scheme, **config)
        self.assertEqual(result["token_type"], "pop")
        shr = result["access_token"]
        payload = json.loads(decode_part(result["access_token"].split(".")[1]))
        logger.debug("AT POP payload = %s", json.dumps(payload, indent=2))
        self.assertEqual(payload["m"], auth_scheme._http_method)
        self.assertEqual(payload["u"], auth_scheme._url.netloc)
        self.assertEqual(payload["p"], auth_scheme._url.path)
        self.assertEqual(payload["nonce"], auth_scheme._nonce)

        validation = requests.post(
            # TODO: This endpoint does not seem to validate the url
            "https://testingsts.azurewebsites.net/servernonce/validateshr",
            data={"SHR": shr},
            )
        self.assertEqual(validation.status_code, 200)

    def test_at_pop_calling_pattern(self):
        # The calling pattern was described here:
        # https://identitydivision.visualstudio.com/DevEx/_git/AuthLibrariesApiReview?path=/PoPTokensProtocol/PoP_API_In_MSAL.md&_a=preview&anchor=proposal-2---optional-isproofofposessionsupportedbyclient-helper-(accepted)

        # It is supposed to call app.is_pop_supported() first,
        # and then fallback to bearer token code path.
        # We skip it here because this test case has not yet initialize self.app
        # assert self.app.is_pop_supported()

        api_endpoint = "https://20.190.132.47/beta/me"
        verify = True  # Hopefully this will make CodeQL happy
        if verify:
            self.skipTest("""
            The api_endpoint is for test only and has no proper SSL certificate,
            so you would have to disable SSL certificate checks and run this test case manually.
            We tried suppressing the CodeQL warning by adding this in the proper places
                @suppress py/bandit/requests-ssl-verify-disabled
            but it did not work.
            """)
        # @suppress py/bandit/requests-ssl-verify-disabled
        resp = requests.get(api_endpoint, verify=verify)  # CodeQL [SM03157]
        self.assertEqual(resp.status_code, 401, "Initial call should end with an http 401 error")
        result = self._get_shr_pop(**dict(
            self.get_lab_user(usertype="cloud"),  # This is generally not the current laptop's default AAD account
            scope=["https://graph.microsoft.com/.default"],
            auth_scheme=msal.PopAuthScheme(
                http_method=msal.PopAuthScheme.HTTP_GET,
                url=api_endpoint,
                nonce=self._extract_pop_nonce(resp.headers.get("WWW-Authenticate")),
                ),
            ))
        resp = requests.get(
            api_endpoint,
            # CodeQL [SM03157]
            verify=verify,  # @suppress py/bandit/requests-ssl-verify-disabled
            headers={
            "Authorization": "pop {}".format(result["access_token"]),
            })
        self.assertEqual(resp.status_code, 200, "POP resource should be accessible")

    def _extract_pop_nonce(self, www_authenticate):
        # This is a hack for testing purpose only. Do not use this in prod.
        # FYI: There is a www-authenticate package but it falters when encountering realm=""
        import re
        found = re.search(r'nonce="(.+?)"', www_authenticate)
        if found:
            return found.group(1)

    def _get_shr_pop(
            self, client_id=None, authority=None, scope=None, auth_scheme=None,
            **kwargs):
        result = self._test_acquire_token_interactive(
            # Lab test users tend to get kicked out from WAM, we use local user to test
            client_id=client_id,
            authority=authority,
            scope=scope,
            auth_scheme=auth_scheme,
            **kwargs)  # It also tests assertCacheWorksForUser()
        self.assertEqual(result["token_source"], "broker", "POP is only supported by broker")
        self.assertEqual(result["token_type"], "pop")
        payload = json.loads(decode_part(result["access_token"].split(".")[1]))
        logger.debug("AT POP payload = %s", json.dumps(payload, indent=2))
        self.assertEqual(payload["m"], auth_scheme._http_method)
        self.assertEqual(payload["u"], auth_scheme._url.netloc)
        self.assertEqual(payload["p"], auth_scheme._url.path)
        self.assertEqual(payload["nonce"], auth_scheme._nonce)
        return result


if __name__ == "__main__":
    unittest.main()
