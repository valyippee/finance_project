from typing import Optional

from base_db import engine, Submission
from sqlalchemy.orm import sessionmaker


class SubmissionRepository:
    """
    Manages interaction with the submission table in the database.
    """
    def __init__(self):
        pass

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
        pass
