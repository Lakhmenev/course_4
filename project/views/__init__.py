from .genres import genres_ns
from .directors import directors_ns
from .movies import movies_ns
from .users import users_ns
from .users import user_ns
from .auth import auth_ns
from .protected import protected_ns


__all__ = [
    "genres_ns", "directors_ns", "movies_ns", "users_ns", "auth_ns", "protected_ns", "user_ns"
]
