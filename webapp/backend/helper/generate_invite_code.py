import secrets
import string

def generate_invite_code(length: int = 6) -> str:
    """Generate a random invite code."""
    characters = string.ascii_letters + string.digits
    invite_code = ''.join(secrets.choice(characters) for _ in range(length))
    return invite_code
