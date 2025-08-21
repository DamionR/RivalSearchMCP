import logging
import sys
import os

# Create a centralized logger for the entire application
# Configure to use stderr instead of stdout to avoid corrupting MCP protocol
logger = logging.getLogger("rival_search_mcp")

# Set log level from environment variable or default to INFO
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logger.setLevel(getattr(logging, log_level, logging.INFO))

# Prevent propagation to root logger to avoid duplicate messages
logger.propagate = False

# Add handler if none exists (to avoid duplicate handlers)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
