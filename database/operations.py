"""
Database operations and queries
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy import func, desc, and_, or_
from database.models import (
    ResearchPaper, Component, QueryHistory, 
    SupplyChain, ComplianceStandard, CachedResponse
)
from database.connection import db_manager
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class DatabaseOperations:
    """High-level database operations"""
    
    # ==================== Research Papers ====================
    
    @staticmethod
    def add_research_paper(paper_data: Dict) -> Optional[ResearchPaper]:
        """Add a research paper to database"""
        with db_manager.get_session() as session:
            try:
                # Check if paper already exists (by DOI or URL)
                existing = None
                if paper_data.get('doi'):
                    existing = session.query(ResearchPaper).filter_by(
                        doi=paper_data['doi']
                    ).first()
                
                if existing:
                    logger.info(f"Paper already exists: {existing.title}")
                    return existing
                
                paper = ResearchPaper(
                    title=paper_data.get('title'),
                    authors=paper_data.get('authors', []),
                    abstract=paper_data.get('abstract'),
                    year=paper_data.get('year'),
                    source=paper_data.get('source'),
                    url=paper_data.get('url'),
                    doi=paper_data.get('doi'),
                    domains=paper_data.get('domains', []),
                    keywords=paper_data.get('keywords', []),
                    citation_count=paper_data.get('citation_count', 0)
                )
                
                session.add(paper)
                session.flush()
                logger.info(f"Added paper: {paper.title}")
                return paper
            
            except Exception as e:
                logger.error(f"Error adding paper: {e}")
                return None
    
    @staticmethod
    def search_papers(
        query: str,
        domains: List[str] = None,
        min_year: int = None,
        limit: int = 50
    ) -> List[ResearchPaper]:
        """Search for papers in database"""
        with db_manager.get_session() as session:
            q = session.query(ResearchPaper)
            
            if query:
                q = q.filter(
                    or_(
                        ResearchPaper.title.ilike(f"%{query}%"),
                        ResearchPaper.abstract.ilike(f"%{query}%")
                    )
                )
            
            if domains:
                # PostgreSQL JSON array contains
                q = q.filter(ResearchPaper.domains.contains(domains))
            
            if min_year:
                q = q.filter(ResearchPaper.year >= min_year)
            
            papers = q.order_by(desc(ResearchPaper.year)).limit(limit).all()
            return papers
    
    # ==================== Components ====================
    
    @staticmethod
    def add_component(component_data: Dict) -> Optional[Component]:
        """Add a component to database"""
        with db_manager.get_session() as session:
            try:
                # Check if exists
                existing = session.query(Component).filter_by(
                    part_number=component_data['part_number']
                ).first()
                
                if existing:
                    # Update existing
                    for key, value in component_data.items():
                        setattr(existing, key, value)
                    existing.updated_at = datetime.utcnow()
                    logger.info(f"Updated component: {existing.part_number}")
                    return existing
                
                component = Component(**component_data)
                session.add(component)
                session.flush()
                logger.info(f"Added component: {component.part_number}")
                return component
            
            except Exception as e:
                logger.error(f"Error adding component: {e}")
                return None
    
    @staticmethod
    def get_component(part_number: str) -> Optional[Component]:
        """Get component by part number"""
        with db_manager.get_session() as session:
            return session.query(Component).filter_by(
                part_number=part_number
            ).first()
    
    @staticmethod
    def search_components(
        query: str = None,
        category: str = None,
        manufacturer: str = None,
        limit: int = 50
    ) -> List[Component]:
        """Search for components"""
        with db_manager.get_session() as session:
            q = session.query(Component)
            
            if query:
                q = q.filter(Component.part_number.ilike(f"%{query}%"))
            
            if category:
                q = q.filter(Component.category == category)
            
            if manufacturer:
                q = q.filter(Component.manufacturer.ilike(f"%{manufacturer}%"))
            
            return q.limit(limit).all()
    
    # ==================== Query History ====================
    
    @staticmethod
    def log_query(query_data: Dict) -> Optional[QueryHistory]:
        """Log a user query"""
        with db_manager.get_session() as session:
            try:
                query_log = QueryHistory(**query_data)
                session.add(query_log)
                session.flush()
                return query_log
            except Exception as e:
                logger.error(f"Error logging query: {e}")
                return None
    
    @staticmethod
    def get_user_history(user_id: str, limit: int = 20) -> List[QueryHistory]:
        """Get user's query history"""
        with db_manager.get_session() as session:
            return session.query(QueryHistory).filter_by(
                user_id=user_id
            ).order_by(desc(QueryHistory.created_at)).limit(limit).all()
    
    # ==================== Caching ====================
    
    @staticmethod
    def get_cached_response(query: str) -> Optional[str]:
        """Get cached response for query"""
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        
        with db_manager.get_session() as session:
            cached = session.query(CachedResponse).filter(
                and_(
                    CachedResponse.query_hash == query_hash,
                    or_(
                        CachedResponse.expires_at.is_(None),
                        CachedResponse.expires_at > datetime.utcnow()
                    )
                )
            ).first()
            
            if cached:
                # Update hit count
                cached.hit_count += 1
                cached.last_accessed = datetime.utcnow()
                session.flush()
                logger.info(f"Cache hit for query (hits: {cached.hit_count})")
                return cached.response_text
            
            return None
    
    @staticmethod
    def cache_response(
        query: str,
        response: str,
        metadata: Dict = None,
        ttl_hours: int = 24
    ):
        """Cache a response"""
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
        
        with db_manager.get_session() as session:
            try:
                # Check if exists
                cached = session.query(CachedResponse).filter_by(
                    query_hash=query_hash
                ).first()
                
                if cached:
                    cached.response_text = response
                    cached.response_metadata = metadata
                    cached.expires_at = expires_at
                    cached.last_accessed = datetime.utcnow()
                else:
                    cached = CachedResponse(
                        query_hash=query_hash,
                        query_text=query,
                        response_text=response,
                        response_metadata=metadata,
                        expires_at=expires_at
                    )
                    session.add(cached)
                
                session.flush()
                logger.info("Response cached successfully")
            
            except Exception as e:
                logger.error(f"Error caching response: {e}")
    
    # ==================== Analytics ====================
    
    @staticmethod
    def get_popular_queries(days: int = 7, limit: int = 10) -> List[Dict]:
        """Get most popular queries"""
        with db_manager.get_session() as session:
            since = datetime.utcnow() - timedelta(days=days)
            
            results = session.query(
                QueryHistory.query_text,
                func.count(QueryHistory.id).label('count')
            ).filter(
                QueryHistory.created_at >= since
            ).group_by(
                QueryHistory.query_text
            ).order_by(
                desc('count')
            ).limit(limit).all()
            
            return [{"query": r[0], "count": r[1]} for r in results]
    
    @staticmethod
    def get_trending_domains(days: int = 7) -> List[Dict]:
        """Get trending EE domains"""
        with db_manager.get_session() as session:
            since = datetime.utcnow() - timedelta(days=days)
            
            queries = session.query(QueryHistory).filter(
                QueryHistory.created_at >= since
            ).all()
            
            domain_counts = {}
            for q in queries:
                if q.domains:
                    for domain in q.domains:
                        domain_counts[domain] = domain_counts.get(domain, 0) + 1
            
            sorted_domains = sorted(
                domain_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            return [{"domain": d[0], "count": d[1]} for d in sorted_domains]


# Global operations instance
db_ops = DatabaseOperations()
