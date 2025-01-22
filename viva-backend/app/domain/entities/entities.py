from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()

@dataclass
class FocusLocation:
    start: int
    end: int

@dataclass
class Scenario:
    sentence_id: int
    focus_location: FocusLocation

class AiReview:
    is_correct: bool
    ai_expression: str

class User(Base):
    __tablename__ = 'users'

    google_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(50))
    profile_picture: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    essays: Mapped[List["Essay"]] = relationship("Essay", back_populates="user")

class Essay(Base):
    __tablename__ = 'essays'

    essay_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(255), ForeignKey('users.google_id'))
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship("User", back_populates="essays")
    essay_sentences: Mapped[List["EssaySentence"]] = relationship("EssaySentence", back_populates="essay")
    sentences: Mapped[List["Sentence"]] = relationship(
        "Sentence", 
        secondary="essay_sentences", 
        back_populates="essays",
        viewonly=True
    )

class Sentence(Base):
    __tablename__ = 'sentences'

    sentence_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sentence: Mapped[str] = mapped_column(Text, nullable=False)
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    essay_sentences: Mapped[List["EssaySentence"]] = relationship("EssaySentence", back_populates="sentence")
    essays: Mapped[List["Essay"]] = relationship(
        "Essay", 
        secondary="essay_sentences", 
        back_populates="sentences",
        viewonly=True
    )
    active_mappings: Mapped[List["ActiveMapping"]] = relationship("ActiveMapping", back_populates="sentence")

class EssaySentence(Base):
    __tablename__ = 'essay_sentences'

    essay_id: Mapped[int] = mapped_column(Integer, ForeignKey('essays.essay_id'), primary_key=True)
    sentence_id: Mapped[int] = mapped_column(Integer, ForeignKey('sentences.sentence_id'), primary_key=True)
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    essay: Mapped["Essay"] = relationship("Essay", back_populates="essay_sentences")
    sentence: Mapped["Sentence"] = relationship("Sentence", back_populates="essay_sentences", overlaps="essays,sentences")

class ActiveMapping(Base):
    __tablename__ = 'active_mappings'

    mapping_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sentence_id: Mapped[int] = mapped_column(Integer, ForeignKey('sentences.sentence_id'), nullable=False)
    focus_start: Mapped[int] = mapped_column(Integer, nullable=False)
    focus_end: Mapped[int] = mapped_column(Integer, nullable=False)
    chinese: Mapped[str] = mapped_column(String, nullable=False)
    user_expression: Mapped[str] = mapped_column(String, nullable=False)
    ai_review_is_correct: Mapped[Optional[bool]] = mapped_column(Boolean)
    ai_review_expression: Mapped[Optional[str]] = mapped_column(String)
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    sentence: Mapped["Sentence"] = relationship("Sentence", back_populates="active_mappings")


class WordReview(Base):
    __tablename__ = 'word_review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word: Mapped[str] = mapped_column(String(255), nullable=True)
    wrong_word: Mapped[str] = mapped_column(String(255), nullable=True)
    translation: Mapped[str] = mapped_column(Text, nullable=True)
    example_sentence: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(255), ForeignKey('users.google_id'))
    easiness: Mapped[float] = mapped_column(Float, nullable=True)
    interval: Mapped[int] = mapped_column(Integer, nullable=True)
    repetitions: Mapped[int] = mapped_column(Integer, nullable=True)
    review_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_know: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WordReviewLog(Base):
    __tablename__ = 'word_review_log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word_id: Mapped[int] = mapped_column(Integer, nullable=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(255), ForeignKey('users.google_id'))
    easiness: Mapped[float] = mapped_column(Float, nullable=True)
    interval: Mapped[int] = mapped_column(Integer, nullable=True)
    repetitions: Mapped[int] = mapped_column(Integer, nullable=True)
    review_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())