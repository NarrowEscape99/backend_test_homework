import datetime as dt


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if date is not None:
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.date.today()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_week_stats(self):
        now = dt.date.today()
        one_week_ago = now - dt.timedelta(days=7)
        weekly_data = [record.amount for record in self.records if
                       one_week_ago <= record.date <= now]
        return sum(weekly_data)

    def get_today_stats(self):
        now = dt.date.today()
        daily_data = [record.amount for record in self.records if
                      record.date == now]
        return sum(daily_data)

    def get_today_limit_balance(self):
        money_limit = self.limit - self.get_today_stats()
        return money_limit


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        now_calories = self.limit - self.get_today_stats()
        if self.get_today_stats() < 0:
            answer_1 = ('Сегодня можно съесть что-нибудь ещё, но с общей '
                        'калорийностью не более '
                        f'{now_calories} кКал')
            return answer_1
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        now_stats = self.get_today_stats()
        currenсies = {
            'usd': ('USD', CashCalculator.USD_RATE),
            'eur': ('Euro', CashCalculator.EURO_RATE),
            'rub': ('руб', CashCalculator.RUB_RATE),
        }
        foreign_exchange, rate = currenсies[currency]
        money_now = round(((
            self.limit - now_stats) / rate), 2)
        if now_stats < self.limit:
            answer_2 = (f'На сегодня осталось {money_now} '
                        f'{foreign_exchange}')
            return answer_2
        if now_stats == self.limit:
            return 'Денег нет, держись'
        debt = 0 - money_now
        answer_3 = ('Денег нет, держись: твой долг - '
                    f'{debt} {foreign_exchange}')
        return answer_3
