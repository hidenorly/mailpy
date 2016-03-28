# mailpy
UNIX standard mail command aleternative by python, supporting to send UTF-8/HTML/Attachments

# How to use

# Prepare

Please have $HOME/.mailrc

## .mailrc example for gmail (with TLS authentification)

```~/.mailrc
set smtp-use-starttls
set nss-config-dir=/etc/ssl/certs
set ssl-verify=ignore
set smtp=smtp://smtp.gmail.com:587
set smtp-auth=login
set smtp-auth-user=hoge.hoge@gmail.com
set smtp-auth-password=hogepassword
set from="hoge.hoge@gmail.com(hoge)"
```

## .mailrc example for smtp without TLS authentification

```~/.mailrc
set smtp=smtp://smtp.gmail.com:25
set smtp-auth=login
set smtp-auth-user=hoge
set smtp-auth-password=hogepassword
set from="hoge.hoge@hoge.com(hoge)"
```

## Basic usage

```
$ echo hoge | mail.py -s "email subject" hoge@hoge.com
$ mail.py -s "email subject" hoge@hoge.com < hoge.txt
```

```hoge.txt
UTF-8で扱っているので日本語もOkです。
```

## Attach file

```
$ echo hoge | mail.py -s "email subject" -a hoge.txt hoge@hoge.com
```

## Send html email

```
$ mail.py -t html -s "Html mail" -r hoge.png < hoge.html
```

Please note that hoge.png is used by the hoge.html and if you sepcify the resources with -r, mail.py will translate the URL; for example, <img src="hoge.png"> --> <img src="cid:hoge.png">
