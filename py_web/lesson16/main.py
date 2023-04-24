import time

from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.db import get_db
from src.routes import contacts, auth

app = FastAPI()


@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers["performance"] = str(during)
    return response


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


@app.get("/")
def main_pange():
    return {"greating": "Hello FastAPI"}


app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")

# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpZ29yLnZveXQ5OEBnbWFpbC5jb20iLCJpYXQiOjE2ODIzNDU5ODgsImV4cCI6MTY4MjM1MzE4OCwic2NvcGUiOiJhY2Nlc3NfdG9rZW4ifQ.Z6W5vEWccloFMKPVmNiUsH9hXV5Z3bDtZPBET-Pzz8M",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpZ29yLnZveXQ5OEBnbWFpbC5jb20iLCJpYXQiOjE2ODIzNDU5ODgsImV4cCI6MTY4Mjk1MDc4OCwic2NvcGUiOiJyZWZyZXNoX3Rva2VuIn0.fYNA_La_KyASKkroWPqk725K0JSADcsTc8_VmvOajsA",
#   "token_type": "bearer"
# }