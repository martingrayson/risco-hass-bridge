import logging
import logging.config
import os

CONFIGURATION = {
    'version': 1,

    'formatters': {
        'simple': {
            'format': '[%(asctime)s][%(name)s] %(levelname)s %(message)s',
            'datefmt': "%Y-%m-%dT%H:%M:%S%z",
        }
    },

    'handlers': {'console': {
        'level': os.environ.get('LOGGING_CONSOLE_LEVEL', 'DEBUG'),
        'class': 'logging.StreamHandler',
        'formatter': 'simple',
    }
    },

    'loggers': {
        '': {
            'level': os.environ.get('LOGGING_LEVEL', 'DEBUG'),
            'handlers': os.environ.get('LOGGING_HANDLERS',
                                       'console').split(','),
            'propagate': 0,
        }
    },
}

logging.config.dictConfigClass(CONFIGURATION).configure()


class CustomLogger(object):

    def __init__(self, **kwargs):
        self.logger = kwargs.pop('logger')

        if not self.logger or not hasattr(self.logger, 'log'):
            raise TypeError("Must specify a logger")

        self.extras = kwargs

    def log(self, level, message, *args, **kwargs):
        extra = self.extras.copy()
        extra.update(kwargs.pop('extra', {}))

        kwargs['extra'] = extra
        self.logger.log(level, message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        return self.log(logging.DEBUG, message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        return self.log(logging.INFO, message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        return self.log(logging.ERROR, message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        return self.log(logging.CRITICAL, message, *args, **kwargs)


class LoggingMixin(object):

    @property
    def logger(self):
        if not hasattr(self, '_logger') or not self._logger:
            self._logger = CustomLogger(logger=logging.getLogger(
                '.'.join([
                    self.__module__,
                    self.__class__.__name__
                ])))
        return self._logger
