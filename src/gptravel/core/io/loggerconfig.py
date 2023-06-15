import logging
import os

from dotenv import load_dotenv

load_dotenv()

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
FORMAT = "[%(asctime)s - %(levelname)s] %(message)s"
logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)
handler = logging.StreamHandler()
handler.setLevel(LOGLEVEL)
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)
