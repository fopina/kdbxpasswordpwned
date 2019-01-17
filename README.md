# kdbxpasswordpwned
Check keepass passwords against https://haveibeenpwned.com/Passwords

### Usage

```bash
$ ./kdbxpasswordpwned.py /path/to/file.kdbx
Password:
Password for asd (HKlue477ZHBV/JaLQj/1QQ==) seen 1151 times before
```

Or the docker image

```
```bash
$ docker run --rm -ti -v /path/to/file.kdbx:/tmp.kdbx fopina/kdbxpasswordpwned /tmp.kdbx
Password:
Password for asd (HKlue477ZHBV/JaLQj/1QQ==) seen 1151 times before
```