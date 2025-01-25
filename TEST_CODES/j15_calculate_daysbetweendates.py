from datetime import datetime

def calculate_days(date1, date2):
    date_format = "%d/%m/%Y"
    date1 = datetime.strptime(date1, date_format)
    date2 = datetime.strptime(date2, date_format)
    return (date2 - date1).days

if __name__ == "__main__":
    date1, date2 = input().split(', ')
    print(calculate_days(date1.strip("[]'"), date2.strip("[]'")))
