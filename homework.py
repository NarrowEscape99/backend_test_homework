import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_today_stats(self):
        summ = [record.amount for record in self.records if
                record.date == dt.date.today()]
        return sum(summ)

    def get_week_stats(self):
        woche = dt.date.today() - dt.timedelta(days=7)
        woche_summ = [record.amount for record in self.records if
                      woche <= record.date <= dt.date.today()]
        return sum(woche_summ)


class CashCalculator(Calculator):
    USD_RATE = float(60.0)
    EURO_RATE = float(70.0)
    RUB_RATE = float(1.0)
    heute_geld = 0
    currenсies = {
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE),
        'rub': ('руб', RUB_RATE),
    }

    def get_today_cash_remained(self, currency):
        vaerung = self.currenсies[currency]
        heute_geld = round(((
            self.limit - self.get_today_stats()) / vaerung[1]), 2)
        if self.get_today_stats() < self.limit:
            antwort1 = (f'На сегодня осталось {heute_geld} '
                        f'{vaerung[0]}')
            return antwort1
        elif self.get_today_stats() == self.limit:
            return 'Денег нет, держись'
        else:
            geld_abs = abs(heute_geld)
            antwort2 = ('Денег нет, держись: твой долг - '
                        f'{geld_abs} {vaerung[0]}')
            return antwort2


class CaloriesCalculator(Calculator):
    today_calories_remained = 0

    def get_calories_remained(self):
        heute_cal = abs(self.limit - self.get_today_stats())
        if self.get_today_stats() < self.limit:
            antwort3 = ('Сегодня можно съесть что-нибудь ещё, но с общей '
                        'калорийностью не более '
                        f'{heute_cal} кКал')
            return antwort3
        else:
            return 'Хватит есть!'


cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
