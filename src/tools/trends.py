"""
Google Trends tools for FastMCP server.
Handles Google Trends data analysis, export, and comprehensive comparisons.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastmcp import FastMCP

from src.core.trends import GoogleTrendsAPI
from src.logging.logger import logger


def register_trends_tools(mcp: FastMCP):
    """Register all Google Trends-related tools."""

    @mcp.tool
    async def search_trends(
        keywords: List[str], timeframe: str = "today 12-m", geo: str = "US"
    ) -> dict:
        """
        Search for Google Trends data for given keywords.

        Args:
            keywords: List of search terms to analyze
            timeframe: Time range (e.g., 'today 12-m', 'today 5-y', 'now 1-d')
            geo: Geographic location (e.g., 'US', 'GB', 'CA')

        Returns:
            List of trend data for each keyword
        """
        try:
            logger.info(f"🔍 Searching trends for keywords: {keywords}")

            # Use the GoogleTrendsAPI class
            trends_api = GoogleTrendsAPI()

            # Get trends data
            data = trends_api.search_trends(keywords, timeframe, geo)

            if data.empty:
                return {
                    "success": False,
                    "error": "No data found for the specified keywords and timeframe",
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "geo": geo,
                }

            # Calculate statistics for each keyword
            results = []
            for keyword in keywords:
                if keyword in data.columns:
                    keyword_data = data[keyword].dropna()
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

                        stats = {
                            "keyword": keyword,
                            "mean_interest": float(keyword_data.mean()),
                            "peak_interest": int(keyword_data.max()),
                            "peak_date": peak_date_str,
                            "data_points": len(keyword_data),
                            "date_range": f"{str(data.index[0])} to {str(data.index[-1])}",
                        }
                        results.append(stats)

            logger.info(f"✅ Retrieved trend data for {len(results)} keywords")

            return {
                "success": True,
                "results": results,
                "keywords": keywords,
                "timeframe": timeframe,
                "geo": geo,
                "total_data_points": len(data),
            }

        except Exception as e:
            logger.error(f"❌ Error searching trends: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "keywords": keywords,
                "timeframe": timeframe,
                "geo": geo,
            }

    @mcp.tool
    async def get_related_queries(
        keyword: str, timeframe: str = "today 12-m", geo: str = "US"
    ) -> dict:
        """
        Get related queries for a keyword.

        Args:
            keyword: Search term to analyze
            timeframe: Time range for analysis
            geo: Geographic location

        Returns:
            List of related queries with interest values
        """
        try:
            logger.info(f"🔍 Getting related queries for: {keyword}")

            # Use the GoogleTrendsAPI class
            trends_api = GoogleTrendsAPI()

            # Get related queries
            related = trends_api.get_related_queries([keyword], timeframe, geo)

            results = []
            if keyword in related:
                data = related[keyword]

                # Add top queries
                if "top" in data and not data["top"].empty:
                    for _, row in data["top"].head(10).iterrows():
                        results.append(
                            {
                                "query": row["query"],
                                "value": int(row["value"]),
                                "type": "top",
                            }
                        )

                # Add rising queries
                if "rising" in data and not data["rising"].empty:
                    for _, row in data["rising"].head(10).iterrows():
                        results.append(
                            {
                                "query": row["query"],
                                "value": int(row["value"]),
                                "type": "rising",
                            }
                        )

            logger.info(f"✅ Found {len(results)} related queries")

            return {
                "success": True,
                "results": results,
                "keyword": keyword,
                "timeframe": timeframe,
                "geo": geo,
                "total_queries": len(results),
            }

        except Exception as e:
            logger.error(f"❌ Error getting related queries: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "keyword": keyword,
                "timeframe": timeframe,
                "geo": geo,
            }

    @mcp.tool
    async def get_interest_by_region(
        keyword: str,
        resolution: str = "COUNTRY",
        timeframe: str = "today 12-m",
        geo: str = "",
    ) -> dict:
        """
        Get interest by geographic region for a keyword.

        Args:
            keyword: Search term to analyze
            resolution: Geographic resolution ('COUNTRY', 'REGION', 'CITY', 'DMA')
            timeframe: Time range for analysis
            geo: Geographic location filter

        Returns:
            List of regions with interest values
        """
        try:
            logger.info(f"🌍 Getting regional interest for: {keyword}")

            # Use the GoogleTrendsAPI class
            trends_api = GoogleTrendsAPI()

            # Get regional interest data
            data = trends_api.get_interest_by_region(
                [keyword], resolution, timeframe, geo
            )

            results = []
            if not data.empty and keyword in data.columns:
                # Get top 20 regions
                top_regions = data.nlargest(20, keyword)

                for region, row in top_regions.iterrows():
                    results.append(
                        {
                            "region": region,
                            "interest": int(row[keyword]),
                            "keyword": keyword,
                        }
                    )

            logger.info(f"✅ Found interest data for {len(results)} regions")

            return {
                "success": True,
                "results": results,
                "keyword": keyword,
                "resolution": resolution,
                "timeframe": timeframe,
                "geo": geo,
                "total_regions": len(results),
            }

        except Exception as e:
            logger.error(f"❌ Error getting regional interest: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "keyword": keyword,
                "resolution": resolution,
                "timeframe": timeframe,
                "geo": geo,
            }

    @mcp.tool
    async def get_trending_searches(geo: str = "US") -> dict:
        """
        Get trending searches for a location.

        Args:
            geo: Geographic location (e.g., 'US', 'GB', 'CA')

        Returns:
            List of trending search terms
        """
        try:
            logger.info(f"🔥 Getting trending searches for: {geo}")

            # Use the GoogleTrendsAPI class
            trends_api = GoogleTrendsAPI()

            # Get trending searches
            trending = trends_api.get_trending_searches(geo)

            # Convert to list and get top 20
            if isinstance(trending, list):
                trending_list = trending[:20]
            else:
                trending_list = []

            logger.info(f"✅ Found {len(trending_list)} trending searches")

            return {
                "success": True,
                "trending_searches": trending_list,
                "geo": geo,
                "total_searches": len(trending_list),
            }

        except Exception as e:
            logger.error(f"❌ Error getting trending searches: {str(e)}")
            return {"success": False, "error": str(e), "geo": geo}

    @mcp.tool
    async def export_trends_to_csv(
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "US",
        filename: Optional[str] = None,
    ) -> dict:
        """
        Export Google Trends data to CSV file.

        Args:
            keywords: List of search terms
            timeframe: Time range for data
            geo: Geographic location
            filename: Optional custom filename

        Returns:
            Export result with file details
        """
        try:
            logger.info(f"📊 Exporting trends data for: {keywords}")

            # Use the GoogleTrendsAPI class
            trends_api = GoogleTrendsAPI()

            # Get interest over time data
            data = trends_api.search_trends(keywords, timeframe, geo)

            if data.empty:
                return {
                    "success": False,
                    "error": "No data found for the specified keywords and timeframe",
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "geo": geo,
                }

            # Export to CSV
            export_result = trends_api.export_data(data, "csv")

            if export_result.get("success"):
                logger.info(
                    f"✅ Exported trends data to CSV: {export_result['filename']}"
                )
                return {
                    "success": True,
                    "message": "Trends data exported to CSV successfully",
                    "filename": export_result["filename"],
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "geo": geo,
                    "file_path": export_result["path"],
                }
            else:
                return {
                    "success": False,
                    "error": export_result.get("error", "Export failed"),
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "geo": geo,
                }

        except Exception as e:
            logger.error(f"❌ Error exporting to CSV: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "keywords": keywords,
                "timeframe": timeframe,
                "geo": geo,
            }

    @mcp.tool
    async def export_trends_to_json(
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "US",
        filename: Optional[str] = None,
    ) -> dict:
        """
        Export Google Trends data to JSON file.

        Args:
            keywords: List of search terms
            timeframe: Time range for data
            geo: Geographic location
            filename: Optional custom filename

        Returns:
            Export result with file details
        """
        try:
            logger.info(f"📊 Exporting trends data to JSON for: {keywords}")

            # Use the GoogleTrendsAPI class
            trends_api = GoogleTrendsAPI()

            # Get interest over time data
            data = trends_api.search_trends(keywords, timeframe, geo)

            if data.empty:
                return {
                    "success": False,
                    "error": "No data found for the specified keywords and timeframe",
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "geo": geo,
                }

            # Export to JSON
            export_result = trends_api.export_data(data, "json")

            if export_result.get("success"):
                logger.info(
                    f"✅ Exported trends data to JSON: {export_result['filename']}"
                )
                return {
                    "success": True,
                    "message": "Trends data exported to JSON successfully",
                    "filename": export_result["filename"],
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "geo": geo,
                    "file_path": export_result["path"],
                }
            else:
                return {
                    "success": False,
                    "error": export_result.get("error", "Export failed"),
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "geo": geo,
                }

        except Exception as e:
            logger.error(f"❌ Error exporting to JSON: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "keywords": keywords,
                "timeframe": timeframe,
                "geo": geo,
            }

    @mcp.tool
    async def create_sql_table(
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "US",
        table_name: Optional[str] = None,
    ) -> dict:
        """
        Create SQLite table with Google Trends data.

        Args:
            keywords: List of search terms
            timeframe: Time range for data
            geo: Geographic location
            table_name: Optional custom table name

        Returns:
            SQL table creation result
        """
        try:
            logger.info(f"🗄️ Creating SQL table for: {keywords}")

            # Use the GoogleTrendsAPI class
            trends_api = GoogleTrendsAPI()

            # Get interest over time data
            data = trends_api.search_trends(keywords, timeframe, geo)

            if data.empty:
                return {
                    "success": False,
                    "error": "No data found for the specified keywords and timeframe",
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "geo": geo,
                }

            # Generate table name
            if not table_name:
                keyword_str = "_".join(
                    k[:3] for k in keywords[:3] for key in [k.replace(" ", "_")]
                )
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                table_name = f"trends_{keyword_str}_{timestamp}"

            # Sanitize table name
            table_name = "".join(c for c in table_name if c.isalnum() or c == "_")

            # Create database directory
            db_dir = Path("google_trends_db")
            db_dir.mkdir(exist_ok=True)
            db_path = db_dir / f"{table_name}.db"

            # Create SQLite table using the API
            table_result = trends_api.create_sql_table(data, table_name, str(db_path))

            if table_result.get("success"):
                logger.info(
                    f"✅ Created SQL table '{table_name}' with {table_result['rows_inserted']} rows"
                )
                return {
                    "success": True,
                    "table_name": table_name,
                    "rows_inserted": table_result["rows_inserted"],
                    "columns": table_result["columns"],
                    "database_path": str(db_path),
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "geo": geo,
                }
            else:
                return {
                    "success": False,
                    "error": table_result.get("error", "Failed to create table"),
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "geo": geo,
                }

        except Exception as e:
            logger.error(f"❌ Error creating SQL table: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "keywords": keywords,
                "timeframe": timeframe,
                "geo": geo,
            }

    @mcp.tool
    async def get_available_timeframes() -> dict:
        """
        Get list of available timeframes for Google Trends queries.

        Returns:
            List of available timeframe options
        """
        try:
            available_timeframes = [
                "now 1-H",  # Past hour
                "now 4-H",  # Past 4 hours
                "now 1-d",  # Past day
                "now 7-d",  # Past 7 days
                "today 1-m",  # Past month
                "today 3-m",  # Past 3 months
                "today 12-m",  # Past 12 months
                "today 5-y",  # Past 5 years
                "2004-present",  # All time
            ]

            logger.info(f"✅ Available timeframes: {len(available_timeframes)} options")

            return {
                "success": True,
                "timeframes": available_timeframes,
                "total_timeframes": len(available_timeframes),
            }

        except Exception as e:
            logger.error(f"❌ Error getting timeframes: {str(e)}")
            return {"success": False, "error": str(e)}

    @mcp.tool
    async def get_available_regions() -> dict:
        """
        Get list of available geographic regions.

        Returns:
            List of available region codes
        """
        try:
            available_regions = [
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

            logger.info(f"✅ Available regions: {len(available_regions)} countries")

            return {
                "success": True,
                "regions": available_regions,
                "total_regions": len(available_regions),
            }

        except Exception as e:
            logger.error(f"❌ Error getting regions: {str(e)}")
            return {"success": False, "error": str(e)}

    @mcp.tool
    async def compare_keywords_comprehensive(
        keywords: List[str], timeframe: str = "today 12-m", geo: str = "US"
    ) -> dict:
        """
        Comprehensive comparison of multiple keywords including trends, related queries, and regional interest.

        Args:
            keywords: List of keywords to compare
            timeframe: Time range for analysis
            geo: Geographic location

        Returns:
            Comprehensive comparison data
        """
        try:
            logger.info(f"🔍 Starting comprehensive comparison of: {keywords}")

            # Use GoogleTrendsAPI directly for all operations
            trends_api = GoogleTrendsAPI()

            # Get trends data
            trends_data_raw = trends_api.search_trends(keywords, timeframe, geo)
            trends_data = []
            if not trends_data_raw.empty:
                for keyword in keywords:
                    if keyword in trends_data_raw.columns:
                        keyword_data = trends_data_raw[keyword].dropna()
                        if not keyword_data.empty:
                            try:
                                from datetime import datetime

                                peak_date = keyword_data.idxmax()
                                if isinstance(peak_date, datetime):
                                    peak_date_str = peak_date.strftime("%Y-%m-%d")
                                else:
                                    peak_date_str = str(peak_date)
                            except Exception:
                                peak_date_str = str(peak_date)

                            trends_data.append(
                                {
                                    "keyword": keyword,
                                    "mean_interest": float(keyword_data.mean()),
                                    "peak_interest": int(keyword_data.max()),
                                    "peak_date": peak_date_str,
                                    "data_points": len(keyword_data),
                                }
                            )

            # Get related queries for each keyword
            related_queries = {}
            for keyword in keywords:
                try:
                    related_raw = trends_api.get_related_queries(
                        [keyword], timeframe, geo
                    )
                    if keyword in related_raw:
                        data = related_raw[keyword]
                        results = []

                        # Add top queries
                        if "top" in data and not data["top"].empty:
                            for _, row in data["top"].head(10).iterrows():
                                results.append(
                                    {
                                        "query": row["query"],
                                        "value": int(row["value"]),
                                        "type": "top",
                                    }
                                )

                        # Add rising queries
                        if "rising" in data and not data["rising"].empty:
                            for _, row in data["rising"].head(10).iterrows():
                                results.append(
                                    {
                                        "query": row["query"],
                                        "value": int(row["value"]),
                                        "type": "rising",
                                    }
                                )

                        related_queries[keyword] = results
                    else:
                        related_queries[keyword] = []
                except Exception as e:
                    logger.warning(
                        f"Could not get related queries for {keyword}: {str(e)}"
                    )
                    related_queries[keyword] = []

            # Get regional interest for first keyword
            regional_interest = []
            if keywords:
                try:
                    regional_raw = trends_api.get_interest_by_region(
                        [keywords[0]], "COUNTRY", timeframe, geo
                    )
                    if not regional_raw.empty and keywords[0] in regional_raw.columns:
                        # Get top 20 regions
                        top_regions = regional_raw.nlargest(20, keywords[0])

                        for region, row in top_regions.iterrows():
                            regional_interest.append(
                                {
                                    "region": region,
                                    "interest": int(row[keywords[0]]),
                                    "keyword": keywords[0],
                                }
                            )
                except Exception as e:
                    logger.warning(f"Could not get regional interest: {str(e)}")

            # Compile results
            result = {
                "keywords": keywords,
                "timeframe": timeframe,
                "geo": geo,
                "analysis_date": datetime.now().isoformat(),
                "trends_data": trends_data,
                "related_queries": related_queries,
                "regional_interest": regional_interest,
                "summary": {
                    "total_keywords": len(keywords),
                    "total_trend_points": len(trends_data),
                    "total_related_queries": sum(
                        len(v) for v in related_queries.values()
                    ),
                    "total_regions": len(regional_interest),
                },
            }

            logger.info(
                f"✅ Completed comprehensive comparison with {result['summary']['total_trend_points']} trend points"
            )

            return {
                "success": True,
                "comparison_result": result,
                "keywords": keywords,
                "timeframe": timeframe,
                "geo": geo,
            }

        except Exception as e:
            logger.error(f"❌ Error in comprehensive comparison: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "keywords": keywords,
                "timeframe": timeframe,
                "geo": geo,
            }
