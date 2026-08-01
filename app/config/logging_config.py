import logging.config

from app.contexts import REQUEST_ID


class RequestIdFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.request_id = REQUEST_ID.get()
        return super().format(record)


def setup_logging() -> None:
    logging.config.dictConfig(LOGGER_SETTINGS)


LOGGER_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "app.config.logging_config.RequestIdFormatter",
            "format": (
                "%(asctime)s | "
                "%(levelname)s | "
                "%(name)s | "
                "%(request_id)s | "
                "%(message)s"
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}
