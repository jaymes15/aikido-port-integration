import sys
from loguru import logger


def setup_logging(level: str = "INFO"):
    """
    Setup logging configuration for the integration.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Remove default handler
    logger.remove()

    # Add console handler with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # Add file handler for persistent logs
    logger.add(
        "logs/integration.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )

    # Add error file handler
    logger.add(
        "logs/errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="5 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )

    logger.info(f"🔧 Logging configured with level: {level}")
    logger.info("📁 Logs will be saved to: logs/integration.log and logs/errors.log")


def get_logger():
    """Get the configured logger instance."""
    return logger
