import logging

from edge.registry.colors import bcolors

class LoggingFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: bcolors.gray + bcolors.bold,
        logging.INFO: bcolors.blue + bcolors.bold,
        logging.WARNING: bcolors.yellow + bcolors.bold,
        logging.ERROR: bcolors.red,
        logging.CRITICAL: bcolors.red + bcolors.bold,
    }
    
    # default name color
    DEFAULT_NAME_COLOR = bcolors.green + bcolors.bold
    
    def __init__(self, name_color=None):
        super().__init__()
        self.name_color = name_color if name_color else self.DEFAULT_NAME_COLOR
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelno, bcolors.reset)
        format_str = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (namecolor){name}(reset) {message}"
        format_str = format_str.replace("(black)", bcolors.black + bcolors.bold)
        format_str = format_str.replace("(reset)", bcolors.reset)
        format_str = format_str.replace("(levelcolor)", log_color)
        format_str = format_str.replace("(namecolor)", self.name_color)
        formatter = logging.Formatter(format_str, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)

# shared file handler formatter
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)

def setup_logger(name, log_file, level=logging.INFO, name_color: bool = None, retain: bool = False):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers = []

    logger.propagate = False
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LoggingFormatter(name_color=name_color))
    logger.addHandler(console_handler)
    
    file_handler = logging.FileHandler(filename=log_file, encoding="utf-8", mode="a" if retain else "w")
    file_handler.setFormatter(file_handler_formatter)
    logger.addHandler(file_handler)
    
    return logger

#context build
cockatoo_logger = setup_logger("cockatoo.edge", "logs/cockatoo.log", logging.INFO) #exclusive for commands
db_logger = setup_logger("cockatoo.database", "logs/database.log", logging.INFO, name_color=bcolors.blue) #exclusively for database
scanner_logger = setup_logger("cockatoo.moderation", "logs/moderation.log", logging.INFO, name_color=bcolors.magenta)