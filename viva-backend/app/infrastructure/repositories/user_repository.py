from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from domain.entities.entities import User
from infrastructure.repositories.database_manager import db_manager

class UserRepository:
    def create_user(self, google_id: str, email: str, username: str = None, profile_picture: str = None) -> dict:
        with db_manager.session_scope() as session:
            new_user = User(
                google_id=google_id,
                email=email,
                username=username,
                profile_picture=profile_picture
            )
            session.add(new_user)
            session.flush()
            return self._user_to_dict(new_user)

    def get_user_by_google_id(self, google_id: str) -> Optional[dict]:
        with db_manager.session_scope() as session:
            user = session.query(User).filter(User.google_id == google_id).first()
            return self._user_to_dict(user) if user else None

    def get_user_by_email(self, email: str) -> Optional[User]:
        with db_manager.session_scope() as session:
            return session.query(User).filter(User.email == email).first()

    def update_user(self, google_id: str, **kwargs) -> dict:
        with db_manager.session_scope() as session:
            user = session.query(User).filter(User.google_id == google_id).first()
            if not user:
                raise ValueError("User not found")
            
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            session.flush()
            return self._user_to_dict(user)

    def delete_user(self, google_id: str) -> bool:
        with db_manager.session_scope() as session:
            user = session.query(User).filter(User.google_id == google_id).first()
            if not user:
                return False
            
            session.delete(user)
            return True

    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        with db_manager.session_scope() as session:
            return session.query(User).offset(skip).limit(limit).all()

    def search_users(self, keyword: str) -> List[User]:
        with db_manager.session_scope() as session:
            return session.query(User).filter(
                (User.username.ilike(f'%{keyword}%')) | (User.email.ilike(f'%{keyword}%'))
            ).all()

    def _user_to_dict(self, user: User) -> dict:
        return {
            'google_id': user.google_id,
            'email': user.email,
            'username': user.username,
            'profile_picture': user.profile_picture
        }