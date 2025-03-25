import sqlite3
import json
import os
import logging
from datetime import datetime
from ..utils.config import MEMORY_DB_PATH

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, db_path=MEMORY_DB_PATH):
        """Initialize the memory manager with the database path."""
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the SQLite database with required tables."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                summary TEXT
            )
            ''')
            
            # Create messages table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                timestamp TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
            ''')
            
            # Create user_preferences table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL
            )
            ''')
            
            conn.commit()
            conn.close()
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def store_message(self, role, content, conversation_id=None):
        """Store a message in the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # If no conversation_id provided, create a new conversation
            if conversation_id is None:
                timestamp = datetime.now().isoformat()
                cursor.execute(
                    "INSERT INTO conversations (timestamp, summary) VALUES (?, ?)",
                    (timestamp, "New conversation")
                )
                conversation_id = cursor.lastrowid
            
            # Store the message
            timestamp = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO messages (conversation_id, timestamp, role, content) VALUES (?, ?, ?, ?)",
                (conversation_id, timestamp, role, content)
            )
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "message_id": cursor.lastrowid,
                "conversation_id": conversation_id
            }
        except Exception as e:
            logger.error(f"Error storing message: {e}")
            return {"success": False, "error": str(e)}
    
    def get_conversation(self, conversation_id):
        """Retrieve all messages from a specific conversation."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp",
                (conversation_id,)
            )
            
            messages = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return {"success": True, "messages": messages}
        except Exception as e:
            logger.error(f"Error retrieving conversation: {e}")
            return {"success": False, "error": str(e)}
    
    def get_recent_conversations(self, limit=5):
        """Retrieve recent conversations."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM conversations ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            
            conversations = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return {"success": True, "conversations": conversations}
        except Exception as e:
            logger.error(f"Error retrieving recent conversations: {e}")
            return {"success": False, "error": str(e)}
    
    def set_user_preference(self, key, value):
        """Set a user preference in the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT OR REPLACE INTO user_preferences (key, value) VALUES (?, ?)",
                (key, json.dumps(value))
            )
            
            conn.commit()
            conn.close()
            return {"success": True}
        except Exception as e:
            logger.error(f"Error setting user preference: {e}")
            return {"success": False, "error": str(e)}
    
    def get_user_preference(self, key):
        """Get a user preference from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT value FROM user_preferences WHERE key = ?",
                (key,)
            )
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {"success": True, "value": json.loads(row["value"])}
            else:
                return {"success": False, "error": "Preference not found"}
        except Exception as e:
            logger.error(f"Error getting user preference: {e}")
            return {"success": False, "error": str(e)} 