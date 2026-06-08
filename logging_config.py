import logging

def setup_logging():
    """Configures structured logging to output to a local file."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler() 
        ]
    )