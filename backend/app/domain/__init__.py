"""Internal domain types shared by services, repositories and schemas.

Domain records are deliberately NOT the API schemas (Pydantic) and NOT the
ORM models (SQLAlchemy): each can evolve independently.
"""
