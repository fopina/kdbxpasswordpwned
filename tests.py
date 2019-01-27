#!/usr/bin/env python

import unittest
import kdbxpasswordpwned
import mock
from contextlib import contextmanager
import sys
import os
import construct
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


class TestKPP(unittest.TestCase):
    def test_usage(self):
        with _capture_output() as fout:
            self.assertRaisesRegexp(SystemExit, '2', kdbxpasswordpwned.main)
        try:
            self.assertEqual(
                fout[1].getvalue(),
                '''\
usage: tests.py [-h] [-k KEYFILE] [-u] [-p] kdbx
tests.py: error: too few arguments
'''
            )
        except AssertionError:
            # check py3 argparse output
            self.assertEqual(
                fout[1].getvalue(),
                '''\
usage: tests.py [-h] [-k KEYFILE] [-u] [-p] kdbx
tests.py: error: the following arguments are required: kdbx
'''
            )

    @mock.patch('requests.get')
    def test_check_hash(self, req_mock):
        # password sha1: 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
        req_mock.return_value = mock.MagicMock(content=b'FF:10')
        self.assertEqual(
            kdbxpasswordpwned.check_hash('password'),
            0
        )
        req_mock.assert_called_once_with('https://api.pwnedpasswords.com/range/5BAA6')
        req_mock.reset_mock()

        req_mock.return_value = mock.MagicMock(
            content=b'''
FF:10
1E4C9B93F3F0682250B6CF8331B7EE68FD8:90
'''
            )
        self.assertEqual(
            kdbxpasswordpwned.check_hash('password'),
            90
        )
        req_mock.assert_called_once_with('https://api.pwnedpasswords.com/range/5BAA6')

    @mock.patch('getpass.getpass')
    def test_wrong_password(self, gp_mock):
        gp_mock.return_value = 'wrong'
        self.assertRaisesRegexp(
            construct.ChecksumError,
            "wrong checksum, read '.+?', computed '.+?'",
            kdbxpasswordpwned.main,
            [_asset('sample.kdbx')]
        )

    @mock.patch('getpass.getpass')
    @mock.patch('kdbxpasswordpwned.check_hash')
    def test_run(self, ch_mock, gp_mock):
        gp_mock.return_value = 'reallysafeone'
        ch_mock.return_value = 3
        with _capture_output() as fout:
            kdbxpasswordpwned.main([
                _asset('sample.kdbx')
            ])
        self.assertEqual(
            fout[0].getvalue(),
            '''\
Password for title1 seen 3 times before
Password for title2 seen 3 times before
'''
        )
        ch_mock.assert_has_calls([
            mock.call('testit'),
            mock.call('blabla')
        ])

    @mock.patch('getpass.getpass')
    @mock.patch('kdbxpasswordpwned.check_hash')
    def test_run_show_user_and_password(self, ch_mock, gp_mock):
        gp_mock.return_value = 'reallysafeone'
        ch_mock.return_value = 2
        with _capture_output() as fout:
            kdbxpasswordpwned.main([
                _asset('sample.kdbx'),
                '-up'
            ])
        self.assertEqual(
            fout[0].getvalue(),
            '''\
Password for title1 seen 2 times before - testuser - testit
Password for title2 seen 2 times before - None - blabla
'''
        )
        ch_mock.assert_has_calls([
            mock.call('testit'),
            mock.call('blabla')
        ])

    @mock.patch('getpass.getpass')
    def test_run_keyfile_missing(self, gp_mock):
        gp_mock.return_value = 'reallysafeone'
        self.assertRaisesRegexp(
            construct.ChecksumError,
            "wrong checksum, read '.+?', computed '.+?'",
            kdbxpasswordpwned.main,
            [_asset('sample_with_key.kdbx')]
        )

    @mock.patch('getpass.getpass')
    @mock.patch('kdbxpasswordpwned.check_hash')
    def test_run_keyfile(self, ch_mock, gp_mock):
        gp_mock.return_value = 'reallysafeone'
        ch_mock.return_value = 0
        with _capture_output() as fout:
            kdbxpasswordpwned.main([
                _asset('sample_with_key.kdbx'),
                '-k', _asset('sample.key'),
            ])
        self.assertEqual(fout[0].getvalue(), '')
        ch_mock.assert_has_calls([
            mock.call('testit'),
            mock.call('blabla')
        ])


def _asset(name):
    return os.path.join(
        os.path.dirname(__file__),
        'test_assets',
        name
    )


@contextmanager
def _capture_output():
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = StringIO(), StringIO()
    try:
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


if __name__ == '__main__':
    unittest.main()
