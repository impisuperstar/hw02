import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    x = int(datetime.datetime.today().strftime("%Y"))
    return  {
        'year': x
    }