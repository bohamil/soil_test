from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    groups: Mapped[list["Group"]] = relationship(back_populates="user")
    fields: Mapped[list["Field"]] = relationship(back_populates="user")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="groups")
    fields: Mapped[list["Field"]] = relationship(back_populates="group")


class Field(Base):
    __tablename__ = "fields"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id"), nullable=True)
    field_name: Mapped[str] = mapped_column(String, index=True)
    geometry_wkt: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_file_name: Mapped[str | None] = mapped_column(String, nullable=True)
    attributes_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="fields")
    group: Mapped[Group | None] = relationship(back_populates="fields")
    sampling_plans: Mapped[list["SamplingPlan"]] = relationship(back_populates="field")


class SamplingPlan(Base):
    __tablename__ = "sampling_plans"
    __table_args__ = (UniqueConstraint("field_id", "name", name="uq_sampling_plan_field_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    grid_size_acres: Mapped[float] = mapped_column(Float)
    grid_offset_x: Mapped[float] = mapped_column(Float, default=0.0)
    grid_offset_y: Mapped[float] = mapped_column(Float, default=0.0)
    numbering_method: Mapped[str] = mapped_column(String, default="snake")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    field: Mapped[Field] = relationship(back_populates="sampling_plans")
    points: Mapped[list["SamplingPoint"]] = relationship(back_populates="sampling_plan")
    lab_uploads: Mapped[list["LabUpload"]] = relationship(back_populates="sampling_plan")


class SamplingPoint(Base):
    __tablename__ = "sampling_points"
    __table_args__ = (
        UniqueConstraint("sampling_plan_id", "point_index", name="uq_sampling_point_plan_index"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sampling_plan_id: Mapped[int] = mapped_column(ForeignKey("sampling_plans.id"), index=True)
    point_index: Mapped[int] = mapped_column(Integer)
    geometry_wkt: Mapped[str] = mapped_column(Text)
    properties_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    sampling_plan: Mapped[SamplingPlan] = relationship(back_populates="points")


class LabUpload(Base):
    __tablename__ = "lab_uploads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sampling_plan_id: Mapped[int] = mapped_column(ForeignKey("sampling_plans.id"), index=True)
    original_filename: Mapped[str] = mapped_column(String)
    mapping_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sampling_plan: Mapped[SamplingPlan] = relationship(back_populates="lab_uploads")
