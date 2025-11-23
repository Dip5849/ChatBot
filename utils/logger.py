import logging
import logging.config
import os
from datetime import datetime
import structlog


def logger_config_dict(log_file_name):

    """Function to return logging configuration dictionary"""
    log_config = {
        'version':1,
        'formatters':{
            'file_formatter':{
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.JSONRenderer()
            },
            'console_formatter':{
                '()': structlog.stdlib.ProcessorFormatter, 
                'processor': structlog.dev.ConsoleRenderer()
            }

        },
        'handlers':{
            'file':{
                'class':'logging.FileHandler',
                'formatter':'file_formatter',
                'level':'INFO',
                'filename': log_file_name
            },
            'console':{
                'class':'logging.StreamHandler',
                'formatter':'console_formatter',
                'level':'DEBUG'
            }

        },
        'loggers':{
            'custom_logger':{
                'handlers':['file','console'],
                'level':'DEBUG',
                'propagate':True
            }
        }
    }

    return log_config


class CustomLogger:
    def __init__(self, log_dir_name = 'logs'):

        ## Defining log directory and file paths        
        self.log_dir_path = os.path.join(os.getcwd(),log_dir_name)
        self.log_file_name = f'Log_{datetime.now().strftime('%d_%m_%Y__%H_%M_%S')}.log'
        self.log_file_path = os.path.join(self.log_dir_path, self.log_file_name)

        #creating log directory if it doesn't exist        
        os.makedirs(self.log_dir_path, exist_ok=True)
        logging.config.dictConfig(logger_config_dict(self.log_file_path))
        structlog.configure(
            processors=[
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory()
        )

    def get_logger(self, name):
        name = 'custom_logger.'+ os.path.basename(name)# Ensuring the logger name matches the configuration
        return structlog.getLogger(name)


if __name__ == "__main__":
    logger = CustomLogger().get_logger('custom_logger')
    logger.info('this is working fine', user='dip', password='mondal')
    print(os.getcwd())