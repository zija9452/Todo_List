from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
import os
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Get the JWT secret from environment variables
JWT_SECRET = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_key_for_development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    """
    Data model for JWT token payload.

    Attributes:
        user_id: The ID of the user extracted from the token
        username: The username extracted from the token (optional)
    """
    user_id: Optional[str] = None
    username: Optional[str] = None


# Initialize security scheme for FastAPI
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with the given data and expiration time.

    Args:
        data: Dictionary containing the data to encode in the token
        expires_delta: Optional timedelta for token expiration (defaults to 30 minutes)

    Returns:
        Encoded JWT token as a string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        TokenData object containing the decoded token data

    Raises:
        HTTPException: If the token is invalid, expired, or cannot be decoded
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_data = TokenData(user_id=user_id, username=username)
        return token_data

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get the current user from the JWT token in the request.

    Args:
        credentials: HTTP authorization credentials containing the JWT token

    Returns:
        TokenData object containing the current user's information

    Raises:
        HTTPException: If the token is invalid or cannot be validated
    """
    token = credentials.credentials
    return verify_token(token)


def verify_user_owns_resource(current_user: TokenData, resource_user_id: str) -> bool:
    """
    Verify that the current user owns the specified resource.

    Args:
        current_user: TokenData object containing the current user's information
        resource_user_id: The user ID associated with the resource

    Returns:
        True if the current user owns the resource, False otherwise

    Raises:
        HTTPException: If the user does not own the resource (403 Forbidden)
    """
    if current_user.user_id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    return True


def decode_token_payload(token: str) -> dict:
    """
    Decode a JWT token without verification (for debugging purposes only).

    Args:
        token: JWT token string to decode

    Returns:
        Dictionary containing the decoded token payload
    """
    try:
        # This decodes the token without verification - use only for debugging
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except Exception:
        return {}


if __name__ == "__main__":
    # Example usage
    sample_data = {"sub": "user123", "username": "johndoe"}
    token = create_access_token(sample_data)
    print(f"Generated token: {token}")

    decoded = verify_token(token)
    print(f"Decoded token data: {decoded}")