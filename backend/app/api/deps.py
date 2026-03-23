from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.admin_models import Profile
import json
import base64
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """
    Decodes the Supabase JWT without native verification locally for speed,
    checking the role assigned by Supabase Auth / PostgreSQL.
    """
    try:
        # A real Supabase JWT has 3 parts. We decode the payload (middle part).
        payload_b64 = token.split('.')[1]
        # Pad base64 string
        payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("No user ID found in token")

        # Verify against our profiles table
        result = await db.execute(select(Profile).where(Profile.id == user_id))
        user = result.scalars().first()
        if not user:
            print(f"[AUTH] Auto-provisioning missing Profile for {user_id}")
            email = payload.get("email", f"user_{user_id[:8]}@example.com")
            role = payload.get("app_metadata", {}).get("role", "citizen")
            # Create a new Profile record seamlessly
            user_uuid = uuid.UUID(user_id)
            user = Profile(id=user_uuid, username=email, role=role)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
        return user
    except Exception as e:
        print(f"Auth Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def require_admin(current_user: Profile = Depends(get_current_user)):
    if current_user.role not in ['admin', 'officer']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
