#!/usr/bin/env python3
"""
Initialize database schema and optionally seed with sample data
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import db_manager
from database.models import Base
from database.operations import db_ops
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize database"""
    logger.info("Initializing database...")
    
    # Test connection
    if not db_manager.test_connection():
        logger.error("Database connection failed!")
        return False
    
    # Create tables
    logger.info("Creating tables...")
    db_manager.create_tables()
    
    logger.info("✅ Database initialized successfully!")
    return True


def seed_sample_data():
    """Seed database with sample data (optional)"""
    logger.info("Seeding sample data...")
    
    # Sample research paper
    sample_paper = {
        "title": "High-Efficiency GaN Power Transistors for Automotive Applications",
        "authors": ["John Doe", "Jane Smith"],
        "abstract": "This paper presents novel GaN transistor designs...",
        "year": 2024,
        "source": "IEEE",
        "url": "https://example.com/paper",
        "domains": ["power_management", "automotive"],
        "keywords": ["GaN", "power electronics", "automotive"]
    }
    
    db_ops.add_research_paper(sample_paper)
    
    # Sample component
    sample_component = {
        "part_number": "STM32H743ZIT6",
        "manufacturer": "STMicroelectronics",
        "category": "microcontroller",
        "specifications": {
            "core": "ARM Cortex-M7",
            "frequency": "480MHz",
            "flash": "2MB",
            "ram": "1MB"
        },
        "unit_price": 8.50,
        "stock_status": "in_stock"
    }
    
    db_ops.add_component(sample_component)
    
    logger.info("✅ Sample data seeded!")


def main():
    """Main entry point"""
    print("=" * 60)
    print("  EE Research Scout - Database Initialization")
    print("=" * 60)
    
    if not init_database():
        sys.exit(1)
    
    # Ask if user wants sample data
    seed = input("\nSeed with sample data? (y/N): ")
    if seed.lower() == 'y':
        seed_sample_data()
    
    print("\n🎉 Database setup complete!")


if __name__ == "__main__":
    main()
