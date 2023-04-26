from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact
from src.services.auth import auth_service
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as respository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get(
    "/search",
    response_model=List[ContactResponse],
    description="No more than 10 requests per minute.",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def search_contacts(
    first_name: str = Query(None),
    last_name: str = Query(None),
    email: str = Query(None),
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.current_user),
):
    contacts = await respository_contacts.search_contacts(
        db, first_name, last_name, email
    )
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get(
    "/birthday",
    response_model=List[ContactResponse],
    description="No more than 10 requests per minute.",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def birthday_contacts(
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.current_user),
):
    contacts = await respository_contacts.birthday_contacts(db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    description="No more than 10 requests per minute.",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def get_contact(
    contact_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.current_user),
):
    contact = await respository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.get(
    "/",
    response_model=List[ContactResponse],
    description="No more than 10 requests per minute.",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def get_contacts(
    limit: int = Query(ge=5, le=10),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.current_user),
):
    contacts = await respository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.post(
    "/",
    response_model=ContactResponse,
    description="No more than 10 requests per minute.",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def create_contacts(
    body: ContactModel,
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.current_user),
):
    contact = await respository_contacts.create_contact(body, db)
    return contact


@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
    description="No more than 10 requests per minute.",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def updade_contac(
    body: ContactModel,
    contact_id: int = Path(description="The ID of the contacts to update", ge=1),
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.current_user),
):
    contact = await respository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete(
    "/contact_id",
    status_code=status.HTTP_204_NO_CONTENT,
    description="No more than 10 requests per minute.",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def remove_contact(
    contact_id: int = Path(description="The ID of the contacts to delete", ge=1),
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.current_user),
):
    contact = await respository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
