import librus


msgdb = "_librusmsg.db"
dstemail = "mymail@mydomain.com"
planpng = "plan.png"
mysmtp = 'smtp.mydomain.com'
mysmtpauth = ["smtpaccount", "SecretPass"]

smtp = librus.msgCenter(mysmtp, mysmtpauth[0], mysmtpauth[1],
                        dstemail, "Librus Note <sender@mydomain.com>")


libdb = librus.LibrusMsgs(msgdb)
mylib = librus.Librus("LibrusID", "VerySecret")

mylib.setSubjects()
mylib.checkNewMsg(libdb, smtp)
mylib.checkNewNotes(libdb, smtp)
k = librus.Calendar(False)
k.addEvent("poniedziałek", "15:00", "16:00", "Chess class",
           "Teacher", "Location")
k.addEvent("środa", "15:00", "15:50", "Folk dance",
           "OtherTeacher", "School")
k = mylib.addEvents(k)
k.assignColors()

mylib.checkNewGrades(libdb, smtp)

mylib.logout()

k.draw(planpng)
smtp.sendPlan(planpng, k.week)
