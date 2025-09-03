#!/usr/bin/env python3
"""
Environment-based configurations for RivalSearchMCP.
"""

import os

def get_environment_config():
    """Get environment-based configuration."""
    return {
        "suppress_logs": os.environ.get("SUPPRESS_LOGS", "false").lower() == "true",
    }
