from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings

security = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify API key from Authorization header
    Expected format Authorization: Bearer <api_key>
    """
    if not settings.enable_auth:
        return True

    token = credentials.credentials
    if token not in settings.api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return True

# Optional dependency - use when you want to make auth optional
def optional_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not settings.enable_auth:
        return None
    return verify_api_key(credentials)