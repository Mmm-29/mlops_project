import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Networksecurity.logging import logger
class securityException(Exception):
    """Base class for all security exceptions."""
    def __init__(self, error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.line_no = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
    
    def __str__(self):
        return "Error occurred in script name [{}] at line number [{}] with error message [{}]".format(
            self.file_name, 
            self.line_no, 
            str(self.error_message)
        )
    
