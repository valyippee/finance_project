from typing import Optional

from base_db import engine, Submission
from sqlalchemy.orm import sessionmaker
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
        self.Session = sessionmaker(init_engine)

    def find_by_id(self, id: int) -> Optional[Submission]:
        """
        Returns a Submission that matches id. If such submission does
        not exist, return None.
        """
        pass

    def input_submission(self, new_submission):
        """
        Insert new_submission into the database.
        """
        with self.Session() as session:
            try:
                session.add(new_submission)
                session.commit()
            except (SQLAlchemyError, FlushError, ConcurrentModificationError):
                session.rollback()
                raise
