from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_async_session
from user.schemas import ProfileUpdate, ProfileCreate
from auth.models import profile as Profile

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"]
)


@router.get("/{profile_id}", response_model=Profile)
async def get_profile(profile_id: int, session: Session = Depends(get_async_session)):
    profile = session.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/", response_model=Profile)
async def create_profile(profile_data: ProfileCreate, session: Session = Depends(get_async_session)):
    profile = Profile(**profile_data.dict())
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.put("/{profile_id}", response_model=Profile)
async def update_profile(profile_id: int, profile_data: ProfileUpdate, session: Session = Depends(get_async_session)):
    profile = session.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    session.commit()
    session.refresh(profile)
    return profile


@router.delete("/{profile_id}")
async def delete_profile(profile_id: int, session: Session = Depends(get_async_session)):
    profile = session.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    session.delete(profile)
    session.commit()
    return {"message": "Profile deleted"}
