# Copyright (c) 2015-2025 by Ron Frederick <ronf@timeheart.net> and others.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v2.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-2.0/
#
# This program may also be made available under the following secondary
# licenses when the conditions for such availability set forth in the
# Eclipse Public License v2.0 are satisfied:
#
#    GNU General Public License, Version 2.0, or any later versions of
#    that license
#
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later
#
# Contributors:
#     Ron Frederick - initial implementation, API, and documentation

"""Unit tests for key exchange"""

import asyncio
import inspect
import unittest

from hashlib import sha1

import asyncssh

from asyncssh.crypto import curve25519_available, curve448_available
from asyncssh.crypto import sntrup_available
from asyncssh.crypto import Curve25519DH, Curve448DH, ECDH, PQDH
from asyncssh.kex_dh import MSG_KEXDH_INIT, MSG_KEXDH_REPLY
from asyncssh.kex_dh import MSG_KEX_DH_GEX_REQUEST, MSG_KEX_DH_GEX_GROUP
from asyncssh.kex_dh import MSG_KEX_DH_GEX_INIT, MSG_KEX_DH_GEX_REPLY, _KexDHGex
from asyncssh.kex_dh import MSG_KEX_ECDH_INIT, MSG_KEX_ECDH_REPLY
from asyncssh.kex_dh import MSG_KEXGSS_INIT, MSG_KEXGSS_HOSTKEY
from asyncssh.kex_dh import MSG_KEXGSS_COMPLETE, MSG_KEXGSS_ERROR
from asyncssh.kex_rsa import MSG_KEXRSA_PUBKEY, MSG_KEXRSA_SECRET
from asyncssh.kex_rsa import MSG_KEXRSA_DONE
from asyncssh.gss import GSSClient, GSSServer
from asyncssh.kex import register_kex_alg, get_kex_algs, get_kex
from asyncssh.packet import SSHPacket, Boolean, Byte, MPInt, String
from asyncssh.public_key import decode_ssh_public_key

from .util import asynctest, get_test_key, gss_available, patch_gss
from .util import AsyncTestCase, ConnectionStub


class _KexConnectionStub(ConnectionStub):
    """Connection stub class to test key exchange"""

    def __init__(self, alg, gss, duplicate=0, peer=None, server=False):
        super().__init__(peer, server)

        self._gss = gss
        self._key_waiter = asyncio.Future()

        self._duplicate = duplicate
        self._kex = get_kex(self, alg)

    async def start(self):
        """Start key exchange"""

        await self._kex.start()

    def connection_lost(self, exc):
        """Handle the closing of a connection"""

        raise NotImplementedError

    def enable_gss_kex_auth(self):
        """Ignore request to enable GSS key exchange authentication"""

    async def process_packet(self, data):
        """Process an incoming packet"""

        packet = SSHPacket(data)
        pkttype = packet.get_byte()
        result = self._kex.process_packet(pkttype, None, packet)

        if inspect.isawaitable(result):
            await result

    def get_hash_prefix(self):
        """Return the bytes used in calculating unique connection hashes"""

        # pylint: disable=no-self-use

        return b'prefix'

    def send_newkeys(self, k, h):
        """Handle a request to send a new keys message"""

        self._key_waiter.set_result(self._kex.compute_key(k, h, b'A', h, 128))

    async def get_key(self):
        """Return generated key data"""

        return await self._key_waiter

    def get_gss_context(self):
        """Return the GSS context associated with this connection"""

        return self._gss

    def send_packet(self, pkttype, *args, **kwargs):
        """Duplicate sending packets of a specific type"""

        super().send_packet(pkttype, *args)

        if pkttype == self._duplicate:
            super().send_packet(pkttype, *args, **kwargs)

    async def simulate_dh_init(self, e):
        """Simulate receiving a DH init packet"""

        await self.process_packet(Byte(MSG_KEXDH_INIT) + MPInt(e))

    async def simulate_dh_reply(self, host_key_data, f, sig):
        """Simulate receiving a DH reply packet"""

        await self.process_packet(b''.join((Byte(MSG_KEXDH_REPLY),
                                            String(host_key_data),
                                            MPInt(f), String(sig))))

    async def simulate_dh_gex_group(self, p, g):
        """Simulate receiving a DH GEX group packet"""

        await self.process_packet(Byte(MSG_KEX_DH_GEX_GROUP) +
                                  MPInt(p) + MPInt(g))

    async def simulate_dh_gex_init(self, e):
        """Simulate receiving a DH GEX init packet"""

        await self.process_packet(Byte(MSG_KEX_DH_GEX_INIT) + MPInt(e))

    async def simulate_dh_gex_reply(self, host_key_data, f, sig):
        """Simulate receiving a DH GEX reply packet"""

        await self.process_packet(b''.join((Byte(MSG_KEX_DH_GEX_REPLY),
                                            String(host_key_data),
                                      MPInt(f), String(sig))))

    async def simulate_gss_complete(self, f, sig):
        """Simulate receiving a GSS complete packet"""

        await self.process_packet(b''.join((Byte(MSG_KEXGSS_COMPLETE),
                                            MPInt(f), String(sig),
                                            Boolean(False))))

    async def simulate_ecdh_init(self, client_pub):
        """Simulate receiving an ECDH init packet"""

        await self.process_packet(Byte(MSG_KEX_ECDH_INIT) + String(client_pub))

    async def simulate_ecdh_reply(self, host_key_data, server_pub, sig):
        """Simulate receiving ab ECDH reply packet"""

        await self.process_packet(b''.join((Byte(MSG_KEX_ECDH_REPLY),
                                            String(host_key_data),
                                            String(server_pub), String(sig))))

    async def simulate_rsa_pubkey(self, host_key_data, trans_key_data):
        """Simulate receiving an RSA pubkey packet"""

        await self.process_packet(Byte(MSG_KEXRSA_PUBKEY) +
                                  String(host_key_data) +
                                  String(trans_key_data))

    async def simulate_rsa_secret(self, encrypted_k):
        """Simulate receiving an RSA secret packet"""

        await self.process_packet(Byte(MSG_KEXRSA_SECRET) +
                                  String(encrypted_k))

    async def simulate_rsa_done(self, sig):
        """Simulate receiving an RSA done packet"""

        await self.process_packet(Byte(MSG_KEXRSA_DONE) + String(sig))


class _KexClientStub(_KexConnectionStub):
    """Stub class for client connection"""

    @classmethod
    def make_pair(cls, alg, gss_host=None, duplicate=0):
        """Make a client and server connection pair to test key exchange"""

        client_conn = cls(alg, gss_host, duplicate)
        return client_conn, client_conn.get_peer()

    def __init__(self, alg, gss_host, duplicate):
        server_conn = _KexServerStub(alg, gss_host, duplicate, peer=self)

        if gss_host:
            gss = GSSClient(gss_host, None, 'delegate' in gss_host)
        else:
            gss = None

        super().__init__(alg, gss, duplicate, peer=server_conn)

    def connection_lost(self, exc):
        """Handle the closing of a connection"""

        if exc and not self._key_waiter.done():
            self._key_waiter.set_exception(exc)

        self.close()

    def validate_server_host_key(self, host_key_data):
        """Validate and return the server's host key"""

        # pylint: disable=no-self-use

        return decode_ssh_public_key(host_key_data)


class _KexServerStub(_KexConnectionStub):
    """Stub class for server connection"""

    def __init__(self, alg, gss_host, duplicate, peer):
        gss = GSSServer(gss_host, None) if gss_host else None
        super().__init__(alg, gss, duplicate, peer, True)

        if gss_host and 'no_host_key' in gss_host:
            self._server_host_key = None
        else:
            priv_key = get_test_key('ecdsa-sha2-nistp256')
            self._server_host_key = asyncssh.load_keypairs(priv_key)[0]

    def connection_lost(self, exc):
        """Handle the closing of a connection"""

        if self._peer:
            self._peer.connection_lost(exc)

        self.close()

    def get_server_host_key(self):
        """Return the server host key"""

        return self._server_host_key


@patch_gss
class _TestKex(AsyncTestCase):
    """Unit tests for kex module"""

    async def _check_kex(self, alg, gss_host=None):
        """Unit test key exchange"""

        client_conn, server_conn = _KexClientStub.make_pair(alg, gss_host)

        try:
            await client_conn.start()
            await server_conn.start()

            self.assertEqual((await client_conn.get_key()),
                             (await server_conn.get_key()))
        finally:
            client_conn.close()
            server_conn.close()

    @asynctest
    async def test_key_exchange_algs(self):
        """Unit test key exchange algorithms"""

        for alg in get_kex_algs():
            with self.subTest(alg=alg):
                if alg.startswith(b'gss-'):
                    if gss_available: # pragma: no branch
                        await self._check_kex(alg + b'-mech', '1')
                else:
                    await self._check_kex(alg)

        if gss_available: # pragma: no branch
            for steps in range(4):
                with self.subTest('GSS key exchange', steps=steps):
                    await self._check_kex(b'gss-group1-sha1-mech', str(steps))

            with self.subTest('GSS with credential delegation'):
                await self._check_kex(b'gss-group1-sha1-mech', '1,delegate')

            with self.subTest('GSS with no host key'):
                await self._check_kex(b'gss-group1-sha1-mech', '1,no_host_key')

            with self.subTest('GSS with full host principal'):
                await self._check_kex(b'gss-group1-sha1-mech', 'host/1@TEST')

    @asynctest
    async def test_dh_gex_old(self):
        """Unit test old DH group exchange request"""

        register_kex_alg(b'dh-gex-sha1-1024', _KexDHGex, sha1, (1024,), True)
        register_kex_alg(b'dh-gex-sha1-2048', _KexDHGex, sha1, (2048,), True)

        for size in (b'1024', b'2048'):
            with self.subTest('Old DH group exchange', size=size):
                await self._check_kex(b'dh-gex-sha1-' + size)

    @asynctest
    async def test_dh_gex(self):
        """Unit test old DH group exchange request"""

        register_kex_alg(b'dh-gex-sha1-1024-1536', _KexDHGex, sha1,
                         (1024, 1536), True)
        register_kex_alg(b'dh-gex-sha1-1536-3072', _KexDHGex, sha1,
                         (1536, 3072), True)
        register_kex_alg(b'dh-gex-sha1-2560-2560', _KexDHGex, sha1,
                         (2560, 2560), True)
        register_kex_alg(b'dh-gex-sha1-2560-4096', _KexDHGex, sha1,
                         (2560, 4096), True)
        register_kex_alg(b'dh-gex-sha1-9216-9216', _KexDHGex, sha1,
                         (9216, 9216), True)

        for size in (b'1024-1536', b'1536-3072', b'2560-2560',
                     b'2560-4096', b'9216-9216'):
            with self.subTest('Old DH group exchange', size=size):
                await self._check_kex(b'dh-gex-sha1-' + size)

    @asynctest
    async def test_dh_errors(self):
        """Unit test error conditions in DH key exchange"""

        client_conn, server_conn = \
            _KexClientStub.make_pair(b'diffie-hellman-group14-sha1')

        host_key = server_conn.get_server_host_key()

        with self.subTest('Init sent to client'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.process_packet(Byte(MSG_KEXDH_INIT))

        with self.subTest('Reply sent to server'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.process_packet(Byte(MSG_KEXDH_REPLY))

        with self.subTest('Invalid e value'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_dh_init(0)

        with self.subTest('Invalid f value'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.start()
                await client_conn.simulate_dh_reply(host_key.public_data,
                                                    0, b'')

        with self.subTest('Invalid signature'):
            with self.assertRaises(asyncssh.KeyExchangeFailed):
                await client_conn.start()
                await client_conn.simulate_dh_reply(host_key.public_data,
                                                    2, b'')

        client_conn.close()
        server_conn.close()

    @asynctest
    async def test_dh_gex_errors(self):
        """Unit test error conditions in DH group exchange"""

        client_conn, server_conn = \
            _KexClientStub.make_pair(b'diffie-hellman-group-exchange-sha1')

        with self.subTest('Request sent to client'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.process_packet(Byte(MSG_KEX_DH_GEX_REQUEST))

        with self.subTest('Group sent to server'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_dh_gex_group(1, 2)

        with self.subTest('Init sent to client'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.simulate_dh_gex_init(1)

        with self.subTest('Init sent before group'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_dh_gex_init(1)

        with self.subTest('Reply sent to server'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_dh_gex_reply(b'', 1, b'')

        with self.subTest('Reply sent before group'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.simulate_dh_gex_reply(b'', 1, b'')

        client_conn.close()
        server_conn.close()

    @asynctest
    async def test_dh_gex_multiple_messages(self):
        """Unit test duplicate messages in DH group exchange"""

        for pkttype in (MSG_KEX_DH_GEX_REQUEST, MSG_KEX_DH_GEX_GROUP):
            client_conn, server_conn = _KexClientStub.make_pair(
                b'diffie-hellman-group-exchange-sha1', duplicate=pkttype)

            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.start()
                await client_conn.get_key()

            client_conn.close()
            server_conn.close()

    @unittest.skipUnless(gss_available, 'GSS not available')
    @asynctest
    async def test_gss_errors(self):
        """Unit test error conditions in GSS key exchange"""

        client_conn, server_conn = \
            _KexClientStub.make_pair(b'gss-group1-sha1-mech', '3')

        with self.subTest('Init sent to client'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.process_packet(Byte(MSG_KEXGSS_INIT))

        with self.subTest('Host key sent to server'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.process_packet(Byte(MSG_KEXGSS_HOSTKEY))

        with self.subTest('Host key sent twice to client'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.process_packet(Byte(MSG_KEXGSS_HOSTKEY))
                await client_conn.process_packet(Byte(MSG_KEXGSS_HOSTKEY))

        with self.subTest('Complete sent to server'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.process_packet(Byte(MSG_KEXGSS_COMPLETE))

        with self.subTest('Exchange failed to complete'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.simulate_gss_complete(1, b'succeed')

        with self.subTest('Error sent to server'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.process_packet(Byte(MSG_KEXGSS_ERROR))

        client_conn.close()
        server_conn.close()

        with self.subTest('Signature verification failure'):
            with self.assertRaises(asyncssh.KeyExchangeFailed):
                await self._check_kex(b'gss-group1-sha1-mech',
                                      '0,verify_error')

        with self.subTest('Empty token in init'):
            with self.assertRaises(asyncssh.ProtocolError):
                await self._check_kex(b'gss-group1-sha1-mech', '0,empty_init')

        with self.subTest('Empty token in continue'):
            with self.assertRaises(asyncssh.ProtocolError):
                await self._check_kex(b'gss-group1-sha1-mech',
                                      '1,empty_continue')

        with self.subTest('Token after complete'):
            with self.assertRaises(asyncssh.ProtocolError):
                await self._check_kex(b'gss-group1-sha1-mech',
                                      '0,continue_token')

        for steps in range(2):
            with self.subTest('Token after complete', steps=steps):
                with self.assertRaises(asyncssh.ProtocolError):
                    await self._check_kex(b'gss-group1-sha1-mech',
                                          str(steps) + ',extra_token')

        with self.subTest('Context not secure'):
            with self.assertRaises(asyncssh.ProtocolError):
                await self._check_kex(b'gss-group1-sha1-mech',
                                      '1,no_server_integrity')

        with self.subTest('GSS error'):
            with self.assertRaises(asyncssh.KeyExchangeFailed):
                await self._check_kex(b'gss-group1-sha1-mech', '1,step_error')

        with self.subTest('GSS error with error token'):
            with self.assertRaises(asyncssh.KeyExchangeFailed):
                await self._check_kex(b'gss-group1-sha1-mech',
                                      '1,step_error,errtok')

    @asynctest
    async def test_ecdh_errors(self):
        """Unit test error conditions in ECDH key exchange"""

        client_conn, server_conn = \
            _KexClientStub.make_pair(b'ecdh-sha2-nistp256')

        with self.subTest('Init sent to client'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.simulate_ecdh_init(b'')

        with self.subTest('Invalid client public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_ecdh_init(b'')

        with self.subTest('Reply sent to server'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_ecdh_reply(b'', b'', b'')

        with self.subTest('Invalid server host key'):
            with self.assertRaises(asyncssh.KeyImportError):
                await client_conn.simulate_ecdh_reply(b'', b'', b'')

        with self.subTest('Invalid server public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                host_key = server_conn.get_server_host_key()
                await client_conn.simulate_ecdh_reply(host_key.public_data,
                                                      b'', b'')

        with self.subTest('Invalid signature'):
            with self.assertRaises(asyncssh.KeyExchangeFailed):
                host_key = server_conn.get_server_host_key()
                server_pub = ECDH(b'nistp256').get_public()
                await client_conn.simulate_ecdh_reply(host_key.public_data,
                                                      server_pub, b'')

        client_conn.close()
        server_conn.close()

    @unittest.skipUnless(curve25519_available, 'Curve25519 not available')
    @asynctest
    async def test_curve25519dh_errors(self):
        """Unit test error conditions in Curve25519DH key exchange"""

        client_conn, server_conn = \
            _KexClientStub.make_pair(b'curve25519-sha256')

        with self.subTest('Invalid client public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_ecdh_init(b'')

        with self.subTest('Invalid server public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                host_key = server_conn.get_server_host_key()
                await client_conn.simulate_ecdh_reply(host_key.public_data,
                                                      b'', b'')

        with self.subTest('Invalid peer public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                host_key = server_conn.get_server_host_key()
                server_pub = b'\x01' + 31*b'\x00'
                await client_conn.simulate_ecdh_reply(host_key.public_data,
                                                      server_pub, b'')

        with self.subTest('Invalid signature'):
            with self.assertRaises(asyncssh.KeyExchangeFailed):
                host_key = server_conn.get_server_host_key()
                server_pub = Curve25519DH().get_public()
                await client_conn.simulate_ecdh_reply(host_key.public_data,
                                                      server_pub, b'')

        client_conn.close()
        server_conn.close()

    @unittest.skipUnless(curve448_available, 'Curve448 not available')
    @asynctest
    async def test_curve448dh_errors(self):
        """Unit test error conditions in Curve448DH key exchange"""

        client_conn, server_conn = \
            _KexClientStub.make_pair(b'curve448-sha512')

        with self.subTest('Invalid client public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_ecdh_init(b'')

        with self.subTest('Invalid server public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                host_key = server_conn.get_server_host_key()
                await client_conn.simulate_ecdh_reply(host_key.public_data,
                                                      b'', b'')

        with self.subTest('Invalid signature'):
            with self.assertRaises(asyncssh.KeyExchangeFailed):
                host_key = server_conn.get_server_host_key()
                server_pub = Curve448DH().get_public()
                await client_conn.simulate_ecdh_reply(host_key.public_data,
                                                      server_pub, b'')

        client_conn.close()
        server_conn.close()

    @unittest.skipUnless(sntrup_available, 'SNTRUP761 not available')
    @asynctest
    async def test_sntrup761dh_errors(self):
        """Unit test error conditions in SNTRUP761 key exchange"""

        pqdh = PQDH(b'sntrup761')

        client_conn, server_conn = \
            _KexClientStub.make_pair(b'sntrup761x25519-sha512@openssh.com')

        with self.subTest('Invalid client SNTRUP761 public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_ecdh_init(b'')

        with self.subTest('Invalid client Curve25519 public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                pub = pqdh.pubkey_bytes * b'\0'
                await server_conn.simulate_ecdh_init(pub)

        with self.subTest('Invalid server SNTRUP761 public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                host_key = server_conn.get_server_host_key()
                await client_conn.simulate_ecdh_reply(host_key.public_data,
                                                      b'', b'')

        with self.subTest('Invalid server Curve25519 public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                host_key = server_conn.get_server_host_key()
                ciphertext = pqdh.ciphertext_bytes * b'\0'
                await client_conn.simulate_ecdh_reply(host_key.public_data,
                                                      ciphertext, b'')

        client_conn.close()
        server_conn.close()

    @asynctest
    async def test_rsa_errors(self):
        """Unit test error conditions in RSA key exchange"""

        client_conn, server_conn = \
            _KexClientStub.make_pair(b'rsa2048-sha256')

        with self.subTest('Pubkey sent to server'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_rsa_pubkey(b'', b'')

        with self.subTest('Secret sent to client'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.simulate_rsa_secret(b'')

        with self.subTest('Done sent to server'):
            with self.assertRaises(asyncssh.ProtocolError):
                await server_conn.simulate_rsa_done(b'')

        with self.subTest('Invalid transient public key'):
            with self.assertRaises(asyncssh.ProtocolError):
                await client_conn.simulate_rsa_pubkey(b'', b'')

        with self.subTest('Invalid encrypted secret'):
            with self.assertRaises(asyncssh.KeyExchangeFailed):
                await server_conn.start()
                await server_conn.simulate_rsa_secret(b'')

        with self.subTest('Invalid signature'):
            with self.assertRaises(asyncssh.KeyExchangeFailed):
                host_key = server_conn.get_server_host_key()
                trans_key = get_test_key('ssh-rsa', 2048)
                await client_conn.simulate_rsa_pubkey(host_key.public_data,
                                                      trans_key.public_data)
                await client_conn.simulate_rsa_done(b'')

        client_conn.close()
        server_conn.close()
