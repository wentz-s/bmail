#!/usr/bin/python
import xml.etree.ElementTree as e
import smtplib
import email
import imaplib
import poplib
import string

def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
            elif maintype == 'text':
                return email_message_instance.get_payload()


tree = e.parse('config.xml')
root = tree.getroot()
#XML parsing
for a in root.iter('server_smtp'):
    server = a.text
for y in root.iter('server_receive_imap'):
    server_receive_imap = y.text
for z in root.iter('server_receive_pop'):
    server_receive_pop = z.text
for b in root.iter('protocol'):
    protocol = b.text
for c in root.iter('login'):
    login = c.text
for d in root.iter('password'):
    password = d.text
for h in root.iter('folder'):
    folder = h.text
for h in root.iter('smtp_port'):
    smtp_port = int(h.text)

#SMTP for sending mails
print "What do you want?\n1: Send a mail\n2: Read your mail with IMAP\n3: Read ALL your mails with pop3"
choice = input("Choice: ");
if choice == 1:
    smtp = smtplib.SMTP(server, smtp_port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(login, password)
    msg = input("Message: ")
    dest = input("To: ")
    smtp.sendmail(login, dest, msg)
elif choice == 3:
    mail = poplib.POP3_SSL(server_receive_pop)
    mail.user(login)
    mail.pass_(password)
    numMessage = len(mail.list()[1])
    for i in reversed(range(numMessage)):
        msg = mail.retr(i + 1)
        strmail = string.join(msg[1], "\n")
        themail = email.message_from_string(strmail)
        print themail["From"]
        print themail["Subject"]
        print themail["To"]
        print themail["Date"]
        print get_first_text_block(themail)
        print "\n"
    mail.quit()
elif choice == 2:
    mail = imaplib.IMAP4_SSL(server_receive_imap) #fichier de config
    mail.login(login, password) #fichier conf
    mail.list()
    mail.select("inbox")
    nb_mail = len(mail.search(None, "ALL")[1][0].split())
    nb_mail_neg = -1 * nb_mail
    print nb_mail
    nb_mail_neg = nb_mail_neg - 1;
    for i in range(-1, nb_mail_neg, -1):
        result, data = mail.uid('search', None, "ALL")
        latest_email_uid = data[0].split()[i]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)

        numero_chrono = i * -1
        print numero_chrono
        print email_message['Delivered-To']
        print email.utils.parseaddr(email_message['From'])
        print email_message['Subject']


    choice = input("What do you want?:\n1: Read an Email\n2:Delete a Email ")
    if choice == 1:
        choice = input("Enter the number of the mail: ")

        choice = choice * -1
        result, data = mail.uid('search', None, "ALL")
        latest_email_uid = data[0].split()[choice]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        print email_message['Delivered-To']
        print email.utils.parseaddr(email_message['From'])
        print email_message['Subject']
        print get_first_text_block(email_message)


    elif choice == 2:
        choice = input("Enter the number of the mail: ")

        choice = -1 * choice
        result, data = mail.search(None, "ALL");
        latest_email_uid = data[0].split()[choice]
        mail.store(latest_email_uid, '+FLAGS', '\\Deleted')
        mail.expunge()
else:
    print "Quit"
