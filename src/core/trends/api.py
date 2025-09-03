"""
Google Trends API core functionality for RivalSearchMCP.
Provides access to Google Trends data for various use cases.
"""

import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.logging.logger import logger

# Set matplotlib style
try:
    plt.style.use("seaborn-v0_8")
except:
    plt.style.use("seaborn")


class GoogleTrendsAPI:
    """
    A comprehensive wrapper for Google Trends data using pytrends
    Provides access to all Google Trends functionality
    """

    def __init__(
        self, hl="en-US", tz=360, timeout=(10, 25), retries=3, backoff_factor=0.3
    ):
        """
        Initialize the Google Trends API wrapper

        Args:
            hl (str): Language (default: 'en-US')
            tz (int): Timezone offset in minutes (default: 360 for EST)
            timeout (tuple): Request timeout (connect, read)
            retries (int): Number of retries for failed requests
            backoff_factor (float): Backoff factor for retries
        """
        self.hl = hl
        self.tz = tz
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor

        # Initialize pytrends client
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the pytrends client."""
        from pytrends.request import TrendReq

        self.client = TrendReq(
            hl=self.hl,
            tz=self.tz,
            timeout=self.timeout,
            retries=self.retries,
            backoff_factor=int(self.backoff_factor),
        )
        logger.info("✅ Google Trends API client initialized successfully")

    def search_trends(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> pd.DataFrame:
        """
        Search for trends data for given keywords

        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data (e.g., 'today 12-m', 'today 5-y')
            geo (str): Geographic location (e.g., 'US', 'GB')
            cat (int): Category ID (0 for all categories)

        Returns:
            pd.DataFrame: Trends data
        """
        if not self.client:
            logger.error("Google Trends client not initialized")
            return pd.DataFrame()

        try:
            logger.info(f"🔍 Searching trends for: {keywords}")

            # Build payload
            self.client.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)

            # Get interest over time
            data = self.client.interest_over_time()

            if data.empty:
                logger.warning("No trends data found")
                return pd.DataFrame()

            logger.info(f"✅ Retrieved trends data with {len(data)} data points")
            return data

        except Exception as e:
            logger.error(f"❌ Error searching trends: {e}")
            return pd.DataFrame()

    def get_interest_over_time(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> pd.DataFrame:
        """
        Get interest over time data (alias for search_trends)

        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data
            geo (str): Geographic location
            cat (int): Category ID

        Returns:
            pd.DataFrame: Interest over time data
        """
        return self.search_trends(keywords, timeframe, geo, cat)

    def get_related_queries(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> Dict:
        """
        Get related queries for given keywords

        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data
            geo (str): Geographic location
            cat (int): Category ID

        Returns:
            Dict: Related queries data
        """
        if not self.client:
            logger.error("Google Trends client not initialized")
            return {}

        try:
            logger.info(f"🔍 Getting related queries for: {keywords}")

            # Build payload
            self.client.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)

            # Get related queries
            related = self.client.related_queries()

            logger.info(f"✅ Retrieved related queries data")
            return related

        except Exception as e:
            logger.error(f"❌ Error getting related queries: {e}")
            return {}

    def get_related_topics(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> Dict:
        """
        Get related topics for given keywords

        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data
            geo (str): Geographic location
            cat (int): Category ID

        Returns:
            Dict: Related topics data
        """
        if not self.client:
            logger.error("Google Trends client not initialized")
            return {}

        try:
            logger.info(f"🔍 Getting related topics for: {keywords}")

            # Build payload
            self.client.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)

            # Get related topics
            topics = self.client.related_topics()

            logger.info(f"✅ Retrieved related topics data")
            return topics

        except Exception as e:
            logger.error(f"❌ Error getting related topics: {e}")
            return {}

    def get_interest_by_region(
        self,
        keywords: List[str],
        resolution: str = "COUNTRY",
        timeframe: str = "today 12-m",
        geo: str = "",
    ) -> pd.DataFrame:
        """
        Get interest by geographic region for given keywords

        Args:
            keywords (List[str]): List of search terms
            resolution (str): Geographic resolution ('COUNTRY', 'REGION', 'CITY', 'DMA')
            timeframe (str): Time range for data
            geo (str): Geographic location filter

        Returns:
            pd.DataFrame: Regional interest data
        """
        if not self.client:
            logger.error("Google Trends client not initialized")
            return pd.DataFrame()

        try:
            logger.info(f"🌍 Getting regional interest for: {keywords}")

            # Build payload
            self.client.build_payload(keywords, cat=0, timeframe=timeframe, geo=geo)

            # Get interest by region
            data = self.client.interest_by_region(resolution=resolution)

            if data.empty:
                logger.warning("No regional interest data found")
                return pd.DataFrame()

            logger.info(f"✅ Retrieved regional interest data for {len(data)} regions")
            return data

        except Exception as e:
            logger.error(f"❌ Error getting regional interest: {e}")
            return pd.DataFrame()

    def get_trending_searches(self, geo: str = "US") -> List[str]:
        """
        Get trending searches for a location

        Args:
            geo (str): Geographic location (e.g., 'US', 'GB', 'CA')

        Returns:
            List[str]: List of trending search terms
        """
        if not self.client:
            logger.error("Google Trends client not initialized")
            return []

        try:
            logger.info(f"🔥 Getting trending searches for: {geo}")

            # Get trending searches
            trending = self.client.trending_searches(pn=geo)

            if trending.empty:
                logger.warning("No trending searches found")
                return []

            # Convert to list
            trending_list = trending[0].tolist()

            logger.info(f"✅ Retrieved {len(trending_list)} trending searches")
            return trending_list

        except Exception as e:
            logger.error(f"❌ Error getting trending searches: {e}")
            return []

    def get_realtime_trending_searches(self, geo: str = "US") -> List[str]:
        """
        Get real-time trending searches for a location

        Args:
            geo (str): Geographic location (e.g., 'US', 'GB', 'CA')

        Returns:
            List[str]: List of real-time trending search terms
        """
        if not self.client:
            logger.error("Google Trends client not initialized")
            return []

        try:
            logger.info(f"⚡ Getting real-time trending searches for: {geo}")

            # Get real-time trending searches
            trending = self.client.realtime_trending_searches(pn=geo)

            if trending.empty:
                logger.warning("No real-time trending searches found")
                return []

            # Convert to list
            trending_list = trending[0].tolist()

            logger.info(
                f"✅ Retrieved {len(trending_list)} real-time trending searches"
            )
            return trending_list

        except Exception as e:
            logger.error(f"❌ Error getting real-time trending searches: {e}")
            return []

    def get_statistics(self, data: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Calculate comprehensive statistics for trends data

        Args:
            data (pd.DataFrame): Trends data from search_trends

        Returns:
            Dict[str, Dict[str, Any]]: Statistics for each keyword
        """
        if data.empty:
            return {}

        try:
            logger.info("📊 Calculating trends statistics")

            stats = {}
            for column in data.columns:
                if column == "isPartial":
                    continue

                keyword_data = data[column].dropna()
                if not keyword_data.empty:
                    peak_date = keyword_data.idxmax()
                    try:
                        # Type cast to handle type checker
                        from datetime import datetime

                        if isinstance(peak_date, datetime):
                            peak_date_str = peak_date.strftime("%Y-%m-%d")
                        else:
                            peak_date_str = str(peak_date)
                    except Exception:
                        peak_date_str = str(peak_date)

                    stats[column] = {
                        "mean": float(keyword_data.mean()),
                        "median": float(keyword_data.median()),
                        "std": float(keyword_data.std()),
                        "min": int(keyword_data.min()),
                        "max": int(keyword_data.max()),
                        "peak_value": int(keyword_data.max()),
                        "peak_date": peak_date_str,
                        "total_points": len(keyword_data),
                        "trend_direction": self._calculate_trend_direction(
                            keyword_data
                        ),
                        "volatility": (
                            float(keyword_data.std() / keyword_data.mean())
                            if keyword_data.mean() > 0
                            else 0
                        ),
                    }

            logger.info(f"✅ Calculated statistics for {len(stats)} keywords")
            return stats

        except Exception as e:
            logger.error(f"❌ Error calculating statistics: {e}")
            return {}

    def _calculate_trend_direction(self, data: pd.Series) -> str:
        """Calculate trend direction (increasing, decreasing, stable)."""
        if len(data) < 2:
            return "insufficient_data"

        # Calculate linear trend
        x = np.arange(len(data))
        slope = np.polyfit(x, data, 1)[0]

        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"

    def export_data(
        self, data: pd.DataFrame, format: str = "csv", filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export trends data to various formats

        Args:
            data (pd.DataFrame): Data to export
            format (str): Export format ('csv', 'json', 'excel')
            filename (str): Optional custom filename

        Returns:
            Dict[str, Any]: Export result
        """
        if data.empty:
            return {"success": False, "error": "No data to export"}

        try:
            logger.info(f"📊 Exporting data to {format.upper()}")

            # Generate filename
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"trends_data_{timestamp}.{format}"

            # Export based on format
            if format.lower() == "csv":
                data.to_csv(filename, index=True)
            elif format.lower() == "json":
                data.to_json(filename, orient="records", indent=2)
            elif format.lower() == "excel":
                data.to_excel(filename, index=True)
            else:
                return {"success": False, "error": f"Unsupported format: {format}"}

            # Get file size
            size_bytes = os.path.getsize(filename)

            logger.info(f"✅ Exported data to {filename}")

            return {
                "success": True,
                "filename": filename,
                "format": format,
                "size_bytes": size_bytes,
                "path": os.path.abspath(filename),
            }

        except Exception as e:
            logger.error(f"❌ Error exporting data: {e}")
            return {"success": False, "error": str(e)}

    def create_sql_table(
        self, data: pd.DataFrame, table_name: str, db_path: str = "trends_data.db"
    ) -> Dict[str, Any]:
        """
        Create SQLite table with trends data

        Args:
            data (pd.DataFrame): Data to insert
            table_name (str): Table name
            db_path (str): Database file path

        Returns:
            Dict[str, Any]: Table creation result
        """
        if data.empty:
            return {"success": False, "error": "No data to create table from"}

        try:
            logger.info(f"🗄️ Creating SQL table '{table_name}'")

            # Create database connection
            conn = sqlite3.connect(db_path)

            # Reset index to make date a regular column
            data_reset = data.reset_index()
            data_reset.rename(columns={"date": "trend_date"}, inplace=True)

            # Write to SQLite
            data_reset.to_sql(table_name, conn, if_exists="replace", index=False)

            # Get table info
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]

            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]

            conn.close()

            logger.info(f"✅ Created SQL table '{table_name}' with {row_count} rows")

            return {
                "success": True,
                "table_name": table_name,
                "rows_inserted": row_count,
                "columns": columns,
                "database_path": db_path,
            }

        except Exception as e:
            logger.error(f"❌ Error creating SQL table: {e}")
            return {"success": False, "error": str(e)}

    def get_available_timeframes(self) -> List[str]:
        """Get list of available timeframes."""
        return [
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

    def get_available_regions(self) -> List[str]:
        """Get list of available geographic regions."""
        return [
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

    def is_available(self) -> bool:
        """Check if the API is available and working."""
        return hasattr(self, "client") and self.client is not None

    def close(self):
        """Close the API client."""
        if hasattr(self, "client") and self.client:
            try:
                # pytrends doesn't have a close method, but we can clean up
                del self.client
                self.client = None
                logger.info("✅ Google Trends API client closed")
            except Exception as e:
                logger.warning(f"Warning: Could not close client cleanly: {e}")
