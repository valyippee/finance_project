from typing import Optional
from base_db import engine, Submission
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import FlushError, ConcurrentModificationError
import logging

logger = logging.getLogger(__name__)


class SubmissionRepository:
    """
    Manages interaction with the submission table in the database.
    """
    def __init__(self, init_engine=engine):
        """
        Initializes the SubmissionRepository with a default engine imported from base_db.
        """
        self.engine = init_engine

    def find_by_id(self, _id: str) -> Optional[Submission]:
        """
        Returns a Submission that matches _id. If such submission does
        not exist, return None.
        """
        with Session(self.engine) as session:
            result = session.query(Submission).\
                filter_by(submission_id=_id).all()
            return result[0]

    def input_submission(self, new_submission):
        """
        Insert new_submission into the database.
        """
        with Session(self.engine) as session:
            try:
                session.add(new_submission)
                session.commit()
            except (SQLAlchemyError, FlushError, ConcurrentModificationError):
                session.rollback()
                raise
