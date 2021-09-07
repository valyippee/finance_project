import logging
from typing import Optional
from base_db import engine, Comment
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import FlushError, ConcurrentModificationError


logger = logging.getLogger(__name__)


class CommentRepository:
    """
    Manages interaction with the comment table in the database.
    """
    def __init__(self, init_engine=engine):
        self.engine = init_engine

    def find_by_id(self, _id: str) -> Optional[Comment]:
        """
        Returns a Submission that matches _id. If such submission does
        not exist, return None.
        """
        with Session(self.engine) as session:
            result = session.query(Comment).filter_by(comment_id=_id).all()
            return result[0]

    def input_comment(self, new_comment: Comment):
        """
        Insert new_submission into the database.
        """
        with Session(self.engine) as session:
            try:
                session.add(new_comment)
                session.commit()
            except (SQLAlchemyError, FlushError, ConcurrentModificationError):
                session.rollback()
                raise

