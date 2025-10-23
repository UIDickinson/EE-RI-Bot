import requests
import arxiv
from typing import List, Dict, Any
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)


class ResearchTools:
    def __init__(self):
        self.apis = {
            "ieee": os.getenv("IEEE_API_KEY"),
            "google_patents": os.getenv("GOOGLE_PATENTS_KEY")
        }
        
        self.priority_institutions = [
            "ETH Zurich", "TU Munich", "IMEC", "Fraunhofer",
            "Tsinghua", "KAIST", "Tokyo Tech", "IIT", "NUS", "TSMC"
        ]
    
    def search_research_papers(
        self,
        query: str,
        domain: str = "general",
        date_range: str = None,
        include_patents: bool = True
    ) -> Dict[str, Any]:
        results = {
            "papers": [],
            "patents": [],
            "top_sources": [],
            "metadata": {
                "query": query,
                "domain": domain,
                "search_date": datetime.now().isoformat()
            }
        }
        
        domain_keywords = {
            "power_management": "power management OR PMIC OR DC-DC OR buck OR boost",
            "emc_emi": "EMC OR EMI OR electromagnetic compatibility",
            "edge_ai": "edge AI OR neural processing OR AI accelerator",
            "embedded_systems": "embedded OR microcontroller OR MCU OR RTOS"
        }
        
        enhanced_query = query
        if domain != "general" and domain in domain_keywords:
            enhanced_query = f"{query} AND ({domain_keywords[domain]})"
        
        arxiv_papers = self._search_arxiv(enhanced_query, date_range)
        results["papers"].extend(arxiv_papers)
        if arxiv_papers:
            results["top_sources"].append("arXiv")
        
        semantic_papers = self._search_semantic_scholar(enhanced_query, date_range)
        results["papers"].extend(semantic_papers)
        if semantic_papers:
            results["top_sources"].append("Semantic Scholar")
        
        return results
    
    def _search_arxiv(self, query: str, date_range: str) -> List[Dict]:
        try:
            search = arxiv.Search(
                query=query,
                max_results=30,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            papers = []
            for result in search.results():
                if date_range:
                    pub_year = result.published.year
                    start_year, end_year = map(int, date_range.split("-"))
                    if not (start_year <= pub_year <= end_year):
                        continue
                
                papers.append({
                    "title": result.title,
                    "authors": [author.name for author in result.authors],
                    "abstract": result.summary,
                    "year": str(result.published.year),
                    "url": result.entry_id,
                    "source": "arXiv"
                })
            
            logger.info(f"Found {len(papers)} papers on arXiv")
            return papers
        except Exception as e:
            logger.error(f"arXiv error: {e}")
            return []
    
    def _search_semantic_scholar(self, query: str, date_range: str) -> List[Dict]:
        try:
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": query,
                "limit": 30,
                "fields": "title,authors,abstract,year,venue,openAccessPdf"
            }
            
            if date_range:
                start_year, end_year = date_range.split("-")
                params["year"] = f"{start_year}-{end_year}"
            
            response = requests.get(url, params=params, timeout=15)
            data = response.json()
            
            papers = []
            for paper in data.get("data", []):
                papers.append({
                    "title": paper.get("title", ""),
                    "authors": [a.get("name") for a in paper.get("authors", [])],
                    "abstract": paper.get("abstract", ""),
                    "year": str(paper.get("year", "")),
                    "source": "Semantic Scholar"
                })
            
            logger.info(f"Found {len(papers)} papers on Semantic Scholar")
            return papers
        except Exception as e:
            logger.error(f"Semantic Scholar error: {e}")
            return []
