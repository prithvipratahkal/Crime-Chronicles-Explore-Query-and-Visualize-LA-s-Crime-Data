from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import List, Optional
from crime_search_engine import CrimeSearchEngine
import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext

app = FastAPI()

# Initialize the search engine
search_engine = CrimeSearchEngine(
    embeddings_file="embeddings.npy",
    metadata_file="metadata.json",
    model_name="all-MiniLM-L6-v2",
    hf_token="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"
)
search_engine.setup()

# Database connection settings
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "user_db",
    "user": "user",
    "password": "password"
}

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


def hash_password(password: str) -> str:
    """Hash a plain text password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


# Response model for the query API
class QueryResponse(BaseModel):
    results: Optional[List[dict]]
    message: str


@app.post("/signup")
async def signup(request: Request):
    """API to handle user signup."""
    body = await request.json()
    email = body.get("email")
    phone = body.get("phone")
    name = body.get("name")
    password = body.get("password")

    if not all([email, phone, name, password]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Email already registered.")

            hashed_password = hash_password(password)
            cursor.execute(
                "INSERT INTO users (email, phone, name, password) VALUES (%s, %s, %s, %s)",
                (email, phone, name, hashed_password)
            )
            conn.commit()
        return {"message": "User registered successfully."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")
    finally:
        conn.close()


@app.post("/login")
async def login(request: Request):
    """API to handle user login."""
    body = await request.json()
    email = body.get("email")
    password = body.get("password")

    if not all([email, password]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user or not verify_password(password, user["password"]):
                raise HTTPException(status_code=401, detail="Invalid email or password.")
        return {"message": "Login successful."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
    finally:
        conn.close()


@app.post("/query", response_model=QueryResponse)
async def query_api(request: Request):
    """API to query the CrimeSearchEngine."""
    body = await request.json()
    user_query = body.get("user_query")

    if not user_query:
        raise HTTPException(status_code=400, detail="Missing user query")

    try:
        results = search_engine.query_embeddings(query=user_query)
        return QueryResponse(results=results, message="Query processed successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "Welcome!"}
