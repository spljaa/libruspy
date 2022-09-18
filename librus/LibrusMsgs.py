import sqlite3
import base64


class LibrusMsgs:
    db = ""
    cur = ""

    def __init__(self, dbpath):
        self.db = sqlite3.connect(dbpath)
        self.cur = self.db.cursor()
        self.runQuery('''CREATE TABLE IF NOT EXISTS wiadomosci
                        (id int primary key, nadawca text,
                         temat text, wiadomosc text)''')
        self.runQuery('''CREATE TABLE IF NOT EXISTS ogloszenia
                        (id text primary key, startDate text,
                         temat text, ogloszenie text)''')
        self.runQuery('''CREATE TABLE IF NOT EXISTS grades
                        (id text primary key, date text,
                         subject text, grade text)''')

    def finish(self):
        self.db.close()

    def runQuery(self, query, params=None):
        if params is not None:
            self.cur.execute(query, params)
        else:
            self.cur.execute(query)
        self.db.commit()

    def addMessage(self, msg):
        query = "insert into wiadomosci values (?, ?, ?, ?)"
        params = (msg["messageId"], msg["senderName"],
                  msg["topic"], msg["Message"])
        self.runQuery(query, params)

    def getIds(self, table):
        resp = self.cur.execute("select id from {}".format(table))
        ids = resp.fetchall()
        return [x[0] for x in ids]

    def getMsgIds(self):
        return self.getIds("wiadomosci")

    def printMsg(self, msgid):
        msg = self.cur.execute("select nadawca, temat, wiadomosc from wiadomosci where id = ?", (msgid,)).fetchone()
        return ["""\
{}""".format(base64.b64decode(msg[2]).decode("utf8")), msg[0], msg[1]]

    def addNotice(self, note):
        query = "insert into ogloszenia values (?, ?, ?, ?)"
        params = (note["Id"], note["StartDate"],
                  note["Subject"], note["Content"])
        self.runQuery(query, params)

    def getNoteIds(self):
        return self.getIds("ogloszenia")

    def printNotice(self, noteid):
        msg = self.cur.execute("select temat, startDate, ogloszenie from ogloszenia where id = ?", (noteid,)).fetchone()
        return["""\
{}""".format(msg[2]), "SchoolNotice", " ".join([msg[1], msg[0]])]

    def getGradeIds(self):
        return self.getIds("grades")

    def addGrade(self, grd):
        query = "insert into grades values (?, ?, ?, ?)"
        params = (grd["Id"], grd["Date"], grd["Subject"], grd["Grade"])
        self.runQuery(query, params)

    def printGrade(self, grdid):
        msg = self.cur.execute("select subject, date, grade from grades where id = ?", (grdid,)).fetchone()
        return["""\
{}""".format(" "), "NewGrade", " ".join([msg[2], msg[0], "({})".format(msg[1])])]
