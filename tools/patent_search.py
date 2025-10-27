"""
Patent Search using PatentsView API with Authentication
"""

import requests
import logging
from typing import Dict, List, Any
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class PatentSearcher:
    def __init__(self):
        self.api_key = os.getenv("PATENTSVIEW_API_KEY")
        self.base_url = "https://search.patentsview.org/api/v1/patent"
        
        if self.api_key:
            logger.info("PatentsView API key configured")
        else:
            logger.warning("PATENTSVIEW_API_KEY not set - using placeholder mode")
    
    def search_patents(
        self,
        query: str,
        country_codes: List[str] = ["US"],
        date_from: str = "2020-01-01",
        max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Search patents using PatentsView API with authentication
        
        API Documentation: https://search.patentsview.org/docs/docs.html
        """
        results = {
            "patents": [],
            "total_found": 0,
            "search_date": datetime.now().isoformat(),
            "query": query,
            "source": "PatentsView"
        }
        
        if not self.api_key:
            logger.warning("No API key - returning placeholder data")
            return self._placeholder_results(query)
        
        try:
            # PatentsView API query structure
            search_query = {
                "q": {
                    "_text_any": {
                        "patent_abstract": query
                    }
                },
                "f": [
                    "patent_number",
                    "patent_title", 
                    "patent_date",
                    "patent_abstract",
                    "assignee_organization"
                ],
                "o": {
                    "page": 1,
                    "per_page": min(max_results, 100)
                }
            }
            
            # Add date filter if specified
            if date_from:
                search_query["q"]["_gte"] = {
                    "patent_date": date_from
                }
            
            headers = {
                "X-Api-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.base_url,
                json=search_query,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                patents_data = data.get("patents", [])
                
                for patent in patents_data:
                    # Extract assignee organization
                    assignees = patent.get("assignees", [])
                    assignee_name = "Unknown"
                    if assignees and len(assignees) > 0:
                        assignee_name = assignees[0].get("assignee_organization", "Unknown")
                    
                    results["patents"].append({
                        "patent_id": patent.get("patent_number"),
                        "title": patent.get("patent_title"),
                        "abstract": patent.get("patent_abstract", "")[:500],
                        "filing_date": patent.get("patent_date"),
                        "assignee": assignee_name,
                        "source": "PatentsView (Authenticated)"
                    })
                
                results["total_found"] = data.get("count", len(results["patents"]))
                logger.info(f"Found {results['total_found']} patents via PatentsView API")
            
            elif response.status_code == 401:
                logger.error("PatentsView API authentication failed - invalid API key")
                results["error"] = "Invalid API key"
                return self._placeholder_results(query)
            
            elif response.status_code == 429:
                logger.warning("PatentsView API rate limit exceeded")
                results["error"] = "Rate limit exceeded"
                return self._placeholder_results(query)
            
            else:
                logger.warning(f"PatentsView API returned status {response.status_code}")
                results["error"] = f"API error: {response.status_code}"
        
        except requests.exceptions.Timeout:
            logger.error("PatentsView API request timeout")
            results["error"] = "Request timeout"
            return self._placeholder_results(query)
        
        except Exception as e:
            logger.error(f"Patent search error: {e}")
            results["error"] = str(e)
            return self._placeholder_results(query)
        
        return results
    
    def _placeholder_results(self, query: str) -> Dict[str, Any]:
        """
        Return placeholder results when API is unavailable
        """
        return {
            "patents": [
                {
                    "patent_id": "US-PLACEHOLDER-001",
                    "title": f"Advanced Technology Related to {query}",
                    "abstract": f"This patent describes innovations in {query} with applications in electrical engineering, power management, and embedded systems. The technology improves efficiency by 15-25% compared to existing solutions.",
                    "filing_date": "2023-06-15",
                    "assignee": "Technology Corporation",
                    "source": "Placeholder (API unavailable)"
                },
                {
                    "patent_id": "US-PLACEHOLDER-002",
                    "title": f"Novel Approach to {query} Implementation",
                    "abstract": f"A method and apparatus for implementing {query} in resource-constrained environments. Includes circuit diagrams and performance benchmarks.",
                    "filing_date": "2023-09-20",
                    "assignee": "Innovation Labs",
                    "source": "Placeholder (API unavailable)"
                }
            ],
            "total_found": 2,
            "search_date": datetime.now().isoformat(),
            "query": query,
            "source": "Placeholder",
            "note": "PatentsView API unavailable - showing placeholder data"
        }
    
    def search_by_assignee(
        self,
        assignee: str,
        date_from: str = "2020-01-01",
        max_results: int = 25
    ) -> Dict[str, Any]:
        """
        Search patents by company/assignee name
        """
        if not self.api_key:
            logger.warning("No API key for assignee search")
            return {"patents": [], "total_found": 0}
        
        try:
            search_query = {
                "q": {
                    "_and": [
                        {
                            "_text_any": {
                                "assignee_organization": assignee
                            }
                        },
                        {
                            "_gte": {
                                "patent_date": date_from
                            }
                        }
                    ]
                },
                "f": [
                    "patent_number",
                    "patent_title",
                    "patent_date",
                    "patent_abstract",
                    "assignee_organization"
                ],
                "o": {
                    "page": 1,
                    "per_page": max_results
                }
            }
            
            headers = {
                "X-Api-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.base_url,
                json=search_query,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                patents = data.get("patents", [])
                
                return {
                    "patents": patents,
                    "total_found": data.get("count", len(patents)),
                    "assignee": assignee
                }
        
        except Exception as e:
            logger.error(f"Assignee search error: {e}")
        
        return {"patents": [], "total_found": 0}
    
    def get_patent_details(self, patent_number: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific patent
        """
        if not self.api_key:
            logger.warning("No API key for patent details")
            return {}
        
        try:
            search_query = {
                "q": {
                    "patent_number": patent_number
                },
                "f": [
                    "patent_number",
                    "patent_title",
                    "patent_date",
                    "patent_abstract",
                    "assignee_organization",
                    "inventor_first_name",
                    "inventor_last_name",
                    "cpc_section_id",
                    "cpc_subgroup_title"
                ]
            }
            
            headers = {
                "X-Api-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.base_url,
                json=search_query,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                patents = data.get("patents", [])
                
                if patents:
                    return patents[0]
        
        except Exception as e:
            logger.error(f"Error fetching patent details: {e}")
        
        return {}
    
    def analyze_patent_trends(
        self,
        patents: List[Dict],
        domain: str
    ) -> Dict[str, Any]:
        """
        Analyze patent trends for a domain
        """
        if not patents:
            return {"total_patents": 0}
        
        analysis = {
            "total_patents": len(patents),
            "top_assignees": {},
            "filing_trend": {}
        }
        
        # Count patents by assignee
        for patent in patents:
            assignee = patent.get("assignee", "Unknown")
            if assignee and assignee != "Unknown":
                analysis["top_assignees"][assignee] = analysis["top_assignees"].get(assignee, 0) + 1
            
            # Group by year
            filing_date = patent.get("filing_date", "")
            if filing_date and filing_date != "Unknown":
                try:
                    year = filing_date[:4]
                    if year.isdigit():
                        analysis["filing_trend"][year] = analysis["filing_trend"].get(year, 0) + 1
                except:
                    pass
        
        # Sort top assignees
        analysis["top_assignees"] = dict(
            sorted(analysis["top_assignees"].items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        return analysis
    
    def search_by_cpc_code(
        self,
        cpc_code: str,
        date_from: str = "2020-01-01",
        max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Search patents by CPC (Cooperative Patent Classification) code
        
        Example CPC codes for EE:
        - H01L: Semiconductor devices
        - H02M: Power conversion
        - H03K: Pulse technique
        - G06N: Neural networks
        """
        if not self.api_key:
            return {"patents": [], "total_found": 0}
        
        try:
            search_query = {
                "q": {
                    "_and": [
                        {
                            "cpc_section_id": cpc_code
                        },
                        {
                            "_gte": {
                                "patent_date": date_from
                            }
                        }
                    ]
                },
                "f": [
                    "patent_number",
                    "patent_title",
                    "patent_date",
                    "patent_abstract",
                    "assignee_organization",
                    "cpc_section_id"
                ],
                "o": {
                    "page": 1,
                    "per_page": max_results
                }
            }
            
            headers = {
                "X-Api-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.base_url,
                json=search_query,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "patents": data.get("patents", []),
                    "total_found": data.get("count", 0),
                    "cpc_code": cpc_code
                }
        
        except Exception as e:
            logger.error(f"CPC search error: {e}")
        
        return {"patents": [], "total_found": 0}