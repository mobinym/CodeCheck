import datetime

def get_weekday(year):
    date = datetime.date(year, 1, 1)
    return date.strftime("%A")

if __name__ == "__main__":
    year = int(input())
    print(get_weekday(year))
