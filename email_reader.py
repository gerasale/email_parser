
# -*- coding: utf-8 -*-
# -- coding: utf-8 --

import imaplib
import re
import email.header
import email
import config
from email.parser import HeaderParser
#from BeautifulSoup import BeautifulSoup 
from bs4 import BeautifulSoup
server = imaplib.IMAP4_SSL('imap.gmail.com')
server.login(config.login, config.password)
server.select('inbox')
result, ids = server.search(None, 'FLAGGED')

print ('New emails with your email in TO is %d' % len(ids[0].split()))

def make_correct (message):
	def decode_mime_words(s): #хрен его знает, как рабоботает эта функция
		return ''.join(word.decode(encoding or 'utf8') if isinstance(word, bytes) else word for word, encoding in email.header.decode_header(s))
	message = decode_mime_words(re.sub(r'\\n|\\r', '', message)) #  декод MIME и удаление символов переноса строки
	message = re.sub(r'\u20bd', 'Р', message) #заменяем знак рубля на "Р"
	message = re.sub(r'\xab', '"', message) #заменяем открывающие кавычки елочки
	message = re.sub(r'\xbb', '"', message) #заменяем закрывающие кавычки елочки
	message = re.sub(r'\s+', ' ', message) # удаляем двойные пробелы, заменяем на одинарные
	message = re.sub(r'^b', '', message) # удаляем откуда-то взявшуюся букву b
	return message

for i in ids[0].split():
	#typ, data = server.fetch(i, '(RFC822)')

	
	#data = server.fetch(i, '(BODY.PEEK[HEADER.FIELDS (Date To Cc From Subject X-Priority Importance Priority Content-Type)] RFC822.SIZE)')	
	data = server.fetch(i, '(RFC822.TEXT)')
	header_data = data[1][0][1]
	parser = HeaderParser()
	msg = parser.parsestr(str(header_data))

	soup = BeautifulSoup(''.join(msg), 'lxml')

	print (soup.prettify())

	# for response_part in data:
	# 	if isinstance(response_part, tuple):
	# 		msg = email.message_from_string(str(response_part[1]))
	# 		email_subject = msg['(BODY[HEADER.FIELDS (SUBJECT FROM)])']
	# 		email_from = msg['FROM']
	# 		print ('From : ' + str(email_from) + '\n')
	# 		print ('Subject : ' + str(email_subject) + '\n')

	#subj = make_correct(str(server.fetch(id,'(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')[1][0][1].strip()))
	#typ, body = server.fetch(id,'(RFC822)')
	#pure_email = body[0][1]
	#msg = email.message_from_string(str(body[0][1]))
	#email_from = msg['to']
	#print (subj)
	#print (email_from)

#typ, data = mail.fetch(i, '(RFC822)' )
#msg = email.message_from_string(response_part[1])

##пытаемся получить тело письма
#id_list = ids[0].split()
#latest_email_id = id_list[-1]
#result, data = server.fetch(latest_email_id, '(RFC822)')
##make_correct('Message %s\n%s\n' % (num, data[0][1]))
#email_message = data [0][1]
#email_message = email.message_from_string(data)
#print (str(email_message['To']))

server.logout()
