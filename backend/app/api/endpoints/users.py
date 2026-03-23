import os
import httpx
import time
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_db
from app.db.admin_models import Complaint, Profile
from app.schemas.admin_schemas import ComplaintResponse
from app.api.deps import get_current_user

router = APIRouter()

# Cloud configuration payload required for the hackathon BaaS transition
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY", "")


@router.get("/complaints", response_model=List[ComplaintResponse])
async def get_my_complaints(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns complaints filed by the currently authenticated user.
    Scoped strictly to citizen_id == current_user.id.
    No cross-user data leakage possible.
    """
    query = (
        select(Complaint)
        .where(Complaint.citizen_id == current_user.id)
        .order_by(Complaint.created_at.desc())
    )
    start = time.time()
    result = await db.execute(query)
    elapsed = int((time.time() - start) * 1000)
    print(f"[users] GET /user/complaints → user={current_user.id} elapsed={elapsed}ms")
    return result.scalars().all()


@router.get("/{username}/exposure")
async def get_safe_exposure(username: str, current_aqi: int):
    """
    Hackathon Win Algorithm: Calculates highly personalized safe 
    outdoor exposure time using Cloud Supabase Profiles.
    """
    if not SUPABASE_URL or not SUPABASE_KEY or "placeholder" in SUPABASE_URL:
        raise HTTPException(
            status_code=503, 
            detail="MISSING_CREDENTIALS: You must populate VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY to resolve the cloud profile."
        )

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        url = f"{SUPABASE_URL}/rest/v1/profiles?username=eq.{username}&select=*"
        try:
            resp = await client.get(url, headers=headers)
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Cloud Connection Terminated: {str(e)}")
            
    if resp.status_code != 200:
        raise HTTPException(status_code=503, detail="Supabase linkage rejected the REST request.")
        
    data = resp.json()
    if not data:
        raise HTTPException(status_code=404, detail="Civilian profile not found in the Supabase cluster. Please register first.")
        
    user = data[0]
    
    age = user.get("age", 30)
    asthma = user.get("has_asthma", False)
    
    safe_minutes = 1440
    
    if current_aqi > 50:
        safe_minutes = 1440 * (50 / current_aqi)
    
    if asthma:
        safe_minutes *= 0.4
    if age > 65 or age < 12:
        safe_minutes *= 0.5
        
    safe_minutes = max(10, min(1440, int(safe_minutes)))
    
    risk_level = "Low"
    if current_aqi > 150 or safe_minutes < 120: risk_level = "High"
    if current_aqi > 300 or safe_minutes < 30: risk_level = "CRITICAL"
    
    vuln_string = []
    if asthma: vuln_string.append("asthma")
    if age > 65: vuln_string.append("senior age bracket")
    elif age < 12: vuln_string.append("pediatric age bracket")
    
    reasoning = f"due to {', '.join(vuln_string)}" if vuln_string else "based on healthy adult baselines"
    
    return {
        "username": username,
        "current_aqi": current_aqi,
        "safe_exposure_minutes": safe_minutes,
        "risk_level": risk_level,
        "recommendation": f"Warning: Your personalized safe exposure is limited to {safe_minutes} mins {reasoning}."
    }


@router.get("/{username}/exposure")
async def get_safe_exposure(username: str, current_aqi: int):
    """
    Hackathon Win Algorithm: Calculates highly personalized safe 
    outdoor exposure time using Cloud Supabase Profiles.
    """
    if not SUPABASE_URL or not SUPABASE_KEY or "placeholder" in SUPABASE_URL:
        # Fallback strictly rejected by Zero-Hallucination protocol. Expose error.
        raise HTTPException(
            status_code=503, 
            detail="MISSING_CREDENTIALS: You must populate VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY to resolve the cloud profile."
        )

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    # Fetch user profile natively using Supabase REST standard (Zero heavy dependencies)
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Assumes a 'profiles' table syncs with Supabase Auth
        url = f"{SUPABASE_URL}/rest/v1/profiles?username=eq.{username}&select=*"
        try:
            resp = await client.get(url, headers=headers)
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Cloud Connection Terminated: {str(e)}")
            
    if resp.status_code != 200:
        raise HTTPException(status_code=503, detail="Supabase linkage rejected the REST request.")
        
    data = resp.json()
    if not data:
        raise HTTPException(status_code=404, detail="Civilian profile not found in the Supabase cluster. Please register first.")
        
    user = data[0]
    
    # Resume identical physiological logic algorithm
    age = user.get("age", 30)
    asthma = user.get("has_asthma", False)
    
    # Baseline: Healthy adult at AQI 50 can stay out 1440 min (24h)
    safe_minutes = 1440
    
    if current_aqi > 50:
        safe_minutes = 1440 * (50 / current_aqi)
    
    if asthma:
        safe_minutes *= 0.4  # 60% reduction
    if age > 65 or age < 12:
        safe_minutes *= 0.5  # 50% reduction
        
    safe_minutes = max(10, min(1440, int(safe_minutes)))
    
    risk_level = "Low"
    if current_aqi > 150 or safe_minutes < 120: risk_level = "High"
    if current_aqi > 300 or safe_minutes < 30: risk_level = "CRITICAL"
    
    vuln_string = []
    if asthma: vuln_string.append("asthma")
    if age > 65: vuln_string.append("senior age bracket")
    elif age < 12: vuln_string.append("pediatric age bracket")
    
    reasoning = f"due to {', '.join(vuln_string)}" if vuln_string else "based on healthy adult baselines"
    
    return {
        "username": username,
        "current_aqi": current_aqi,
        "safe_exposure_minutes": safe_minutes,
        "risk_level": risk_level,
        "recommendation": f"Warning: Your personalized safe exposure is limited to {safe_minutes} mins {reasoning}."
    }
