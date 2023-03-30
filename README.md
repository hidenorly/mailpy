# mailpy

UNIX standard mail command aleternative by python, supporting to send UTF-8/HTML/Attachments

# How to use

## Prepare

Please have $HOME/.mailrc

### .mailrc example for gmail (with TLS authentification)

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

Note that you need to enable per-application password authentication if you want to use gmail recently.


### .mailrc example for smtp without TLS authentification

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
$ python2 mail.py -s "email subject" hoge@hoge.com < hoge.txt
```

```
$ echo hoge | mail.py -s "email subject" hoge@hoge.com
$ python3 mailpy3.py -s "email subject" hoge@hoge.com < hoge.txt
```


```hoge.txt
UTF-8で扱っているので日本語もOkです。
```

## Attach file

```
$ echo hoge | python2 mail.py -s "email subject" -a hoge.txt hoge@hoge.com
```

```
$ echo hoge | python3 mailpy3.py -s "email subject" -a hoge.txt hoge@hoge.com
```

## Send html email

```
$ python2 mail.py -t html -s "Html mail" -r hoge.png < hoge.html
```

```
$ python3 mailpy3.py -t html -s "Html mail" -r hoge.png < hoge.html
```

Please note that hoge.png is used by the hoge.html and if you sepcify the resources with -r, mail.py will translate the URL; for example, ```<img src="hoge.png"> --> <img src="cid:hoge.png">```
