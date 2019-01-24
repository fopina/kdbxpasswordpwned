# kdbxpasswordpwned
Check keepass passwords against https://haveibeenpwned.com/Passwords

[![Build Status](https://travis-ci.org/fopina/kdbxpasswordpwned.svg?branch=master)](https://travis-ci.org/fopina/kdbxpasswordpwned)
[![Coverage Status](https://coveralls.io/repos/github/fopina/kdbxpasswordpwned/badge.svg?branch=master)](https://coveralls.io/github/fopina/kdbxpasswordpwned?branch=master)
[![](https://images.microbadger.com/badges/version/fopina/kdbxpasswordpwned.svg)](https://microbadger.com/images/fopina/kdbxpasswordpwned)
[![](https://images.microbadger.com/badges/image/fopina/kdbxpasswordpwned.svg)](https://microbadger.com/images/fopina/kdbxpasswordpwned)

### Usage

```bash
$ ./kdbxpasswordpwned.py -h
usage: kdbxpasswordpwned.py [-h] [-u] [-p] kdbx

positional arguments:
  kdbx                 keepass file

optional arguments:
  -h, --help           show this help message and exit
  -u, --show-user      show username for found entries
  -p, --show-password  show password for found entries (high shoulders?)
```

```bash
$ ./kdbxpasswordpwned.py /path/to/file.kdbx
Password:
Password for title1 (HKlue477ZHBV/JaLQj/1QQ==) seen 1151 times before
Password for title2 (GUx7/Ho/YWc41r1sco5/ZA==) seen 61164 times before
```

Or the docker image

```bash
$ docker run --rm -ti -v /path/to/file.kdbx:/tmp.kdbx:ro fopina/kdbxpasswordpwned -up /tmp.kdbx
Password for title1 (HKlue477ZHBV/JaLQj/1QQ==) seen 1151 times before - testuser - testit
Password for title2 (GUx7/Ho/YWc41r1sco5/ZA==) seen 61164 times before - None - blabla
```
