# Authentication & Authorization

## Strategy
- **JWT (JSON Web Tokens)**: Used for stateless authentication.
- **Refresh Token Pattern**: For long-lived sessions with security.
- **Role-Based Access Control (RBAC)**: Admin and User roles.

## Authentication Flows
1. **Login**:
   - Endpoint: `POST /api/auth/login`
   - Input: Credentials.
   - Output: Access/Refresh tokens + User Profile.
2. **Registration**:
   - Endpoint: `POST /api/auth/register`
   - Input: Email, Username, Password.
3. **Session Refresh**:
   - Endpoint: `POST /api/auth/refresh`
   - Uses refresh token to issue new access token.

## Implementation Details
- **Library**: `python-jose` for JWT, `passlib` for password hashing (bcrypt).
- **FastAPI Security**: Use `OAuth2PasswordBearer` and `Depends` for dependency injection.
- **CORS**: Strict configuration to allow only authorized origins.
