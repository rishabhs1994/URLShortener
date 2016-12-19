import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
def func(to, shortenedurl): 
	fromaddr = "rishu.sanklecha@gmail.com"
	toaddr = to
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "TEST"
	 
	body = "Shortened URL " + shortenedurl 
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "--------")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

if(__name__ == '__main__'):
	func("rishabh.s@practo.com","AAA")
