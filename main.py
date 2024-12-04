from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import List, Optional
from crime_search_engine import CrimeSearchEngine
import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext

app = FastAPI()

# Initialize the search engine
embeddings_file = "embeddings.npy"  
metadata_file = "metadata.json" 
model_name = "all-MiniLM-L6-v2"
hf_token = "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"

search_engine = CrimeSearchEngine(
    embeddings_file=embeddings_file,
    metadata_file=metadata_file,
    model_name=model_name,
    hf_token=hf_token
)
search_engine.setup()

# Database connection details
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "user_db"
DB_USER = "user"
DB_PASSWORD = "password"

# Define response model
class QueryResponse(BaseModel):
    results: Optional[List[dict]]
    message: str


# Initialize the password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db_connection():
    """
    Get a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor,
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

def hash_password(password: str) -> str:
    """
    Hash a plain text password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/signup")
async def signup(request: Request):
    """
    API to handle user signup.
    """
    conn = get_db_connection()
    try:
        # Extract input parameters from the request body
        body = await request.json()
        email = body.get("email")
        phone = body.get("phone")
        name = body.get("name")
        password = body.get("password")

        # Validate input parameters
        if not email or not phone or not name or not password:
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Check if the email is already registered
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered.")

            # Hash the password and insert the user into the database
            hashed_password = hash_password(password)
            cursor.execute(
                """
                INSERT INTO users (email, phone, name, password)
                VALUES (%s, %s, %s, %s)
                """,
                (email, phone, name, hashed_password),
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
    """
    API to handle user login.
    """
    conn = get_db_connection()
    try:
        # Extract input parameters from the request body
        body = await request.json()
        email = body.get("email")
        password = body.get("password")

        # Validate input parameters
        if not email or not password:
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Fetch user details by email
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
async def query_api(request):
    """
    Endpoint to query the CrimeSearchEngine.
    """
    try:
        request_data = await request.json()

        # Extract individual parameters
        userid = request_data.get("userid")
        user_query = request_data.get("user_query")
        output_type = request_data.get("output_type")

        # Validate output type
        # if output_type not in ["text", "chart"]:
        #     raise HTTPException(status_code=400, detail="Invalid output_type. Must be 'text' or 'chart'.")

        # Query the embeddings
        results = search_engine.query_embeddings(query=user_query)

        # Construct response
        response_message = "Query processed successfully."
        return QueryResponse(results=results, message=response_message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome!"}