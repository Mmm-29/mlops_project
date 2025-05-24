import logging
import os
from datetime import datetime
LOG_FILE="{}.log".format(datetime.now().strftime('%m_%d_%Y_%H_%M_%S')) 
log_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(log_path,exist_ok=True)
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    
)
logger = logging.getLogger(__name__)