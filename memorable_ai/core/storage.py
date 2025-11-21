"""
Storage Layer

SQL-first architecture with optional graph support.
Inspired by Memori's SQL flexibility and Supermemory's graph architecture.

References:
- Memori: https://github.com/GibsonAI/Memori (SQL storage)
- Supermemory: https://github.com/supermemoryai/supermemory (graph architecture)
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from memorable_ai.core.errors import StorageError
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    DateTime,
    Integer,
    Float,
    JSON,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import json

logger = logging.getLogger(__name__)

Base = declarative_base()


class Memory(Base):
    """Memory table schema."""

    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    memory_type = Column(String(50), nullable=False, index=True)  # fact, preference, skill, rule, context
    namespace = Column(String(255), index=True)  # For multi-tenant support
    extra_metadata = Column(JSON)  # Additional metadata
    embedding = Column(JSON)  # Vector embedding for semantic search
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    access_count = Column(Integer, default=0)
    importance_score = Column(Float, default=0.0, index=True)

    # Indexes for performance
    __table_args__ = (
        Index("idx_memory_type_namespace", "memory_type", "namespace"),
        Index("idx_created_at", "created_at"),
    )


class Conversation(Base):
    """Conversation history table."""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    namespace = Column(String(255), index=True)
    messages = Column(JSON, nullable=False)  # Full conversation messages
    response = Column(JSON)  # LLM response
    extracted_memories = Column(JSON)  # Memories extracted from this conversation
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (Index("idx_namespace_created", "namespace", "created_at"),)


class Storage:
    """
    SQL-first storage layer for memories.
    
    Supports PostgreSQL, SQLite, MySQL with full-text search.
    """

    def __init__(self, connection_string: str, namespace: Optional[str] = None):
        """
        Initialize storage.
        
        Args:
            connection_string: Database connection string
            namespace: Optional namespace for multi-tenant support
        """
        self.connection_string = connection_string
        self.namespace = namespace

        # Create engine
        if connection_string.startswith("sqlite"):
            # SQLite needs special configuration
            self.engine = create_engine(
                connection_string,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        else:
            self.engine = create_engine(connection_string, pool_pre_ping=True)

        # Create session factory
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Create tables
        Base.metadata.create_all(self.engine)

        logger.info(f"Storage initialized: {connection_string}")

    def get_session(self) -> Session:
        """Get database session."""
        return self.SessionLocal()

    async def store_memories(self, memories: List[Dict[str, Any]]):
        """
        Store memories in database.
        
        Checks for duplicates before storing to avoid storing the same memory multiple times.
        
        Args:
            memories: List of memory dictionaries
        """
        if not memories:
            return
            
        session = self.get_session()
        try:
            stored_count = 0
            skipped_count = 0
            
            for memory_data in memories:
                content = memory_data.get("content", "").strip()
                if not content:
                    continue
                    
                memory_type = memory_data.get("type", "fact")
                namespace = self.namespace or memory_data.get("namespace")
                
                # Check if a similar memory already exists
                # Check for exact match first (case-insensitive)
                existing = (
                    session.query(Memory)
                    .filter(Memory.content.ilike(content))
                    .filter(Memory.memory_type == memory_type)
                    .filter(Memory.namespace == namespace if namespace else Memory.namespace.is_(None))
                    .first()
                )
                
                if existing:
                    # Memory already exists, skip or update
                    logger.debug(f"Memory already exists (skipping): {content[:50]}...")
                    skipped_count += 1
                    # Update timestamp and access count to show it was referenced again
                    existing.updated_at = datetime.utcnow()
                    existing.access_count = (existing.access_count or 0) + 1
                    continue
                
                # Check for similar content (fuzzy match for near-duplicates)
                # Get all memories with same type and namespace to check for similar content
                all_similar = (
                    session.query(Memory)
                    .filter(Memory.memory_type == memory_type)
                    .filter(Memory.namespace == namespace if namespace else Memory.namespace.is_(None))
                    .all()
                )
                
                # Check if any existing memory has very similar content (>90% similarity)
                content_lower = content.lower()
                is_duplicate = False
                for existing_mem in all_similar:
                    existing_content_lower = existing_mem.content.lower()
                    # Simple similarity check: if one contains the other or vice versa
                    if (content_lower in existing_content_lower and len(content_lower) < len(existing_content_lower)) or \
                       (existing_content_lower in content_lower and len(existing_content_lower) < len(content_lower)):
                        # Check word overlap for better similarity
                        content_words = set(content_lower.split())
                        existing_words = set(existing_content_lower.split())
                        if content_words and existing_words:
                            overlap = len(content_words.intersection(existing_words))
                            total_unique = len(content_words.union(existing_words))
                            similarity = overlap / total_unique if total_unique > 0 else 0
                            if similarity > 0.8:  # 80% word overlap
                                logger.debug(f"Similar memory already exists (skipping): {content[:50]}... (similarity: {similarity:.2f})")
                                skipped_count += 1
                                is_duplicate = True
                                # Update existing memory
                                existing_mem.updated_at = datetime.utcnow()
                                existing_mem.access_count = (existing_mem.access_count or 0) + 1
                                break
                
                if is_duplicate:
                    continue
                
                # Store new memory
                memory = Memory(
                    content=content,
                    memory_type=memory_type,
                    namespace=namespace,
                    extra_metadata=memory_data.get("metadata", {}),
                    embedding=memory_data.get("embedding"),
                    importance_score=memory_data.get("importance_score", 0.0),
                )
                session.add(memory)
                stored_count += 1

            session.commit()
            logger.debug(f"Stored {stored_count} new memories, skipped {skipped_count} duplicates")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to store memories: {e}")
            raise StorageError(f"Failed to store memories: {e}") from e
        finally:
            session.close()

    async def store_conversation(
        self,
        messages: List[Dict[str, Any]],
        response: Optional[Dict[str, Any]] = None,
        extracted_memories: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Store conversation history.
        
        Args:
            messages: Conversation messages
            response: LLM response
            extracted_memories: Memories extracted from conversation
        """
        session = self.get_session()
        try:
            conversation = Conversation(
                namespace=self.namespace,
                messages=messages,
                response=response,
                extracted_memories=extracted_memories,
            )
            session.add(conversation)
            session.commit()
            logger.debug("Stored conversation")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to store conversation: {e}")
            raise
        finally:
            session.close()

    async def get_memories(
        self,
        memory_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Get memories from database.
        
        Args:
            memory_type: Filter by memory type
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of memory dictionaries
        """
        session = self.get_session()
        try:
            query = session.query(Memory)
            
            if self.namespace:
                query = query.filter(Memory.namespace == self.namespace)
            
            if memory_type:
                query = query.filter(Memory.memory_type == memory_type)
            
            memories = query.order_by(Memory.importance_score.desc()).limit(limit).offset(offset).all()
            
            return [
                {
                    "id": m.id,
                    "content": m.content,
                    "type": m.memory_type,
                    "metadata": m.extra_metadata or {},
                    "embedding": m.embedding,
                    "importance_score": m.importance_score,
                    "created_at": m.created_at.isoformat() if m.created_at else None,
                }
                for m in memories
            ]
        except Exception as e:
            logger.error(f"Failed to get memories: {e}")
            return []
        finally:
            session.close()

    async def search_memories_text(
        self, query: str, limit: int = 10, memory_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Full-text search for memories.
        
        Args:
            query: Search query
            limit: Maximum number of results
            memory_type: Filter by memory type
            
        Returns:
            List of matching memories
        """
        session = self.get_session()
        try:
            # Simple LIKE search (can be enhanced with full-text search)
            search_pattern = f"%{query}%"
            db_query = session.query(Memory).filter(Memory.content.like(search_pattern))
            
            if self.namespace:
                db_query = db_query.filter(Memory.namespace == self.namespace)
            
            if memory_type:
                db_query = db_query.filter(Memory.memory_type == memory_type)
            
            memories = db_query.order_by(Memory.importance_score.desc()).limit(limit).all()
            
            return [
                {
                    "id": m.id,
                    "content": m.content,
                    "type": m.memory_type,
                    "metadata": m.extra_metadata or {},
                    "importance_score": m.importance_score,
                }
                for m in memories
            ]
        except Exception as e:
            logger.error(f"Failed to search memories: {e}")
            return []
        finally:
            session.close()

    async def update_memory_importance(self, memory_id: int, importance_score: float):
        """
        Update memory importance score.
        
        Args:
            memory_id: Memory ID
            importance_score: New importance score
        """
        session = self.get_session()
        try:
            memory = session.query(Memory).filter(Memory.id == memory_id).first()
            if memory:
                memory.importance_score = importance_score
                memory.updated_at = datetime.utcnow()
                session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update memory importance: {e}")
        finally:
            session.close()

    async def delete_memory(self, memory_id: int):
        """
        Delete a memory.
        
        Args:
            memory_id: Memory ID to delete
        """
        session = self.get_session()
        try:
            memory = session.query(Memory).filter(Memory.id == memory_id).first()
            if memory:
                session.delete(memory)
                session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete memory: {e}")
        finally:
            session.close()

    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        session = self.get_session()
        try:
            total_memories = session.query(Memory).count()
            if self.namespace:
                namespace_memories = (
                    session.query(Memory).filter(Memory.namespace == self.namespace).count()
                )
            else:
                namespace_memories = total_memories

            return {
                "total_memories": total_memories,
                "namespace_memories": namespace_memories,
                "namespace": self.namespace,
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {}
        finally:
            session.close()

