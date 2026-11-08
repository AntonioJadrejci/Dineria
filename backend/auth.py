from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_db
from models import RestaurantAdmin
from storage import supabase

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)

        if response.user is None:
            raise HTTPException(
                status_code=401,
                detail="Neispravan token."
            )

        return response.user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Nevažeći ili istekli token."
        )


def require_restaurant_access(
    restaurant_id: int,
    user,
    db: Session
):
    access = (
        db.query(RestaurantAdmin)
        .filter(
            RestaurantAdmin.restaurant_id == restaurant_id,
            RestaurantAdmin.user_id == UUID(str(user.id))
        )
        .first()
    )

    if access is None:
        raise HTTPException(
            status_code=403,
            detail="Nemaš dopuštenje za ovaj restoran."
        )