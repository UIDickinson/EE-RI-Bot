"""
EE Research & Innovation Scout Agent - Multi-Provider Support with Web Interface
Supports: OpenAI, Claude (Anthropic), OpenRouter
"""

import logging
import os
from dotenv import load_dotenv
from sentient_agent_framework import (
    AbstractAgent,
    DefaultServer,
    Session,
    Query,
    ResponseHandler
)
from typing import AsyncIterator, Dict, List, Any
import json
from pathlib import Path

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LLMProvider:
    """Universal LLM provider supporting OpenAI, Claude, and OpenRouter"""
    
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "anthropic")
        self.api_key = self._get_api_key()
        self.model = self._get_model()
        self.client = self._initialize_client()
    
    def _get_api_key(self) -> str:
        if self.provider == "anthropic":
            key = os.getenv("ANTHROPIC_API_KEY")
        elif self.provider == "openai":
            key = os.getenv("OPENAI_API_KEY")
        elif self.provider == "openrouter":
            key = os.getenv("OPENROUTER_API_KEY")
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
        
        if not key:
            raise ValueError(f"{self.provider.upper()}_API_KEY not set")
        
        return key
    
    def _get_model(self) -> str:
        if self.provider == "anthropic":
            return os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
        elif self.provider == "openai":
            return os.getenv("OPENAI_MODEL", "gpt-4o")
        elif self.provider == "openrouter":
            return os.getenv("OPENROUTER_MODEL", "anthropic/claude-sonnet-4.5")
        return ""
    
    def _initialize_client(self):
        if self.provider == "anthropic":
            from anthropic import Anthropic
            return Anthropic(api_key=self.api_key)
        
        elif self.provider == "openai":
            from openai import OpenAI
            return OpenAI(api_key=self.api_key)
        
        elif self.provider == "openrouter":
            from openai import OpenAI
            return OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
    
    def create_completion(self, messages: List[Dict], max_tokens: int = 1024) -> str:
        """Non-streaming completion"""
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=messages
            )
            return response.content[0].text
        
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
    
    def stream_completion(self, messages: List[Dict], max_tokens: int = 16000):
        """Streaming completion"""
        if self.provider == "anthropic":
            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    yield text
        
        else:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content


class EEResearchScout(AbstractAgent):
    """EE Research & Innovation Scout Agent"""
    
    def __init__(self, name: str):
        super().__init__(name)
        
        self.llm = LLMProvider()
        logger.info(f"Using {self.llm.provider} with model {self.llm.model}")
        
        self.domain_priorities = {
            "embedded_systems": 1.0,
            "power_management": 0.9,
            "emc_emi": 0.9,
            "edge_ai": 0.85,
            "analog_design": 0.7,
            "rf_wireless": 0.6,
            "digital_systems": 0.6
        }
        
        from tools.research_tools import ResearchTools
        from tools.component_tools import ComponentAnalyzer
        from tools.supply_chain import SupplyChainTracker
        
        self.research_tools = ResearchTools()
        self.component_analyzer = ComponentAnalyzer()
        self.supply_chain = SupplyChainTracker()
        self.knowledge_graph = None
    
    async def assist(
        self,
        session: Session,
        query: Query,
        response_handler: ResponseHandler
    ):
        try:
            user_query = query.prompt
            logger.info(f"Query: {user_query}")
            
            await response_handler.emit_text_block(
                "ANALYSIS", 
                "🔍 Analyzing query and identifying EE domains..."
            )
            
            query_analysis = await self._analyze_query(user_query)
            
            await response_handler.emit_json(
                "QUERY_ANALYSIS",
                {
                    "domains": query_analysis["domains"],
                    "strategy": query_analysis["strategy"],
                    "geographic_focus": ["EU", "Asia"]
                }
            )
            
            await response_handler.emit_text_block(
                "RESEARCH", 
                "📚 Searching academic papers and patents..."
            )
            
            research_results = await self._search_research(
                user_query,
                query_analysis["domains"]
            )
            
            if research_results.get("papers"):
                await response_handler.emit_json(
                    "SOURCES",
                    {
                        "papers_found": len(research_results.get("papers", [])),
                        "top_sources": research_results.get("top_sources", [])
                    }
                )
            
            if query_analysis.get("components"):
                await response_handler.emit_text_block(
                    "COMPONENT_ANALYSIS",
                    "🔬 Analyzing component specifications..."
                )
                
                component_data = await self._analyze_components(
                    query_analysis["components"]
                )
                
                await response_handler.emit_json(
                    "COMPONENTS",
                    component_data
                )
            
            if "availability" in user_query.lower() or "supply" in user_query.lower():
                await response_handler.emit_text_block(
                    "SUPPLY_CHAIN",
                    "📦 Checking supply chain status..."
                )
                
                supply_data = self.supply_chain.check_availability(
                    query_analysis.get("components", []),
                    region="both"
                )
                
                await response_handler.emit_json(
                    "SUPPLY_STATUS",
                    supply_data
                )
            
            await response_handler.emit_text_block(
                "GENERATING",
                "✍️ Generating comprehensive technical analysis..."
            )
            
            final_stream = response_handler.create_text_stream("FINAL_RESPONSE")
            
            async for chunk in self._generate_analysis(
                user_query,
                query_analysis,
                research_results
            ):
                await final_stream.emit_chunk(chunk)
            
            await final_stream.complete()
            await response_handler.complete()
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await response_handler.emit_error(
                "ERROR",
                {"message": str(e)}
            )
            await response_handler.complete()
    
    async def _analyze_query(self, user_query: str) -> Dict[str, Any]:
        prompt = f"""Analyze this EE query and extract:
1. Relevant domains (embedded_systems, power_management, emc_emi, edge_ai, analog_design, rf_wireless)
2. Specific components mentioned
3. Strategy (innovation_search, component_comparison, implementation_guide)

Query: {user_query}

Return JSON:
{{
    "domains": ["domain1"],
    "components": ["component1"],
    "strategy": "innovation_search",
    "geographic_focus": ["EU", "Asia"]
}}"""
        
        messages = [{"role": "user", "content": prompt}]
        response = self.llm.create_completion(messages, max_tokens=1024)
        
        try:
            return json.loads(response)
        except:
            return {
                "domains": ["general"],
                "components": [],
                "strategy": "innovation_search",
                "geographic_focus": ["EU", "Asia"]
            }
    
    async def _search_research(self, query: str, domains: List[str]) -> Dict:
        return self.research_tools.search_research_papers(
            query=query,
            domain=domains[0] if domains else "general",
            date_range="2023-2025",
            include_patents=True
        )
    
    async def _analyze_components(self, components: List[str]) -> Dict:
        analyses = {}
        for component in components[:3]:
            analysis = self.component_analyzer.analyze_component(
                component_id=component,
                analysis_depth="deep_dive"
            )
            analyses[component] = analysis
        return analyses
    
    async def _generate_analysis(
        self,
        user_query: str,
        query_analysis: Dict,
        research_results: Dict
    ) -> AsyncIterator[str]:
        
        papers_context = ""
        if research_results.get("papers"):
            papers_context = "\n\n".join([
                f"- {p['title']} ({p['year']}) - {p.get('abstract', '')[:200]}..."
                for p in research_results["papers"][:10]
            ])
        
        prompt = f"""You are an expert EE Research Scout.

USER QUERY: {user_query}

DOMAINS: {', '.join(query_analysis.get('domains', []))}

RESEARCH CONTEXT:
{papers_context}

Provide comprehensive technical analysis covering:
1. Innovation Overview
2. Technical Deep-Dive (specs, performance, efficiency)
3. Component Analysis (if applicable)
4. Technology Maturity (TRL assessment)
5. Supply Chain (EU/Asia availability)
6. Implementation Guidance (CE, RoHS, CCC compliance)
7. Quantitative Comparisons

Requirements:
- Professional/academic depth
- Quantitative data
- EU/Asia market focus
- Embedded systems priority
- Performance improvements ≥15% for "breakthrough"

Provide detailed, structured analysis:"""
        
        messages = [{"role": "user", "content": prompt}]
        
        for chunk in self.llm.stream_completion(messages, max_tokens=16000):
            yield chunk


if __name__ == "__main__":
    agent = EEResearchScout(name="EE-Research-Scout")
    
    # Create static directory if it doesn't exist
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    
    server = DefaultServer(
        agent,
        static_dir=str(static_dir)
    )
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting EE Research Scout Agent")
    logger.info(f"Web Interface: http://localhost:{port}")
    logger.info(f"API Endpoint: http://localhost:{port}/assist")
    
    server.run(host=host, port=port)