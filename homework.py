import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        heute = dt.date.today()
        heute_data = sum(record.amount for record in self.records
                         if record.date == heute)
        return heute_data

    def get_week_stats(self):
        heute = dt.date.today()
        vor_eine_voche = heute - dt.timedelta(7)
        woche_datei = sum(record.amount for record in self.records
                          if vor_eine_voche <= record.date <= heute)
        return woche_datei

    def remained(self):
        return self.limit - self.get_today_stats()


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()


class CashCalculator(Calculator):
    USD_RATE = float(60.0)
    EURO_RATE = float(70.0)
    RUB_RATE = float(1.0)

    def get_today_cash_remained(self, currency):
        geld_bleiben = self.remained()
        if geld_bleiben == 0:
            return 'Денег нет, держись'
        currencies = {
            'eur': ('Euro', self.EURO_RATE),
            'usd': ('USD', self.USD_RATE),
            'rub': ('руб', self.RUB_RATE),
        }

        vaerung, fx = currencies.get(currency)
        geld_bleiben = round(geld_bleiben / fx, 2)
        if geld_bleiben > 0:
            return f'На сегодня осталось {geld_bleiben} {vaerung}'
        geld_bleiben = abs(geld_bleiben)
        return f'Денег нет, держись: твой долг - {geld_bleiben} {vaerung}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calorie_bleiben = self.remained()
        if calorie_bleiben <= 0:
            return 'Хватит есть!'
        return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {calorie_bleiben} кКал')


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
