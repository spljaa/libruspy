import requests
from datetime import datetime


class Librus:
    username = ""
    password = ""
    web = requests.session()
    __mainhost = "https://synergia.librus.pl"
    __messagehost = "https://wiadomosci.librus.pl"
    __apihost = "https://api.librus.pl"
    __portalhost = "https://portal.librus.pl/"
    __apigateway = "https://synergia.librus.pl/gateway/api/2.0"
    msgs = []
    msgscount = 0
    subjects = {}
    teachers = {}
    classrooms = {}

    def __init__(self, user, pw):
        self.username = user
        self.password = pw
        self.login()

    def login(self):
        my_headers = {"Referer": self.__portalhost}
        self.web.get("{}/rodzina".format(self.__portalhost))
        w = self.web.get("{}/loguj/portalRodzina?v={}".format(self.__mainhost, int(datetime.timestamp(datetime.now()))), headers=my_headers)
        nloc = w.history[1].headers["location"]
        self.web.get("{}{}".format(self.__apihost, nloc))
        pdata = {"action": "login",
                 "login": self.username,
                 "pass": self.password}
        resp = self.web.post("{}{}".format(self.__apihost, nloc),
                             data=pdata).json()
        print(resp["status"])
        if resp["status"] == "actionRequired":
            print(resp)
        nurl = resp["goTo"].replace("\\", "")
        self.web.get("{}{}".format(self.__apihost, nurl))
        self.web.get("{}/wiadomosci3".format(self.__mainhost))

    def logout(self):
        r = self.web.get("{}/api/auth/logout".format(self.__messagehost)).json()["data"]
        print(r["status"])
        nurl = r["redirectUrl"]
        self.web.get("{}{}".format(self.__messagehost, nurl))

    def setSubjects(self):
        s = self.callAPI("Subjects")
        for it in s["Subjects"]:
            self.subjects[it["Id"]] = it["Name"]

    def getTeacher(self, tid):
        if tid not in self.teachers:
            r = self.callAPI("Users/{}".format(tid))
            self.teachers[tid] = r["User"]["FirstName"] + " " + r["User"]["LastName"]
        return self.teachers[tid]

    def getClassroom(self, cid):
        if cid not in self.classrooms:
            r = self.callAPI("Classrooms/{}".format(cid))
            self.classrooms[cid] = r["Classroom"]["Name"]
        return self.classrooms[cid]

    def callAPI(self, endpoint: str):
        return self.web.get("{}/{}".format(self.__apigateway, endpoint)).json()

    def addEvents(self, calendar):
        planZajecRaw = self.callAPI("Timetables?weekStart={}".format(calendar.week))
        day = 0
        for k, v in planZajecRaw["Timetable"].items():
            for lekcja in v:
                if len(lekcja) == 1:
                    s = self.subjects[int(lekcja[0]["Subject"]["Id"])]
                    t = self.getTeacher(int(lekcja[0]["Teacher"]["Id"]))
                    z = lekcja[0]["IsSubstitutionClass"]
                    if not z:
                        sala = self.getClassroom(int(lekcja[0]["Classroom"]["Id"]))
                    else:
                        sala = self.getClassroom(int(lekcja[0]["OrgClassroom"]["Id"]))
                    h = lekcja[0]["HourFrom"]
                    e = lekcja[0]["HourTo"]
                    calendar.addEvent(calendar.ty[day], h, e, s, t, sala, z)
                if len(lekcja) > 1:
                    print("DZIWNA LEKCJA")
            day = day + 1
        return calendar

    def getFullMsg(self, msgid):
        return self.web.get("https://wiadomosci.librus.pl/api/inbox/messages/{}".format(msgid)).json()["data"]

    def checkNewMsg(self, librusdb, msgCenter):
        lmsgs = self.web.get("https://wiadomosci.librus.pl/api/inbox/messages").json()
        self.msgs = lmsgs["data"]
        self.msgscount = lmsgs["total"]
        indb = librusdb.getMsgIds()
        inlib = [int(x["messageId"]) for x in self.msgs]
        for k in inlib:
            if k in indb:
                print("{} w bazie".format(k))
            else:
                print("{} pobierane".format(k))
                librusdb.addMessage(self.getFullMsg(k))
                msgCenter.sendEmail(librusdb.printMsg(k))

    def checkNewNotes(self, librusdb, msgCenter):
        notices = self.callAPI("SchoolNotices")["SchoolNotices"]
        indb = librusdb.getNoteIds()
        for k in notices:
            if k["Id"] in indb:
                print("{} w bazie".format(k["Id"]))
            else:
                print("{} pobierane".format(k["Id"]))
                librusdb.addNotice(k)
                msgCenter.sendEmail(librusdb.printNotice(k["Id"]))
    
    def checkNewGrades(self, librusdb, msgCenter):
        grades = self.callAPI("Grades")["Grades"]
        indb = librusdb.getGradeIds()
        for g in grades:
            if str(g["Id"]) in indb:
                print("{} w bazie".format(g["Id"]))
            else:
                print("{} pobierane".format(g["Id"]))
                grd = {}
                grd["Id"] = g["Id"]
                grd["Date"] = g["Date"]
                grd["Subject"] = self.subjects[g["Subject"]["Id"]]
                grd["Grade"] = g["Grade"]
                librusdb.addGrade(grd)
                msgCenter.sendEmail(librusdb.printGrade(g["Id"]))
