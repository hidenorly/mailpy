#!/usr/bin/env python
# coding: utf-8
#
# Copyright (C) 2016, 2025 hidenorly
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email import charset
from email import encoders
from email.Utils import formatdate
from os.path import expanduser
import os
from optparse import OptionParser, OptionValueError
import sys
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

charset.add_charset('utf-8', charset.SHORTEST, None, 'utf-8')
cset = 'utf-8'

homeDir = expanduser("~")

def readStdin():
	UTF8Reader = codecs.getreader('utf8')
	sys.stdin = UTF8Reader(sys.stdin)

	buf = ""
	for line in sys.stdin:
		buf = buf + line

	return buf

def loadMailRC():
	mailrc = {'smtp':"", 'port':"", 'useTLS':False, 'from_addr': "", 'userId':"", 'password':""}

	f = open(homeDir + "/.mailrc")
	for line in f:
		line = line.strip()
		posE=line.find('=')
		if line.find('smtp=')!=-1:
			pos = line.find('smtp://')
			pos2 = line.rfind(':')
			if pos2==-1:
				pos2 = len(line)
				mailrc['port'] = 25
			else:
				mailrc['port'] = line[pos2+1:len(line)]
			if pos!=-1:
				mailrc['smtp'] = line[pos+7:pos2]
		elif line.find('smtp-auth-user=')!=-1:
			mailrc['userId'] = line[posE+1:len(line)]
		elif line.find('smtp-auth-password=')!=-1:
			mailrc['password'] = line[posE+1:len(line)]
		elif line.find('from=')!=-1:
			mailrc['from_addr'] = line[posE+1:len(line)]
		elif line.find('set smtp-use-starttls')!=-1:
			mailrc['useTLS'] = True

	f.close

	return mailrc

def create_message(from_addr, to_addrs, cc_addrs, bcc_addrs, subject, body, contentType, attachments, relatedAttachments, encoding):
	related = None
	msg = None
	
	# Create Msg & handle body
	if attachments or relatedAttachments:
		msg = MIMEMultipart()
	if relatedAttachments:
		related = MIMEMultipart('related')
		alt = MIMEMultipart('alternative')
		alt.attach( MIMEText(body, contentType, encoding) )
		related.attach(alt)
	if attachments and not relatedAttachments:
		msg.attach( MIMEText(body, contentType, encoding) )
	if not msg:
		msg = MIMEText(body, contentType, encoding)
	
	# handle header
	msg['Subject'] = Header(subject, encoding)
	msg['From'] = from_addr
	msg['To'] = ", ".join(to_addrs)
	if cc_addrs:
		msg['Cc'] = ", ".join(cc_addrs)
	#if bcc_addrs:
	#	msg['Bcc'] = ", ".join(bcc_addrs)
	msg['Date'] = formatdate(localtime=True)

	# handle attachments
	if relatedAttachments:
		for f in relatedAttachments:
			filename = os.path.basename(f)
			extPos = filename.rfind('.')
			isImage = False
			if extPos != -1:
				ext = filename[extPos+1:len(filename)]
				if ext=='gif' or ext=='png' or ext=='jpg' or ext=='jpeg':
					isImage = True
			if isImage:
				img = MIMEImage(open(f,"rb").read(), ext, name=filename)
				img['Content-ID'] = '<%s>' % filename
				related.attach(img)
			else:
				part = MIMEBase('application', "octet-stream")
				part.set_payload(open(f,"rb").read() )
				encoders.encode_base64(part)
				part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
				part['Content-ID'] = '<%s>' % filename
				related.attach(part)
		msg.attach(related)

	if attachments:
		for f in attachments:
			part = MIMEBase('application', "octet-stream")
			part.set_payload( open(f,"rb").read() )
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
			msg.attach(part)

	return msg


def getAuthenticatedSMTP(smtpHost, smtpPort, userId, password, useTLS):
	s = smtplib.SMTP(smtpHost, smtpPort)
	if useTLS:
		s.ehlo()
		s.starttls()
	if userId and password:
		s.ehlo()
		s.login(userId, password)
	return s

def send(s, from_addr, to_addrs, msg):
    s.sendmail(from_addr, to_addrs, msg.as_string())

def getAttachments(attachments):
	if attachments!=None:
		if isinstance(attachments, list) and len(attachments)==1:
			if attachments[0].find(",")!=-1:
				attachments = attachments[0].split(",")
	return attachments

def email_address_normalizer(addresss):
	if addresss:
		return [address.strip() for address in addresss.split(",")]
	return None

if __name__ == '__main__':
	parser = OptionParser()

	parser.add_option("-f", "--from", action="store", type="string", dest="from_addr", help="Specify From:")
	parser.add_option("-s", "--subject", action="store", type="string", dest="subject", help="Specify Subject:")
	parser.add_option("-c", "--cc", action="store", type="string", dest="sendAsCC", help="Specify Cc:")
	parser.add_option("-b", "--bcc", action="store", type="string", dest="sendAsBCC", help="Specify Bcc:")
	parser.add_option("-a", "--attach", action="append", type="string", dest="attachments", default=None, help="Specify attachment file(,)")
	parser.add_option("-t", "--type", action="store", type="string", dest="contentType", default='plain', help="Specify plain or html")
	parser.add_option("-r", "--relatedAttach", action="append", type="string", dest="relatedAttachments", default=None, help="Specify attachment files for html(,)")

	(options, args) = parser.parse_args()

	if not args:
		parser.error("requires To: as last argument")
		parser.print_help()
		exit()

	to_addrs = email_address_normalizer(args[0])
	mailrc = loadMailRC()

	from_addr = mailrc['from_addr']
	if options.from_addr:
		from_addr = options.from_addr

	body = readStdin()

	attachments = getAttachments( options.attachments )
	relatedAttachments = getAttachments( options.relatedAttachments )
	cc_addrs = email_address_normalizer(options.sendAsCC)
	bcc_addrs = email_address_normalizer(options.sendAsBCC)

	msg = create_message(from_addr, to_addrs, cc_addrs, bcc_addrs, options.subject, body, options.contentType, attachments, relatedAttachments, 'utf-8')  # 'ISO-2022-JP')
	s = getAuthenticatedSMTP(mailrc['smtp'], mailrc['port'], mailrc['userId'], mailrc['password'], mailrc['useTLS'])
	actual_destinations = to_addrs
	if cc_addrs:
		actual_destinations.extend(cc_addrs)
	if bcc_addrs:
		actual_destinations.extend(bcc_addrs)
	send(s, from_addr, actual_destinations, msg)
	s.close()
