from typing import Generator
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import SessionLocal
from app.models.employee import Employee
from app.models.team import Team
from app.models.workspace import Workspace
from app.core.config import settings

# Security scheme for extracting Bearer token
bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Employee:
    if credentials is None:
        # Try to get token from Authorization header directly
        authorization: str | None = request.headers.get("Authorization")
        if authorization is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        token = credentials.credentials

    try:
        # Verify the JWT using Supabase JWT secret
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
        # The subject (sub) claim is the user's UUID in auth.users
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing sub claim",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Convert to UUID
        user_id = UUID(user_id_str)
    except (JWTError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Find user in our employee table by supabase_user_id
    user = db.query(Employee).filter(Employee.supabase_user_id == user_id).first()
    if user is None:
        # User not yet in our database; create a minimal record from token claims
        email: str | None = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing email",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Optional: full_name from user_metadata (if stored in token)
        # Supabase may include user_metadata under `user_metadata` claim
        user_metadata = payload.get("user_metadata", {})
        full_name: str | None = user_metadata.get("full_name")
        if not full_name:
            # fallback to email prefix
            full_name = email.split("@")[0]

        # Determine role: default to 'Employee'; could be read from app_metadata
        role: str | None = payload.get("app_metadata", {}).get("role")
        if role is None:
            role = "Employee"

        # Get or create default workspace
        default_workspace = (
            db.query(Workspace).filter(Workspace.slug == "default").first()
        )
        if not default_workspace:
            default_workspace = Workspace(
                company_name="Default Workspace", slug="default"
            )
            db.add(default_workspace)
            db.commit()
            db.refresh(default_workspace)

        # Get or create a default team within the workspace
        default_team = (
            db.query(Team)
            .filter(Team.workspace_id == default_workspace.id)
            .first()
        )
        if not default_team:
            default_team = Team(name="Default Team", workspace_id=default_workspace.id)
            db.add(default_team)
            db.commit()
            db.refresh(default_team)

        user = Employee(
            email=email,
            full_name=full_name,
            role=role,
            is_active=True,
            supabase_user_id=user_id,
            workspace_id=default_workspace.id,
            team_id=default_team.id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    # Update last login
    from datetime import datetime, timezone

    user.last_login = datetime.now(timezone.utc)
    db.add(user)
    db.commit()

    return user


async def get_current_active_user(
    current_user: Employee = Depends(get_current_user),
) -> Employee:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_workspace(
    current_user: Employee = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Workspace:
    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == current_user.workspace_id)
        .first()
    )
    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace