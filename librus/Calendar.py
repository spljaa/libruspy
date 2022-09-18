import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from math import ceil


class Calendar:
    mojlibrus = ""
    ty = ["poniedziałek", "wtorek", "środa", "czwartek",
          "piątek", "sobota", "niedziela"]
    bazowekolory = ["lightcoral", "orange", "gold", "turquoise",
                    "plum", "lime", "salmon", "crimson"]
    eventstypes = {"Day": "int", "HourFrom": "str", "HourTo": "str",
                   "Subject": "str", "Teacher": "str", "Classroom": "str",
                   "IsSubstitution": "bool"}
    events = pd.DataFrame({c: pd.Series(dtype=t) for c, t in eventstypes.items()})
    latest = 17
    earliest = 7
    colors = {}

# shift week add a number to current week
    def __init__(self, shiftweek=0):
        dzis = datetime.today()
        d = 7 * shiftweek
# On weekend assume we ask for incomming plan
        if dzis.weekday() > 4:
            d = d + 7
        n = dzis + timedelta(days=(d-dzis.weekday()))
        self.week = n.strftime("%Y-%m-%d")

    def addEvent(self, day: str, start: str, end: str, subject,
                 teacher, classrom, issubstitution=False):
        dayofweek = self.ty.index(day)
        newEvent = {"Day": dayofweek, "HourFrom": start, "HourTo": end,
                    "Subject": subject, "Teacher": teacher,
                    "Classroom": classrom, "IsSubstitution": issubstitution}
        self.events = pd.concat([self.events,
                                 pd.DataFrame(newEvent, index=[0])]).reset_index(drop=True)

    def assignColors(self):
        i = 0
        for k in sorted(self.events["Subject"].unique()):
            self.colors[k] = self.bazowekolory[i]
            i = i + 1

    def draw(self, dstfile=None):
        plt.figure(figsize=(18, 9))
        plt.title('Plan {}'.format(self.week), fontsize=14)
        plt.xticks(range(1, len(self.ty) + 1), labels=self.ty)
        plt.yticks(range(ceil(self.earliest), ceil(self.latest)),
                   labels=["{0}:00".format(h) for h in range(ceil(self.earliest), ceil(self.latest))])
        plt.ylim(self.latest, self.earliest)
        plt.xlim(0.5, len(self.ty) + 0.5)

        def drawEvent(row):
            day = row["Day"]
            d = day + 0.52
            startH, startM = row["HourFrom"].split(":")
            endH, endM = row["HourTo"].split(":")
            start = float(startH) + float(startM) / 60
            end = float(endH) + float(endM) / 60
            plt.fill_between([d, d+0.96], [start, start], [end, end],
                             color=self.colors[row["Subject"]])
            plt.text(d + 0.94, end - 0.05, row["Classroom"],
                     ha="right", fontsize=9)
            if row["IsSubstitution"]:
                plt.text(d + 0.02, start + 0.05,
                         "Zastępstwo", va='top', fontsize=10)
            plt.text(d + 0.48, (start + end) * 0.502, row["Subject"],
                     ha='center', va='center', fontsize=10)

        self.events.apply(drawEvent, axis=1)
        if dstfile is None:
            plt.show()
        else:
            plt.savefig(dstfile)
