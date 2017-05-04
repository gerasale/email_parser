
# -*- coding: utf-8 -*-
# -- coding: utf-8 --

import imaplib
import re
import email.header
import email
import config
server = imaplib.IMAP4_SSL('imap.gmail.com')
server.login(config.login, config.password)
server.select()
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
	message = re.sub('b', '', message) # удаляем откуда-то взявшуюся букву b
	return message

for id in ids[0].split():
	subj = make_correct(str(server.fetch(id,'(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')[1][0][1].strip()))
	body = server.fetch('2121','(RFC822)')
	pure_email = body[0][1]
	pure_email = email.message_from_string(str(body))
	print (subj)
	#print (pure_email)

##пытаемся получить тело письма
#id_list = ids[0].split()
#latest_email_id = id_list[-1]
#result, data = server.fetch(latest_email_id, '(RFC822)')
##make_correct('Message %s\n%s\n' % (num, data[0][1]))
#email_message = data [0][1]
#email_message = email.message_from_string(data)
#print (str(email_message['To']))

server.logout()
