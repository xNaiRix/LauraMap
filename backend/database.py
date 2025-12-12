from typing import List, Optional
import aiosqlite
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
from contextlib import asynccontextmanager

load_dotenv()

_database_path: Optional[str] = None
_initialized = False
_init_lock = asyncio.Lock()

async def get_db_path() -> str:
    global _database_path
    if _database_path is None:
        BASE_DIR = Path(__file__).parent
        _database_path = os.getenv("DATABASE_URL", str(BASE_DIR / "database.db"))
    return _database_path

async def init_db(force: bool = False):
    global _initialized
    print(_initialized)
    async with _init_lock:
        if _initialized and not force:
            return
            
        database_path = await get_db_path()
        
        if force and os.path.exists(database_path):
            os.remove(database_path)
        
        async with aiosqlite.connect(database_path) as db:
            await db.execute("PRAGMA foreign_keys = ON")
            await db.execute("PRAGMA journal_mode = WAL")
            

            await db.executescript("""
                CREATE TABLE IF NOT EXISTS Articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    article_html TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS Points (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    avatar_id INTEGER,
                    x INTEGER,
                    y INTEGER,
                    size INTEGER DEFAULT 255,
                    brief_info TEXT,
                    audio_id INTEGER,
                    article_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (article_id) REFERENCES Articles(id) ON DELETE SET NULL,
                    FOREIGN KEY (avatar_id) REFERENCES Media(id) ON DELETE SET NULL,
                    FOREIGN KEY (audio_id) REFERENCES Media(id) ON DELETE SET NULL
                );

                CREATE TABLE IF NOT EXISTS Media (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    media_url TEXT NOT NULL,
                    media_type TEXT NOT NULL CHECK (media_type IN ('photo', 'video', 'audio')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            await db.commit()
            _initialized = True
            print(f"Database initialized successfully: {database_path}")

@asynccontextmanager
async def get_connection():
    await init_db()
    database_path = await get_db_path()
    async with aiosqlite.connect(database_path) as conn:
        await conn.execute("PRAGMA foreign_keys = ON")
        yield conn

async def insert_item(table_name: str, **kwargs) -> dict:
    valid_tables = {'Articles', 'Points', 'Media'}
    if table_name not in valid_tables:
        print(f"Invalid table name: {table_name}. Valid tables: {valid_tables}")
        return {}
    if not kwargs:
        print("No data provided for insertion")
        return {}
    
    try:
        fields = list(kwargs.keys())
        placeholders = ', '.join(['?' for _ in fields])
        field_names = ', '.join(fields)
        values = tuple(kwargs.values())
        async with get_connection() as db:
            cursor = await db.execute(
                f"INSERT INTO {table_name} ({field_names}) VALUES ({placeholders})",
                values
            )
            await db.commit()
            last_id = cursor.lastrowid
            
            print(f"Successfully inserted into {table_name}: {kwargs}")
            return {"id":last_id}
            
    except aiosqlite.IntegrityError as e:
        print(f"Integrity error inserting into {table_name}: {e}")
        return {}
    except aiosqlite.Error as e:
        print(f"Database error inserting into {table_name}: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error inserting into {table_name}: {e}")
        return {}

async def get_item(table_name: str, id: int) -> dict:
    async with get_connection() as conn:
        #print("p1")
        async with conn.execute(
            f"SELECT * FROM {table_name} WHERE id = ?",
            (id,)
        ) as cursor:
            #print("p2:", cursor)
            row = await cursor.fetchone()
            #print("p3:", row)
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return {}

async def get_items(table_name: str, **kwargs) -> List[dict]:
    async with get_connection() as conn:
        try:
            if kwargs:
                conditions = []
                values = []
                for field, value in kwargs.items():
                    if value is None:
                        conditions.append(f"{field} IS NULL")
                    elif isinstance(value, (list, tuple)):
                        if not value:
                            return []
                        placeholders = ', '.join(['?' for _ in value])
                        conditions.append(f"{field} IN ({placeholders})")
                        values.extend(value)
                    else:
                        conditions.append(f"{field} = ?")
                        values.append(value)
                
                where_clause = " AND ".join(conditions)
                query = f"SELECT * FROM {table_name} WHERE {where_clause}"

                async with conn.execute(query, values) as cursor:
                    rows = await cursor.fetchall()
            else:
                query = f"SELECT * FROM {table_name}"
                async with conn.execute(query) as cursor:
                    rows = await cursor.fetchall()
            
            if rows:
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
            return []
            
        except aiosqlite.Error as e:
            print(f"Database error in get_items: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in get_items: {e}")
            return []
        

async def update_item(table_name: str, id: int, **kwargs) -> bool:
    if not kwargs:
        return True
    
    try:
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = tuple(kwargs.values()) + (id,)
        
        async with get_connection() as conn:
            async with conn.execute(
                f"SELECT COUNT(*) FROM {table_name} WHERE id = ?",
                (id,)
            ) as cursor:
                count = (await cursor.fetchone())[0]
                if count == 0:
                    print(f"No record found in {table_name} with id={id}")
                    return False
            
            await conn.execute(
                f"UPDATE {table_name} SET {set_clause} WHERE id = ?",
                values
            )
            await conn.commit()
            
            print(f"Successfully updated {table_name} id={id}: {kwargs}")
            return True
            
    except aiosqlite.Error as e:
        print(f"Database error updating {table_name}: {e}")
        return False

async def delete_item(table_name: str, id: int) -> bool:#по id
    try:
        async with get_connection() as conn:
            await conn.execute(
                f"DELETE FROM {table_name} WHERE id = ?",
                (id,)
            )
            await conn.commit()
            
            print(f"Successfully deleted from {table_name} id={id}")
            return True
            
    except aiosqlite.Error as e:
        print(f"Database error deleting from {table_name}: {e}")
        return False
