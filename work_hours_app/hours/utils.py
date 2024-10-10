from calendar import HTMLCalendar

class Calendar(HTMLCalendar):
    def __init__(self, work_entries):
        super().__init__()
        self.work_entries = work_entries

    def formatday(self, day, weekday):
        work_entries_per_day = self.work_entries.filter(date__day=day)
        d = ''
        for entry in work_entries_per_day:
            d += f'<li>{entry.hours_worked}h - {entry.description}</li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, weekday)
        return f'<tr> {week} </tr>'

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super().formatmonth(year, month)
