# kdbxpasswordpwned
Check keepass passwords against https://haveibeenpwned.com/Passwords

[![Build Status](https://travis-ci.org/fopina/kdbxpasswordpwned.svg?branch=master)](https://travis-ci.org/fopina/kdbxpasswordpwned)
[![Coverage Status](https://coveralls.io/repos/github/fopina/kdbxpasswordpwned/badge.svg?branch=master)](https://coveralls.io/github/fopina/kdbxpasswordpwned?branch=master)
[![Docker Version](https://images.microbadger.com/badges/version/fopina/kdbxpasswordpwned.svg)](https://microbadger.com/images/fopina/kdbxpasswordpwned)
[![Docker Image](https://images.microbadger.com/badges/image/fopina/kdbxpasswordpwned.svg)](https://microbadger.com/images/fopina/kdbxpasswordpwned)
[![PyPI Version](https://img.shields.io/pypi/v/kdbxpasswordpwned.svg)](https://pypi.python.org/pypi/kdbxpasswordpwned)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/kdbxpasswordpwned.svg)](https://pypi.python.org/pypi/kdbxpasswordpwned)

### Disclosure

Even if Troy Hunt's API does provide some sense of privacy (as we don't share the password nor even the full SHA1), always review the tools you use with your KeePass files (such as this script which is small and you can easily see the password is not sent anywhere except HIBP API). I have reviewed libkeepass code (0.3.0, pinned in requirements) which is also small, and, as PyPI does not allow replacing existing versions, it is safe.

Also be sure to install tools you trust from places you trust or you might end up installing some shady version such as [this fork](https://github.com/fopina/kdbxpasswordpwned/compare/master...SlivTaMere:bea0f5c) which sends the full password (not the hash) to a different endpoint.

### Usage

Install using `pip`

```bash
$ pip install kdbxpasswordpwned
Collecting kdbxpasswordpwned
Successfully installed kdbxpasswordpwned-0.3
```
And use the CLI

```bash
$ kdbxpasswordpwned -h
usage: kdbxpasswordpwned [-h] [-k KEYFILE] [-u] [-p] kdbx

positional arguments:
  kdbx                  keepass file

optional arguments:
  -h, --help            show this help message and exit
  -k KEYFILE, --keyfile KEYFILE
                        Keyfile if needed
  -u, --show-user       show username for found entries
  -p, --show-password   show password for found entries (high shoulders?)
```

```bash
$ kdbxpasswordpwned /path/to/test_assets/sample.kdbx
Password:
Password for title1 (FEiAje5y9FQmdVCSFDuSRA==) seen 1151 times before
Password for title2 (c3NVlIIN/pPhrM9Pk4Ow+Q==) seen 61164 times before
```

Or simply use the docker image

```bash
$ docker run --rm -ti \
             -v /path/to/test_assets/sample_with_key.kdbx:/tmp.kdbx:ro \
             -v /path/to/test_assets/sample.key:/tmp.key:ro \
             fopina/kdbxpasswordpwned -upk /tmp.key /tmp.kdbx
Password for title1 (FEiAje5y9FQmdVCSFDuSRA==) seen 1151 times before - testuser - testit
Password for title2 (c3NVlIIN/pPhrM9Pk4Ow+Q==) seen 61164 times before - None - blabla
```
