"""
trip_routes.py — CRUD endpoints for Trips
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# pyrefly: ignore [missing-import]
from app.database.session import get_db
from app.schemas.trip_schema import TripCreate, TripUpdate, TripResponse
from app.models.trip import Trip
from app.models.expense import Expense
from app.models.stop import Stop
router = APIRouter()


@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(payload: TripCreate, db: Session = Depends(get_db)):
    """Create a new trip."""

    new_trip = Trip(
        title=payload.title,
        description=payload.description,
        start_date=payload.start_date,
        end_date=payload.end_date,
        total_budget=payload.total_budget,
        
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return new_trip

@router.get("/", response_model=List[TripResponse])
def list_trips(db: Session = Depends(get_db)):
    """List all trips."""

    trips = db.query(Trip).all()

    return trips


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    """Get a single trip by ID."""

    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    return trip


@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: int,
    payload: TripUpdate,
    db: Session = Depends(get_db)
):
    """Update trip details."""

    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    trip.title = payload.title
    trip.description = payload.description
    trip.start_date = payload.start_date
    trip.end_date = payload.end_date
    trip.total_budget = payload.total_budget

    db.commit()
    db.refresh(trip)

    return trip


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """Delete a trip."""

    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    db.delete(trip)
    db.commit()

    return None
@router.get("/{trip_id}/budget-summary")
def get_budget_summary(
    trip_id: int,
    db: Session = Depends(get_db)
):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    expenses = db.query(Expense).filter(
        Expense.trip_id == trip_id
    ).all()

    total_spent = sum(
        expense.amount for expense in expenses
    )

    remaining_budget = trip.total_budget - total_spent

    return {
        "trip_id": trip.id,
        "total_budget": trip.total_budget,
        "total_spent": total_spent,
        "remaining_budget": remaining_budget
    }
@router.get(
    "/{trip_id}/full-itinerary",
    response_model=TripResponse
)
def get_full_itinerary(
    trip_id: int,
    db: Session = Depends(get_db)
):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    return trip