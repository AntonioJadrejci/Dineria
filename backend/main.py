from database import test_connection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Dineria API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Dineria API!"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "application": "Dineria"
    }


@app.get("/api/database-test")
def database_test():
    try:
        result = test_connection()

        return {
            "status": "connected",
            "database": "Supabase PostgreSQL",
            "result": result
        }

    except Exception as error:
        print("Database connection failed:", type(error).__name__)

        return {
            "status": "error",
            "message": "Database connection failed"
        }
