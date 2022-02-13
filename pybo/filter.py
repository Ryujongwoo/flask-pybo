import locale
locale.setlocale(locale.LC_ALL, '')

# 게시판에 출력할 날짜 서식을 변경하는 filter
def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)
