"""Authentication Module

This module provides user authentication and authorization functionality.

Main features:
    - User authentication middleware
    - Login status verification
    - Access control
    - Security validation

Classes:
    None

Functions:
    auth_before(req, sess) -> Optional[Response]: Authentication middleware function

Constants:
    login_redir: Redirect response to login page
"""

from hmac import compare_digest
from fasthtml.common import RedirectResponse

# Redirect response
login_redir = RedirectResponse('/login', status_code=303)

def auth_before(req, sess):
    """Authentication middleware function
    
    Verify user login status and redirect unauthorized users to login page.
    
    Args:
        req: Request object
        sess: Session object
    
    Returns:
        Optional[Response]: Redirect response if unauthorized, None otherwise
    
    Examples:
        >>> auth_before(request, session)
        RedirectResponse('/login', status_code=303)
    """
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth and req.url.path not in ['/login', '/register']: 
        return login_redir 