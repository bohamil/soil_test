from sqlalchemy.orm import Session

from . import models
from . import schemas


def create_group(db: Session, payload: schemas.GroupCreate) -> models.Group:
    group = models.Group(**payload.model_dump())
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def list_groups(db: Session, user_id: int | None = None) -> list[models.Group]:
    query = db.query(models.Group)
    if user_id is not None:
        query = query.filter(models.Group.user_id == user_id)
    return query.order_by(models.Group.created_at.desc()).all()


def get_group(db: Session, group_id: int) -> models.Group | None:
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def update_group(db: Session, group: models.Group, payload: schemas.GroupUpdate) -> models.Group:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(group, key, value)
    db.commit()
    db.refresh(group)
    return group


def delete_group(db: Session, group: models.Group) -> None:
    db.delete(group)
    db.commit()


def create_field(db: Session, payload: schemas.FieldCreate) -> models.Field:
    field = models.Field(**payload.model_dump())
    db.add(field)
    db.commit()
    db.refresh(field)
    return field


def list_fields(db: Session, user_id: int | None = None) -> list[models.Field]:
    query = db.query(models.Field)
    if user_id is not None:
        query = query.filter(models.Field.user_id == user_id)
    return query.order_by(models.Field.created_at.desc()).all()


def get_field(db: Session, field_id: int) -> models.Field | None:
    return db.query(models.Field).filter(models.Field.id == field_id).first()


def update_field(db: Session, field: models.Field, payload: schemas.FieldUpdate) -> models.Field:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(field, key, value)
    db.commit()
    db.refresh(field)
    return field


def delete_field(db: Session, field: models.Field) -> None:
    db.delete(field)
    db.commit()


def create_sampling_plan(
    db: Session,
    field: models.Field,
    payload: schemas.SamplingPlanCreate,
) -> models.SamplingPlan:
    plan = models.SamplingPlan(field=field, **payload.model_dump())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def list_sampling_plans(db: Session, field_id: int) -> list[models.SamplingPlan]:
    return (
        db.query(models.SamplingPlan)
        .filter(models.SamplingPlan.field_id == field_id)
        .order_by(models.SamplingPlan.created_at.desc())
        .all()
    )


def get_sampling_plan(db: Session, plan_id: int) -> models.SamplingPlan | None:
    return db.query(models.SamplingPlan).filter(models.SamplingPlan.id == plan_id).first()


def create_sampling_points(
    db: Session,
    plan: models.SamplingPlan,
    points: list[schemas.SamplingPointCreate],
) -> list[models.SamplingPoint]:
    rows = [models.SamplingPoint(sampling_plan=plan, **point.model_dump()) for point in points]
    db.add_all(rows)
    db.commit()
    for row in rows:
        db.refresh(row)
    return rows


def list_sampling_points(db: Session, plan_id: int) -> list[models.SamplingPoint]:
    return (
        db.query(models.SamplingPoint)
        .filter(models.SamplingPoint.sampling_plan_id == plan_id)
        .order_by(models.SamplingPoint.point_index)
        .all()
    )


def create_lab_upload(
    db: Session,
    plan: models.SamplingPlan,
    payload: schemas.LabUploadCreate,
) -> models.LabUpload:
    upload = models.LabUpload(sampling_plan=plan, **payload.model_dump())
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload


def list_lab_uploads(db: Session, plan_id: int) -> list[models.LabUpload]:
    return (
        db.query(models.LabUpload)
        .filter(models.LabUpload.sampling_plan_id == plan_id)
        .order_by(models.LabUpload.created_at.desc())
        .all()
    )
