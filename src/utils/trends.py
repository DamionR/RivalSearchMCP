"""
Google Trends utility functions for RivalSearchMCP.
Helper functions for trends data processing and analysis.
"""

import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.logging.logger import logger


def generate_filename(
    prefix: str, keywords: List[str], extension: str, custom_name: Optional[str] = None
) -> str:
    """
    Generate filename for trends data export.

    Args:
        prefix: File prefix (e.g., 'trends', 'analysis')
        keywords: List of keywords used in the analysis
        extension: File extension (e.g., 'csv', 'json')
        custom_name: Optional custom filename

    Returns:
        Generated filename
    """
    if custom_name:
        # Ensure proper extension
        if not custom_name.endswith(f".{extension}"):
            custom_name = f"{custom_name}.{extension}"
        return custom_name

    # Generate filename from keywords
    keyword_str = "_".join(k[:3] for k in keywords[:3] for k in [k.replace(" ", "_")])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"{prefix}_{keyword_str}_{timestamp}.{extension}"


def create_export_directory(dir_name: str) -> Path:
    """
    Create export directory for trends data.

    Args:
        dir_name: Directory name

    Returns:
        Path to created directory
    """
    export_dir = Path(dir_name)
    export_dir.mkdir(exist_ok=True)
    logger.info(f"📁 Created export directory: {export_dir}")
    return export_dir


def sanitize_table_name(table_name: str) -> str:
    """
    Sanitize table name for SQLite compatibility.

    Args:
        table_name: Raw table name

    Returns:
        Sanitized table name
    """
    # Remove or replace invalid characters
    sanitized = "".join(c for c in table_name if c.isalnum() or c == "_")

    # Ensure it doesn't start with a number
    if sanitized and sanitized[0].isdigit():
        sanitized = f"table_{sanitized}"

    # Ensure it's not empty
    if not sanitized:
        sanitized = "trends_data"

    return sanitized


def format_date_range(start_date, end_date) -> str:
    """
    Format date range for display.

    Args:
        start_date: Start date
        end_date: End date

    Returns:
        Formatted date range string
    """
    try:
        if hasattr(start_date, "strftime") and hasattr(end_date, "strftime"):
            return (
                f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            )
        else:
            return f"{start_date} to {end_date}"
    except Exception:
        return "Unknown date range"


def validate_timeframe(timeframe: str) -> bool:
    """
    Validate Google Trends timeframe.

    Args:
        timeframe: Timeframe string to validate

    Returns:
        True if valid, False otherwise
    """
    valid_timeframes = [
        "now 1-H",
        "now 4-H",
        "now 1-d",
        "now 7-d",
        "today 1-m",
        "today 3-m",
        "today 12-m",
        "today 5-y",
        "2004-present",
    ]

    return timeframe in valid_timeframes


def validate_region(region: str) -> bool:
    """
    Validate Google Trends region code.

    Args:
        region: Region code to validate

    Returns:
        True if valid, False otherwise
    """
    valid_regions = [
        "US",
        "GB",
        "CA",
        "AU",
        "DE",
        "FR",
        "IT",
        "ES",
        "NL",
        "BR",
        "MX",
        "AR",
        "CL",
        "CO",
        "PE",
        "VE",
        "JP",
        "KR",
        "IN",
        "SG",
        "MY",
        "TH",
        "VN",
        "PH",
        "ID",
        "NZ",
        "ZA",
        "EG",
        "NG",
        "KE",
    ]

    return region.upper() in valid_regions


def validate_resolution(resolution: str) -> bool:
    """
    Validate geographic resolution for regional data.

    Args:
        resolution: Resolution string to validate

    Returns:
        True if valid, False otherwise
    """
    valid_resolutions = ["COUNTRY", "REGION", "CITY", "DMA"]
    return resolution.upper() in valid_resolutions


def calculate_trend_statistics(data: List[int]) -> Dict[str, Any]:
    """
    Calculate basic statistics for trend data.

    Args:
        data: List of trend values

    Returns:
        Dictionary with statistics
    """
    if not data:
        return {}

    import numpy as np

    data_array = np.array(data)

    return {
        "mean": float(np.mean(data_array)),
        "median": float(np.median(data_array)),
        "std": float(np.std(data_array)),
        "min": int(np.min(data_array)),
        "max": int(np.max(data_array)),
        "total_points": len(data_array),
    }


def export_to_excel(data: Dict[str, Any], filename: str) -> Dict[str, Any]:
    """
    Export trends data to Excel format.

    Args:
        data: Data to export
        filename: Output filename

    Returns:
        Export result
    """
    try:
        import pandas as pd

        # Convert data to DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame(data)

        # Export to Excel
        df.to_excel(filename, index=True)

        # Get file size
        size_bytes = os.path.getsize(filename)

        return {
            "success": True,
            "filename": filename,
            "format": "excel",
            "size_bytes": size_bytes,
            "path": os.path.abspath(filename),
        }

    except ImportError:
        return {
            "success": False,
            "error": "openpyxl not available. Install with: pip install openpyxl",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_trends_database(db_path: str = "trends_analysis.db") -> sqlite3.Connection:
    """
    Create SQLite database for trends analysis.

    Args:
        db_path: Database file path

    Returns:
        Database connection
    """
    conn = sqlite3.connect(db_path)

    # Create tables
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS trends_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            date TEXT NOT NULL,
            interest_value INTEGER NOT NULL,
            timeframe TEXT NOT NULL,
            geo TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS related_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            related_query TEXT NOT NULL,
            value INTEGER NOT NULL,
            type TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            geo TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS regional_interest (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            region TEXT NOT NULL,
            interest_value INTEGER NOT NULL,
            resolution TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            geo TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    logger.info(f"🗄️ Created trends database: {db_path}")

    return conn


def cleanup_export_files(directory: str, max_age_hours: int = 24):
    """
    Clean up old export files.

    Args:
        directory: Directory to clean
        max_age_hours: Maximum age of files in hours
    """
    try:
        export_dir = Path(directory)
        if not export_dir.exists():
            return

        current_time = datetime.now()
        max_age_seconds = max_age_hours * 3600

        for file_path in export_dir.glob("*"):
            if file_path.is_file():
                file_age = current_time.timestamp() - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    file_path.unlink()
                    logger.info(f"🗑️ Cleaned up old file: {file_path}")

    except Exception as e:
        logger.warning(f"Could not cleanup export files: {e}")
