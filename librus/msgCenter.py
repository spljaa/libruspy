import smtplib
import time
from email.message import EmailMessage
from email.utils import make_msgid


class msgCenter:
    mysmtp = "smtphost"
    mysmtpauth = ["user", "pass"]
    dstemail = ""
    frmemail = ""

    def __init__(self, server, user, password, dst, frm):
        self.mysmtp = server
        self.mysmtpauth = [user, password]
        self.dstemail = dst
        self.frmemail = frm

    def callSMTP(self, msg):
        server_ssl = smtplib.SMTP_SSL(self.mysmtp, 465)
        server_ssl.ehlo()
        server_ssl.login(self.mysmtpauth[0], self.mysmtpauth[1])
        msg['To'] = self.dstemail
        msg['Reply-To'] = self.dstemail
        server_ssl.send_message(msg)
        server_ssl.close()
        time.sleep(2)

    def sendPlan(self, img, week):
        msg = EmailMessage()
        mid = make_msgid()
        msg.set_content('Tekstowa wersja')
        msg.add_alternative("""\
<html>
  <head></head>
  <body>
    <img src="cid:{mid}" />
  </body>
</html>
""".format(mid=mid[1:-1]), subtype='html')
        with open(img, 'rb') as img:
            msg.get_payload()[1].add_related(img.read(), 'image', 'png', cid=mid)
        msg['From'] = self.frmemail
        msg['Subject'] = "Librus: Plan tygodnia {}".format(week)
        self.callSMTP(msg)

    def sendEmail(self, lmsg):
        msg = EmailMessage()
        msg['From'] = "{} {}".format(lmsg[1], self.frmemail)
        msg['Subject'] = "Librus: {}".format(lmsg[2])
        if "<p>" in lmsg[0] and "</p>" in lmsg[0]:
            msg.set_content(lmsg[0], subtype='html')
        else:
            msg.set_content(lmsg[0])
        self.callSMTP(msg)
