import logging
import sys

# Configure logging to use stderr instead of stdout to avoid corrupting MCP protocol
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Redirect all logging to stderr
)
logger = logging.getLogger(__name__)
