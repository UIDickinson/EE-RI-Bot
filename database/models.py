"""
Database models for EE Research Scout Agent
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float, JSON, 
    Boolean, ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class ResearchPaper(Base):
    """Store research papers and patents"""
    __tablename__ = 'research_papers'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    authors = Column(JSON)  # List of author names
    abstract = Column(Text)
    year = Column(Integer)
    source = Column(String(100))  # arXiv, IEEE, Semantic Scholar, etc.
    url = Column(String(500))
    doi = Column(String(200), unique=True, nullable=True)
    domains = Column(JSON)  # List of EE domains
    keywords = Column(JSON)  # List of keywords
    citation_count = Column(Integer, default=0)
    relevance_score = Column(Float, default=0.0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    queries = relationship("QueryHistory", back_populates="paper")
    
    __table_args__ = (
        Index('idx_year', 'year'),
        Index('idx_source', 'source'),
        Index('idx_domains', 'domains', postgresql_using='gin'),
    )


class Component(Base):
    """Store component information"""
    __tablename__ = 'components'
    
    id = Column(Integer, primary_key=True)
    part_number = Column(String(200), unique=True, nullable=False)
    manufacturer = Column(String(200))
    category = Column(String(100))  # microcontroller, power_ic, sensor, etc.
    
    # Specifications (stored as JSON for flexibility)
    specifications = Column(JSON)
    
    # Pricing
    unit_price = Column(Float)
    currency = Column(String(10), default='USD')
    
    # Availability
    stock_status = Column(String(50))  # in_stock, limited, obsolete
    lead_time_weeks = Column(Integer)
    
    # Links
    datasheet_url = Column(String(500))
    product_url = Column(String(500))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    alternatives = relationship("ComponentAlternative", 
                               foreign_keys="ComponentAlternative.component_id",
                               back_populates="component")
    supply_chain = relationship("SupplyChain", back_populates="component")
    
    __table_args__ = (
        Index('idx_part_number', 'part_number'),
        Index('idx_manufacturer', 'manufacturer'),
        Index('idx_category', 'category'),
    )


class ComponentAlternative(Base):
    """Store component alternatives/equivalents"""
    __tablename__ = 'component_alternatives'
    
    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('components.id'))
    alternative_id = Column(Integer, ForeignKey('components.id'))
    similarity_score = Column(Float, default=0.0)
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    component = relationship("Component", 
                            foreign_keys=[component_id],
                            back_populates="alternatives")
    alternative = relationship("Component", foreign_keys=[alternative_id])
    
    __table_args__ = (
        UniqueConstraint('component_id', 'alternative_id', name='uq_component_alternative'),
    )


class SupplyChain(Base):
    """Store supply chain information"""
    __tablename__ = 'supply_chain'
    
    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('components.id'))
    distributor = Column(String(100))  # Digi-Key, Mouser, etc.
    region = Column(String(50))  # EU, Asia, USA
    
    stock_quantity = Column(Integer)
    price = Column(Float)
    currency = Column(String(10), default='USD')
    moq = Column(Integer)  # Minimum Order Quantity
    
    last_checked = Column(DateTime, default=datetime.utcnow)
    
    component = relationship("Component", back_populates="supply_chain")
    
    __table_args__ = (
        Index('idx_distributor', 'distributor'),
        Index('idx_region', 'region'),
        Index('idx_last_checked', 'last_checked'),
    )


class QueryHistory(Base):
    """Store user query history"""
    __tablename__ = 'query_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))
    session_id = Column(String(100))
    
    query_text = Column(Text, nullable=False)
    domains = Column(JSON)  # Identified domains
    strategy = Column(String(100))  # innovation_search, component_comparison, etc.
    
    # Response metadata
    papers_found = Column(Integer, default=0)
    components_analyzed = Column(Integer, default=0)
    response_time_seconds = Column(Float)
    
    # User feedback
    helpful = Column(Boolean, nullable=True)
    feedback_text = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    paper_id = Column(Integer, ForeignKey('research_papers.id'), nullable=True)
    paper = relationship("ResearchPaper", back_populates="queries")
    
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_session_id', 'session_id'),
        Index('idx_created_at', 'created_at'),
    )


class ComplianceStandard(Base):
    """Store compliance standards information"""
    __tablename__ = 'compliance_standards'
    
    id = Column(Integer, primary_key=True)
    standard_code = Column(String(50), unique=True, nullable=False)  # CE, FCC, CCC
    region = Column(String(50))
    category = Column(String(100))
    
    description = Column(Text)
    requirements = Column(JSON)
    estimated_cost_min = Column(Float)
    estimated_cost_max = Column(Float)
    timeline_weeks = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_standard_code', 'standard_code'),
        Index('idx_region', 'region'),
    )


class CachedResponse(Base):
    """Cache LLM responses for common queries"""
    __tablename__ = 'cached_responses'
    
    id = Column(Integer, primary_key=True)
    query_hash = Column(String(64), unique=True, nullable=False)  # SHA-256 of query
    query_text = Column(Text)
    
    response_text = Column(Text)
    response_metadata = Column(JSON)
    
    hit_count = Column(Integer, default=1)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Cache expiry
    expires_at = Column(DateTime)
    
    __table_args__ = (
        Index('idx_query_hash', 'query_hash'),
        Index('idx_expires_at', 'expires_at'),
    )
