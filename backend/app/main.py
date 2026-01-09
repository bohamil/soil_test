from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Soil Sampling Backend")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/groups", response_model=schemas.Group)
def create_group(payload: schemas.GroupCreate, db: Session = Depends(get_db)) -> models.Group:
    return crud.create_group(db, payload)


@app.get("/groups", response_model=list[schemas.Group])
def list_groups(
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[models.Group]:
    return crud.list_groups(db, user_id=user_id)


@app.get("/groups/{group_id}", response_model=schemas.Group)
def get_group(group_id: int, db: Session = Depends(get_db)) -> models.Group:
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@app.patch("/groups/{group_id}", response_model=schemas.Group)
def update_group(
    group_id: int, payload: schemas.GroupUpdate, db: Session = Depends(get_db)
) -> models.Group:
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return crud.update_group(db, group, payload)


@app.delete("/groups/{group_id}", status_code=204)
def delete_group(group_id: int, db: Session = Depends(get_db)) -> None:
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    crud.delete_group(db, group)


@app.post("/fields", response_model=schemas.Field)
def create_field(payload: schemas.FieldCreate, db: Session = Depends(get_db)) -> models.Field:
    return crud.create_field(db, payload)


@app.get("/fields", response_model=list[schemas.Field])
def list_fields(
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[models.Field]:
    return crud.list_fields(db, user_id=user_id)


@app.get("/fields/{field_id}", response_model=schemas.Field)
def get_field(field_id: int, db: Session = Depends(get_db)) -> models.Field:
    field = crud.get_field(db, field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    return field


@app.patch("/fields/{field_id}", response_model=schemas.Field)
def update_field(
    field_id: int, payload: schemas.FieldUpdate, db: Session = Depends(get_db)
) -> models.Field:
    field = crud.get_field(db, field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    return crud.update_field(db, field, payload)


@app.delete("/fields/{field_id}", status_code=204)
def delete_field(field_id: int, db: Session = Depends(get_db)) -> None:
    field = crud.get_field(db, field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    crud.delete_field(db, field)


@app.post("/fields/{field_id}/sampling-plans", response_model=schemas.SamplingPlan)
def create_sampling_plan(
    field_id: int,
    payload: schemas.SamplingPlanCreate,
    db: Session = Depends(get_db),
) -> models.SamplingPlan:
    field = crud.get_field(db, field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    return crud.create_sampling_plan(db, field, payload)


@app.get("/fields/{field_id}/sampling-plans", response_model=list[schemas.SamplingPlan])
def list_sampling_plans(field_id: int, db: Session = Depends(get_db)) -> list[models.SamplingPlan]:
    return crud.list_sampling_plans(db, field_id)


@app.post("/sampling-plans/{plan_id}/points", response_model=list[schemas.SamplingPoint])
def create_sampling_points(
    plan_id: int,
    payload: list[schemas.SamplingPointCreate],
    db: Session = Depends(get_db),
) -> list[models.SamplingPoint]:
    plan = crud.get_sampling_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Sampling plan not found")
    return crud.create_sampling_points(db, plan, payload)


@app.get("/sampling-plans/{plan_id}/points", response_model=list[schemas.SamplingPoint])
def list_sampling_points(
    plan_id: int,
    db: Session = Depends(get_db),
) -> list[models.SamplingPoint]:
    return crud.list_sampling_points(db, plan_id)


@app.post("/sampling-plans/{plan_id}/lab-uploads", response_model=schemas.LabUpload)
def create_lab_upload(
    plan_id: int,
    payload: schemas.LabUploadCreate,
    db: Session = Depends(get_db),
) -> models.LabUpload:
    plan = crud.get_sampling_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Sampling plan not found")
    return crud.create_lab_upload(db, plan, payload)


@app.get("/sampling-plans/{plan_id}/lab-uploads", response_model=list[schemas.LabUpload])
def list_lab_uploads(
    plan_id: int,
    db: Session = Depends(get_db),
) -> list[models.LabUpload]:
    return crud.list_lab_uploads(db, plan_id)
