import logging, json, os
from logging.handlers import RotatingFileHandler


LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'bot.log')

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            'time': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
        }
        if record.exc_info:
            payload['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(payload)

def get_logger(name=__name__):
    logger = logging.getLogger('binance_bot')
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)


    fh = RotatingFileHandler(LOG_PATH, maxBytes=5_000_000, backupCount=2)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(JsonFormatter())


    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  
    ch.setFormatter(JsonFormatter())

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
