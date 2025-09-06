"""
Role-Based Access Control (RBAC) Dependencies

This module provides reusable dependency functions for controlling access to endpoints
based on user roles and authentication status.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from app.core.db import get_db
from app.models.user import User
from app.crud.users import get_current_user
from app.core.config import settings

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class Permissions:
    """Permission constants for role-based access control"""
    
    # User permissions
    READ_OWN_PROFILE = "read_own_profile"
    UPDATE_OWN_PROFILE = "update_own_profile"
    UPLOAD_FILES = "upload_files"
    GET_RECOMMENDATIONS = "get_recommendations"
    USE_CHAT = "use_chat"
    VIEW_OWN_ANALYSIS = "view_own_analysis"
    
    # Admin permissions
    MANAGE_USERS = "manage_users"
    MANAGE_PRODUCTS = "manage_products"
    MANAGE_BRANDS = "manage_brands"
    VIEW_ALL_ANALYSIS = "view_all_analysis"
    ACCESS_ADMIN_STATS = "access_admin_stats"
    DELETE_ANY_CONTENT = "delete_any_content"


def get_current_authenticated_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.
    Raises 401 if token is invalid or user not found.
    """
    try:
        user = get_current_user(db, token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_admin(
    current_user: User = Depends(get_current_authenticated_user)
) -> User:
    """
    Dependency to require admin access.
    Checks both the is_admin flag and configured ADMIN_EMAIL.
    """
    is_admin_flag = bool(getattr(current_user, "is_admin", False))
    is_configured_admin = bool(
        settings.ADMIN_EMAIL and current_user.email == settings.ADMIN_EMAIL
    )
    
    if not (is_admin_flag or is_configured_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required"
        )
    
    return current_user


def require_user_or_admin(
    current_user: User = Depends(get_current_authenticated_user)
) -> User:
    """
    Dependency for endpoints that regular users and admins can access.
    This is the same as get_current_authenticated_user but with a clearer name.
    """
    return current_user


def require_owner_or_admin(user_id: int):
    """
    Factory function that creates a dependency to check if the current user
    is either the owner of a resource or an admin.
    
    Usage:
        @router.get("/users/{user_id}/profile")
        def get_user_profile(
            user_id: int,
            current_user: User = Depends(require_owner_or_admin(user_id))
        ):
    """
    def _require_owner_or_admin(
        current_user: User = Depends(get_current_authenticated_user)
    ) -> User:
        # Check if user is admin
        is_admin_flag = bool(getattr(current_user, "is_admin", False))
        is_configured_admin = bool(
            settings.ADMIN_EMAIL and current_user.email == settings.ADMIN_EMAIL
        )
        
        # Allow if admin or if user is accessing their own resource
        if is_admin_flag or is_configured_admin or current_user.id == user_id:
            return current_user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own resources"
        )
    
    return _require_owner_or_admin


def check_user_permission(user: User, permission: str) -> bool:
    """
    Check if a user has a specific permission.
    Returns True if the user has the permission, False otherwise.
    """
    # Admin users have all permissions
    if getattr(user, "is_admin", False):
        return True
    
    if settings.ADMIN_EMAIL and user.email == settings.ADMIN_EMAIL:
        return True
    
    # Define permission mappings for regular users
    user_permissions = {
        Permissions.READ_OWN_PROFILE,
        Permissions.UPDATE_OWN_PROFILE,
        Permissions.UPLOAD_FILES,
        Permissions.GET_RECOMMENDATIONS,
        Permissions.USE_CHAT,
        Permissions.VIEW_OWN_ANALYSIS,
    }
    
    # Admin-only permissions
    admin_permissions = {
        Permissions.MANAGE_USERS,
        Permissions.MANAGE_PRODUCTS,
        Permissions.MANAGE_BRANDS,
        Permissions.VIEW_ALL_ANALYSIS,
        Permissions.ACCESS_ADMIN_STATS,
        Permissions.DELETE_ANY_CONTENT,
    }
    
    # Check if regular user has permission
    if permission in user_permissions:
        return True
    
    # Admin-only permissions require admin status
    if permission in admin_permissions:
        return False
    
    # Unknown permission - deny by default
    return False


def require_permission(permission: str):
    """
    Factory function that creates a dependency to check for a specific permission.
    
    Usage:
        @router.post("/admin/products")
        def create_product(
            current_user: User = Depends(require_permission(Permissions.MANAGE_PRODUCTS))
        ):
    """
    def _require_permission(
        current_user: User = Depends(get_current_authenticated_user)
    ) -> User:
        if not check_user_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        return current_user
    
    return _require_permission


def get_user_role(user: User) -> str:
    """Get the role of a user as a string"""
    if getattr(user, "is_admin", False):
        return "admin"
    if settings.ADMIN_EMAIL and user.email == settings.ADMIN_EMAIL:
        return "admin"
    return "user"


def is_admin_user(user: User) -> bool:
    """Check if a user is an admin"""
    return get_user_role(user) == "admin"


# Optional dependency - returns None if not authenticated
def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional authentication dependency.
    Returns the user if authenticated, None if not.
    Useful for endpoints that have different behavior for authenticated vs anonymous users.
    """
    if not token:
        return None
    
    try:
        return get_current_user(db, token)
    except Exception:
        return None
