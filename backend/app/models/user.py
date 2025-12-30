"""User and UserScope models for authentication and access control"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    """
    User account linked to Clerk authentication

    Roles: coach, location_manager, regional_director, brand_admin
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    clerk_user_id = Column(String(255), unique=True, nullable=False, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    role = Column(
        String(50), nullable=False
    )  # 'coach', 'location_manager', 'regional_director', 'brand_admin'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    brand = relationship("Brand", back_populates="users")
    scopes = relationship("UserScope", back_populates="user", cascade="all, delete-orphan")
    coach = relationship("Coach", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"


class UserScope(Base):
    """
    Defines which regions/locations a user has access to

    For Location Managers and Regional Directors who need scoped access
    """

    __tablename__ = "user_scopes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    scope_type = Column(String(50), nullable=False)  # 'region' or 'location'
    scope_id = Column(Integer, nullable=False)  # region_id or location_id
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="scopes")

    def __repr__(self):
        return f"<UserScope(user_id={self.user_id}, type='{self.scope_type}', scope_id={self.scope_id})>"
