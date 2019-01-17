#!/usr/bin/env python

import libkeepass
import requests
import hashlib
import argparse
import getpass


def build_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('kdbx', type=str,
                        help='keepass file')
    parser.add_argument('-u', '--show-user', action='store_true',
                        help='show username for found entries')
    parser.add_argument('-p', '--show-password', action='store_true',
                        help='show password for found entries (high shoulders?)')
    return parser


def check_hash(password):
    h = hashlib.sha1(password).hexdigest().upper()
    hh = h[5:]
    for l in requests.get('https://api.pwnedpasswords.com/range/' + h[:5]).content.splitlines():
        ll = l.split(':')
        if hh == ll[0]:
            return int(ll[1])
    return 0


def main():
    args = build_parser().parse_args()

    with libkeepass.open(args.kdbx, password=getpass.getpass(), mode='rb') as kdb:
        for entry in kdb.obj_root.findall('.//Group/Entry'):
            uuid = entry.find('./UUID').text
            kv = {string.find('./Key').text: string.find('./Value').text for string in entry.findall('./String')}
            if not kv['Password']:
                continue
            r = check_hash(kv['Password'])
            if r > 0:
                m = 'Password for %s (%s) seen %d times before' % (kv['Title'], uuid, r)
                if args.show_user:
                    m += ' - %s' % kv.get('UserName', '(none)')
                if args.show_password:
                    m += ' - %s' % kv['Password']
                print(m)


if __name__ == '__main__':
    main()
