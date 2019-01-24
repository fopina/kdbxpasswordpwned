# kdbxpasswordpwned
Check keepass passwords against https://haveibeenpwned.com/Passwords

[![Build Status](https://travis-ci.org/fopina/kdbxpasswordpwned.svg?branch=master)](https://travis-ci.org/fopina/kdbxpasswordpwned)
[![Coverage Status](https://coveralls.io/repos/github/fopina/kdbxpasswordpwned/badge.svg?branch=master)](https://coveralls.io/github/fopina/kdbxpasswordpwned?branch=master)
[![Docker Version](https://images.microbadger.com/badges/version/fopina/kdbxpasswordpwned.svg)](https://microbadger.com/images/fopina/kdbxpasswordpwned)
[![Docker Image](https://images.microbadger.com/badges/image/fopina/kdbxpasswordpwned.svg)](https://microbadger.com/images/fopina/kdbxpasswordpwned)
[![PyPI Version](https://img.shields.io/pypi/v/kdbxpasswordpwned.svg)](https://pypi.python.org/pypi/kdbxpasswordpwned)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/kdbxpasswordpwned.svg)](https://pypi.python.org/pypi/kdbxpasswordpwned)

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
