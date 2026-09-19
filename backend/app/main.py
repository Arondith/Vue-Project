from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Application
from .schemas import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationStatus,
    ApplicationUpdate,
    StatsResponse,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="ApplyFlow API",
    version="1.0.0",
    description="REST API for the ApplyFlow job application tracker.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/applications", response_model=list[ApplicationRead])
def list_applications(
    application_status: ApplicationStatus | None = Query(default=None, alias="status"),
    q: str = Query(default="", max_length=120),
    db: Session = Depends(get_db),
):
    statement = select(Application)

    if application_status:
        statement = statement.where(Application.status == application_status)

    cleaned_query = q.strip()
    if cleaned_query:
        pattern = f"%{cleaned_query}%"
        statement = statement.where(
            or_(
                Application.company.ilike(pattern),
                Application.role.ilike(pattern),
            )
        )

    statement = statement.order_by(Application.applied_at.desc(), Application.id.desc())
    return db.scalars(statement).all()


@app.post(
    "/api/applications",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    data = payload.model_dump(mode="json")
    application = Application(**data)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@app.put("/api/applications/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    for key, value in payload.model_dump(mode="json").items():
        setattr(application, key, value)

    db.commit()
    db.refresh(application)
    return application


@app.delete(
    "/api/applications/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/api/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    rows = db.execute(
        select(Application.status, func.count(Application.id)).group_by(Application.status)
    ).all()

    counts = {name: count for name, count in rows}
    total = sum(counts.values())

    return StatsResponse(
        total=total,
        applied=counts.get("Applied", 0),
        interview=counts.get("Interview", 0),
        assessment=counts.get("Assessment", 0),
        offer=counts.get("Offer", 0),
        rejected=counts.get("Rejected", 0),
    )
