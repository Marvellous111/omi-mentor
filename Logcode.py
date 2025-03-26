import logging
from pathlib import Path
import os

logger = logging.getLogger(__name__)

# We would like to create a log directory if it doesnt exist (perhaps example)
log_dir = Path(__file__) / "logs" # Create the logs folder in the same level as main.py
log_dir.mkdir(exist_ok=True)

# Lets set up logging with a more detailed format (from example)
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - [%(threadName)s] - %(module)s:%(lineno)d - %(message)s',
                   handlers=[
                       logging.FileHandler(log_dir / "mentor.log"),
                       logging.StreamHandler()
                   ])