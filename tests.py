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
            "wrong checksum, read b{0,1}'.+?', computed b{0,1}'.+?'",
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
            "wrong checksum, read b{0,1}'.+?', computed b{0,1}'.+?'",
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

    @mock.patch('getpass.getpass')
    @mock.patch('kdbxpasswordpwned.check_hash')
    def test_issue_4(self, ch_mock, gp_mock):
        '''
        https://github.com/fopina/kdbxpasswordpwned/issues/4
        argon format support added by moving
        from libkeepass to pykeepass
        '''
        gp_mock.return_value = '123456'
        ch_mock.return_value = 0
        with _capture_output() as fout:
            kdbxpasswordpwned.main([
                _asset('issue_4.kdbx'),
            ])
        self.assertEqual(fout[0].getvalue(), '')
        ch_mock.assert_not_called()

    @mock.patch('requests.get')
    def test_issue_3(self, req_mock):
        '''
        https://github.com/fopina/kdbxpasswordpwned/issues/3
        issue_3.kdbx takes seconds to load, so importing the
        actual issue directly to the test
        '''
        _val = u'\xc7\xf6\xf6\xb5\xe6\xaf\xe1\xe2\xb4\xb2\xe5\xaf\xd5\xb7\xaf\xa3\xa1\xcf\xff\xcb\xdb\xa7\xd2\xf7\xb5\xb8\xab\xfc\xbd\xd7\xb7\xe8\xfb\xfa\xc9\xa6\xe5\xe2\xb8\xf8\xf1\xdb\xa4\xfc\xbc\xd4\xba\xd1\xa4\xde\xa4\xd7\xc7\xaa\xb4\xc5\xc4\xe7\xce\xe9\xe6\xd2\xcd\xd4\xeb\xd7\xb0\xef\xa5\xba\xbb\xbf\xac\xf4\xca\xf3\xb2\xd7\xc1\xe9\xeb\xf4\xb9\xb5\xd6\xf2\xd3\xf6\xca\xd2\xa7\xd5\xeb\xbf\xda\xc1\xca\xc4\xac\xd2\xe4\xd9\xbd\xed\xa5\xdd\xb2\xcb\xff\xd6\xe5\xd8\xa8\xda\xeb\xc5\xcd\xd5\xf9\xf9\xbf\xe0\xce\xaf\xdd\xb3\xfc\xd8\xb3\xda\xc0\xd1\xd1\xb9\xd9\xc9\xb7\xe6\xfe\xc0\xc5\xb3\xf7\xd8\xa3\xe2\xd6\xc4\xda\xf4\xc0\xea\xdf\xe0\xc0\xc3\xfb\xeb\xc0\xec\xb5\xc5\xbf\xfa\xec\xd5\xe5\xeb\xe7\xfc\xda\xe3\xfc\xe6\xdb\xc6\xb1\xf8\xa4\xf2\xed\xf3\xc2\xb5\xb5\xe0\xb3\xd0\xf4\xf6\xa6\xb3\xa1\xcd\xd9\xa1\xd5\xcb\xa6\xef\xa3\xbb\xbf\xea\xd5\xf3\xdc\xfe\xc4\xa2\xc8\xaa\xc9\xd6\xd0\xc3\xdb\xc0\xa7\xd3\xef\xce\xf7\xcc\xa7\xd2\xbb\xd9\xea\xf2\xb3\xab\xd5\xe4\xfb\xd3\xcd\xda\xab\xe2\xdd\xea\xda\xd1\xa8\xfe\xec\xba\xcb\xe7\xd3\xce\xa1\xaf\xdf\xed'
        kdbxpasswordpwned.check_hash(_val)


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
