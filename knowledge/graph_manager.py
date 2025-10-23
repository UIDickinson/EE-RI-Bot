from neo4j import GraphDatabase
from typing import Dict, Any, Optional
import os
import logging

logger = logging.getLogger(__name__)


class KnowledgeGraphManager:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            logger.info("Knowledge graph connected")
        except Exception as e:
            logger.error(f"Neo4j connection failed: {e}")
            self.driver = None
    
    def close(self):
        if self.driver:
            self.driver.close()
    
    def add_component(
        self,
        component_id: str,
        properties: Dict[str, Any]
    ) -> bool:
        if not self.driver:
            return False
        
        with self.driver.session() as session:
            query = """
            MERGE (c:Component {id: $component_id})
            SET c += $properties, c.last_updated = datetime()
            RETURN c
            """
            try:
                result = session.run(
                    query,
                    component_id=component_id,
                    properties=properties
                )
                return result.single() is not None
            except Exception as e:
                logger.error(f"Error adding component: {e}")
                return False
    
    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str
    ) -> bool:
        if not self.driver:
            return False
        
        with self.driver.session() as session:
            query = f"""
            MATCH (s:Component {{id: $source_id}})
            MATCH (t:Component {{id: $target_id}})
            MERGE (s)-[r:{relationship_type}]->(t)
            RETURN r
            """
            try:
                result = session.run(
                    query,
                    source_id=source_id,
                    target_id=target_id
                )
                return result.single() is not None
            except Exception as e:
                logger.error(f"Error creating relationship: {e}")
                return False
