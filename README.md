# mailpy
UNIX standard mail command aleternative by python, supporting to send UTF-8/HTML/Attachments

# How to use

# Prepare

Please have $HOME/.mailrc


## Basic usage

```
$ echo hoge | mail.py -s "email subject" hoge@hoge.com
```

## Attach file

```
$ echo hoge | mail.py -s "email subject" -a hoge.txt hoge@hoge.com
```

## Send html email

```
$ mai.py -t html -s "Html mail" -r hoge.png < hoge.html
```

Please note that hoge.png is used by the hoge.html


