#!/usr/bin/env python3
"""
Comprehensive MCP Test Suite
Combines all testing approaches with real-world scenarios across multiple industries.
Tests MCP protocol communication over STDIO with diverse use cases.
"""

import sys
import os
import json
import subprocess
import time
import asyncio
import signal
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

@dataclass
class TestScenario:
    """Test scenario configuration."""
    name: str
    industry: str
    description: str
    tool_name: str
    arguments: Dict[str, Any]
    expected_success: bool = True

class ComprehensiveMCPTestSuite:
    """Comprehensive MCP test suite with real-world scenarios."""
    
    def __init__(self):
        self.test_results = []
        self.server_process = None
        self.test_scenarios = self._create_test_scenarios()
        
    def _create_test_scenarios(self) -> List[TestScenario]:
        """Create comprehensive test scenarios across multiple industries."""
        return [
            # TECHNOLOGY INDUSTRY - Diverse scenarios
            TestScenario(
                name="Latest AI News",
                industry="Technology",
                description="Get latest AI news from TechCrunch",
                tool_name="rival_retrieve",
                arguments={"resource": "https://techcrunch.com/tag/artificial-intelligence/", "limit": 1, "max_length": 400}
            ),
            TestScenario(
                name="Quantum Computing Search",
                industry="Technology",
                description="Search for quantum computing developments",
                tool_name="google_search",
                arguments={"query": "quantum computing breakthroughs 2025", "max_results": 2}
            ),
            TestScenario(
                name="React Documentation",
                industry="Technology",
                description="Explore React documentation",
                tool_name="explore_docs",
                arguments={"url": "https://react.dev/", "max_pages": 1}
            ),
            
            # FINANCE INDUSTRY - Different sources
            TestScenario(
                name="Crypto Market News",
                industry="Finance",
                description="Get cryptocurrency market updates",
                tool_name="rival_retrieve",
                arguments={"resource": "https://cointelegraph.com/", "limit": 1, "max_length": 300}
            ),
            TestScenario(
                name="ESG Investment Trends",
                industry="Finance",
                description="Search for ESG investment trends",
                tool_name="google_search",
                arguments={"query": "ESG sustainable investing trends 2025", "max_results": 2}
            ),
            TestScenario(
                name="Crypto Research Data",
                industry="Finance",
                description="Store cryptocurrency research",
                tool_name="add_nodes",
                arguments={"nodes": [{"name": "Crypto_Analysis_2025", "type": "cryptocurrency", "facts": ["Bitcoin adoption is increasing", "DeFi protocols are growing"]}]}
            ),
            
            # HEALTHCARE INDUSTRY - New focus areas
            TestScenario(
                name="Mental Health Research",
                industry="Healthcare",
                description="Research mental health developments",
                tool_name="rival_retrieve",
                arguments={"resource": "https://www.psychiatry.org/newsroom", "limit": 1, "max_length": 400}
            ),
            TestScenario(
                name="Gene Therapy Search",
                industry="Healthcare",
                description="Search for gene therapy advances",
                tool_name="google_search",
                arguments={"query": "gene therapy clinical trials 2025", "max_results": 2}
            ),
            TestScenario(
                name="Mental Health Data",
                industry="Healthcare",
                description="Store mental health research",
                tool_name="add_nodes",
                arguments={"nodes": [{"name": "Mental_Health_Research", "type": "psychiatry", "facts": ["Digital therapy is expanding", "AI diagnostics are improving"]}]}
            ),
            
            # E-COMMERCE INDUSTRY - Emerging trends
            TestScenario(
                name="Social Commerce News",
                industry="E-commerce",
                description="Research social commerce trends",
                tool_name="rival_retrieve",
                arguments={"resource": "https://www.digitalcommerce360.com/", "limit": 1, "max_length": 300}
            ),
            TestScenario(
                name="AR Shopping Search",
                industry="E-commerce",
                description="Search for AR shopping technology",
                tool_name="google_search",
                arguments={"query": "augmented reality shopping experiences 2025", "max_results": 2}
            ),
            TestScenario(
                name="Social Commerce Data",
                industry="E-commerce",
                description="Store social commerce insights",
                tool_name="add_nodes",
                arguments={"nodes": [{"name": "Social_Commerce_2025", "type": "ecommerce", "facts": ["Social shopping is growing", "Live streaming sales are popular"]}]}
            ),
            
            # EDUCATION INDUSTRY - Modern learning
            TestScenario(
                name="EdTech Innovations",
                industry="Education",
                description="Research educational technology innovations",
                tool_name="rival_retrieve",
                arguments={"resource": "https://www.edsurge.com/", "limit": 1, "max_length": 350}
            ),
            TestScenario(
                name="VR Education Search",
                industry="Education",
                description="Search for VR in education",
                tool_name="google_search",
                arguments={"query": "virtual reality education applications 2025", "max_results": 2}
            ),
            TestScenario(
                name="EdTech Research Data",
                industry="Education",
                description="Store EdTech research",
                tool_name="add_nodes",
                arguments={"nodes": [{"name": "EdTech_Innovations", "type": "education", "facts": ["VR classrooms are emerging", "Personalized learning is key"]}]}
            ),
            
            # MANUFACTURING INDUSTRY - Advanced manufacturing
            TestScenario(
                name="3D Printing News",
                industry="Manufacturing",
                description="Research 3D printing developments",
                tool_name="rival_retrieve",
                arguments={"resource": "https://3dprint.com/", "limit": 1, "max_length": 300}
            ),
            TestScenario(
                name="Robotics Manufacturing",
                industry="Manufacturing",
                description="Search for robotics in manufacturing",
                tool_name="google_search",
                arguments={"query": "industrial robotics manufacturing automation 2025", "max_results": 2}
            ),
            TestScenario(
                name="3D Printing Data",
                industry="Manufacturing",
                description="Store 3D printing insights",
                tool_name="add_nodes",
                arguments={"nodes": [{"name": "3D_Printing_Trends", "type": "manufacturing", "facts": ["Metal 3D printing is growing", "Mass customization is possible"]}]}
            ),
            
            # REAL ESTATE INDUSTRY - Proptech focus
            TestScenario(
                name="Proptech News",
                industry="Real Estate",
                description="Research property technology news",
                tool_name="rival_retrieve",
                arguments={"resource": "https://www.proptechinsight.com/", "limit": 1, "max_length": 300}
            ),
            TestScenario(
                name="Smart Home Search",
                industry="Real Estate",
                description="Search for smart home technology",
                tool_name="google_search",
                arguments={"query": "smart home real estate technology 2025", "max_results": 2}
            ),
            TestScenario(
                name="Proptech Data",
                industry="Real Estate",
                description="Store proptech insights",
                tool_name="add_nodes",
                arguments={"nodes": [{"name": "Proptech_Trends", "type": "real_estate", "facts": ["Smart homes are in demand", "Virtual tours are standard"]}]}
            ),
            
            # TRAVEL INDUSTRY - Sustainable travel
            TestScenario(
                name="Sustainable Travel News",
                industry="Travel",
                description="Research sustainable travel trends",
                tool_name="rival_retrieve",
                arguments={"resource": "https://www.nationalgeographic.com/travel/", "limit": 1, "max_length": 300}
            ),
            TestScenario(
                name="Eco Tourism Search",
                industry="Travel",
                description="Search for eco-tourism trends",
                tool_name="google_search",
                arguments={"query": "eco tourism sustainable travel 2025", "max_results": 2}
            ),
            TestScenario(
                name="Sustainable Travel Data",
                industry="Travel",
                description="Store sustainable travel insights",
                tool_name="add_nodes",
                arguments={"nodes": [{"name": "Sustainable_Travel", "type": "travel", "facts": ["Eco-tourism is growing", "Carbon offsetting is popular"]}]}
            ),
            
            # MEDIA & ENTERTAINMENT - New media
            TestScenario(
                name="Podcast Industry News",
                industry="Media & Entertainment",
                description="Research podcast industry developments",
                tool_name="rival_retrieve",
                arguments={"resource": "https://www.podcastinsights.com/", "limit": 1, "max_length": 300}
            ),
            TestScenario(
                name="Metaverse Entertainment",
                industry="Media & Entertainment",
                description="Search for metaverse entertainment",
                tool_name="google_search",
                arguments={"query": "metaverse entertainment virtual worlds 2025", "max_results": 2}
            ),
            TestScenario(
                name="Podcast Industry Data",
                industry="Media & Entertainment",
                description="Store podcast industry insights",
                tool_name="add_nodes",
                arguments={"nodes": [{"name": "Podcast_Industry", "type": "media", "facts": ["Podcast advertising is growing", "Interactive podcasts are emerging"]}]}
            ),
            
            # AGRICULTURE INDUSTRY - Smart farming
            TestScenario(
                name="Vertical Farming News",
                industry="Agriculture",
                description="Research vertical farming developments",
                tool_name="rival_retrieve",
                arguments={"resource": "https://www.verticalfarmdaily.com/", "limit": 1, "max_length": 300}
            ),
            TestScenario(
                name="Drone Farming Search",
                industry="Agriculture",
                description="Search for drone technology in farming",
                tool_name="google_search",
                arguments={"query": "agricultural drones farming technology 2025", "max_results": 2}
            ),
            TestScenario(
                name="Vertical Farming Data",
                industry="Agriculture",
                description="Store vertical farming insights",
                tool_name="add_nodes",
                arguments={"nodes": [{"name": "Vertical_Farming", "type": "agriculture", "facts": ["Urban farming is growing", "LED lighting is efficient"]}]}
            )
        ]
    
    def start_server(self):
        """Start the custom MCP server."""
        print("🚀 Starting Custom MCP Server...")
        cmd = [sys.executable, "src/mcp_server.py"]
        self.server_process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(2)  # Wait for server to start
        print("✅ Server started successfully")
    
    def stop_server(self):
        """Stop the MCP server."""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            print("🛑 Server stopped")
    
    def send_mcp_request(self, request: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
        """Send MCP request and get response with timeout."""
        if not self.server_process or not self.server_process.stdin or not self.server_process.stdout:
            raise Exception("Server not running or pipes not available")
        
        request_str = json.dumps(request) + "\n"
        self.server_process.stdin.write(request_str)
        self.server_process.stdin.flush()
        
        # Set up timeout for reading response
        import select
        ready, _, _ = select.select([self.server_process.stdout], [], [], timeout)
        
        if ready:
            response_line = self.server_process.stdout.readline()
            if response_line:
                return json.loads(response_line.strip())
            else:
                raise Exception("No response from server")
        else:
            raise Exception(f"Request timed out after {timeout} seconds")
    
    def initialize_server(self):
        """Initialize the MCP server."""
        print("🔧 Initializing MCP Server...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "comprehensive-test-suite",
                    "version": "1.0.0"
                }
            }
        }
        
        response = self.send_mcp_request(init_request)
        if "result" in response:
            print("✅ Server initialized successfully")
            return True
        else:
            print(f"❌ Server initialization failed: {response}")
            return False
    
    def list_tools(self):
        """List available tools."""
        print("🛠️ Listing available tools...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = self.send_mcp_request(tools_request)
        if "result" in response:
            tools = response["result"].get("tools", [])
            print(f"✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool.get('name', 'unknown')}: {tool.get('description', 'No description')}")
            return tools
        else:
            print(f"❌ Failed to list tools: {response}")
            return []
    
    def test_scenario(self, scenario: TestScenario, tools: List[Dict]) -> Dict[str, Any]:
        """Test a specific scenario."""
        print(f"\n🎯 Testing Scenario: {scenario.name}")
        print(f"   Industry: {scenario.industry}")
        print(f"   Description: {scenario.description}")
        print(f"   Tool: {scenario.tool_name}")
        
        # Check if tool exists
        tool_exists = any(tool.get('name') == scenario.tool_name for tool in tools)
        if not tool_exists:
            result = {
                "scenario": scenario.name,
                "industry": scenario.industry,
                "tool": scenario.tool_name,
                "status": "SKIPPED",
                "reason": "Tool not available",
                "success": False
            }
            print(f"   ⚠️ Tool {scenario.tool_name} not available, skipping")
            return result
        
        try:
            # Call the tool with timeout
            call_request = {
                "jsonrpc": "2.0",
                "id": len(self.test_results) + 3,
                "method": "tools/call",
                "params": {
                    "name": scenario.tool_name,
                    "arguments": scenario.arguments
                }
            }
            
            # Use longer timeouts to allow tools to complete
            timeout = 60 if scenario.tool_name == "explore_docs" else 45
            response = self.send_mcp_request(call_request, timeout)
            
            if "result" in response:
                # Show actual data being pulled
                result_data = response["result"]
                print(f"   ✅ Success: Tool executed successfully")
                
                # Display sample of the data
                if isinstance(result_data, dict):
                    if "content" in result_data:
                        content = result_data["content"]
                        if isinstance(content, list) and content:
                            sample = str(content[0])[:200] + "..." if len(str(content[0])) > 200 else str(content[0])
                            print(f"   📄 Data sample: {sample}")
                    elif "results" in result_data:
                        results = result_data["results"]
                        if isinstance(results, list) and results:
                            sample = str(results[0])[:200] + "..." if len(str(results[0])) > 200 else str(results[0])
                            print(f"   🔍 Results sample: {sample}")
                    else:
                        print(f"   📊 Response: {str(result_data)[:200]}...")
                else:
                    print(f"   📊 Response: {str(result_data)[:200]}...")
                
                result = {
                    "scenario": scenario.name,
                    "industry": scenario.industry,
                    "tool": scenario.tool_name,
                    "status": "SUCCESS",
                    "response": result_data,
                    "success": True
                }
            else:
                result = {
                    "scenario": scenario.name,
                    "industry": scenario.industry,
                    "tool": scenario.tool_name,
                    "status": "ERROR",
                    "error": response.get("error", "Unknown error"),
                    "success": False
                }
                print(f"   ❌ Error: {response.get('error', 'Unknown error')}")
                
        except Exception as e:
            result = {
                "scenario": scenario.name,
                "industry": scenario.industry,
                "tool": scenario.tool_name,
                "status": "EXCEPTION",
                "error": str(e),
                "success": False
            }
            print(f"   💥 Exception: {e}")
        
        return result
    
    def run_comprehensive_tests(self):
        """Run comprehensive test suite."""
        print("🎯 COMPREHENSIVE MCP TEST SUITE")
        print("=" * 60)
        print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Total scenarios: {len(self.test_scenarios)}")
        print(f"🏭 Industries covered: {len(set(s.industry for s in self.test_scenarios))}")
        print("=" * 60)
        
        try:
            # Start server
            self.start_server()
            
            # Initialize server
            if not self.initialize_server():
                print("❌ Failed to initialize server, aborting tests")
                return
            
            # List tools
            tools = self.list_tools()
            if not tools:
                print("❌ No tools available, aborting tests")
                return
            
            # Test each scenario
            print(f"\n🚀 Starting {len(self.test_scenarios)} test scenarios...")
            
            for i, scenario in enumerate(self.test_scenarios, 1):
                print(f"\n📋 Scenario {i}/{len(self.test_scenarios)}")
                result = self.test_scenario(scenario, tools)
                self.test_results.append(result)
                
                # Small delay between tests
                time.sleep(0.5)
            
            # Generate comprehensive report
            self.generate_report()
            
        except Exception as e:
            print(f"💥 Test suite failed with exception: {e}")
        finally:
            self.stop_server()
    
    def generate_report(self):
        """Generate comprehensive test report."""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # Overall statistics
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - successful_tests
        
        print(f"📈 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {successful_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        # Industry breakdown
        print(f"\n🏭 Results by Industry:")
        industry_stats = {}
        for result in self.test_results:
            industry = result["industry"]
            if industry not in industry_stats:
                industry_stats[industry] = {"total": 0, "success": 0}
            industry_stats[industry]["total"] += 1
            if result["success"]:
                industry_stats[industry]["success"] += 1
        
        for industry, stats in industry_stats.items():
            success_rate = (stats["success"]/stats["total"])*100
            print(f"   {industry}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # Tool breakdown
        print(f"\n🛠️ Results by Tool:")
        tool_stats = {}
        for result in self.test_results:
            tool = result["tool"]
            if tool not in tool_stats:
                tool_stats[tool] = {"total": 0, "success": 0}
            tool_stats[tool]["total"] += 1
            if result["success"]:
                tool_stats[tool]["success"] += 1
        
        for tool, stats in tool_stats.items():
            success_rate = (stats["success"]/stats["total"])*100
            print(f"   {tool}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # Detailed results
        print(f"\n📋 Detailed Results:")
        for result in self.test_results:
            status_icon = "✅" if result["success"] else "❌"
            print(f"   {status_icon} {result['industry']} - {result['scenario']} ({result['tool']})")
            if not result["success"]:
                print(f"      Error: {result.get('error', 'Unknown error')}")
        
        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (successful_tests/total_tests)*100
            },
            "industry_stats": industry_stats,
            "tool_stats": tool_stats,
            "detailed_results": self.test_results
        }
        
        # Save report in tests directory
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        report_filename = f"comprehensive_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(tests_dir, report_filename)
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: {report_path}")
        print("=" * 60)
        
        if successful_tests == total_tests:
            print("🎉 ALL TESTS PASSED! MCP Server is fully functional across all industries!")
        else:
            print(f"⚠️ {failed_tests} tests failed. Review the detailed results above.")

def main():
    """Main entry point."""
    test_suite = ComprehensiveMCPTestSuite()
    test_suite.run_comprehensive_tests()

if __name__ == "__main__":
    main()
