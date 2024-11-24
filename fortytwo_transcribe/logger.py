import logging


class OneLineFormatter(logging.Formatter):
    def format(self, record):
        record.msg = record.msg.replace('\n', ' ')
        return super().format(record)

formatter = OneLineFormatter(
    fmt='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.basicConfig(
    level=logging.WARNING,
    handlers=[
        logging.FileHandler("logs/fortytwo_transcribe.log"),
        logging.StreamHandler()
    ]
)

for handler in logging.root.handlers:
    handler.setFormatter(formatter)

logger = logging.getLogger("FortyTwoTranscribe")
logger.setLevel(logging.INFO)