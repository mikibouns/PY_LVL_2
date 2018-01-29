import logging
import sys
import logging.handlers

# формат сообщения
format = logging.Formatter('%(asctime)s %(levelname)-10s %(message)s')

# выводит сообщения с уровнем ERROR в поток stderr
crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.ERROR)
crit_hand.setFormatter(format)

# обработчик, выводит сообщения в файл
# applog_hand = logging.FileHandler('app.log')
# applog_hand.setLevel(logging.INFO)
# applog_hand.setFormatter(format)

# ротация логов
rotation_hand = logging.handlers.RotatingFileHandler('app.log', maxBytes=125000, backupCount=10)
rotation_hand.setLevel(logging.INFO)
rotation_hand.setFormatter(format)

# регистратор верхнего уровня
app_log = logging.getLogger('app')
app_log.setLevel(logging.INFO)
# app_log.addHandler(applog_hand)
app_log.addHandler(crit_hand)
app_log.addHandler(rotation_hand)


if __name__ == '__main__':
    pass