from typing import Optional

from base_db import engine, Comment
from sqlalchemy.orm import sessionmaker


class CommentRepository:
    """
    Manages interaction with the comment table in the database.
    """
    def __init__(self):
        pass

    def find_by_id(self, id: int) -> Optional[Comment]:
        """
        Returns a Submission that matches id. If such submission does
        not exist, return None.
        """
        pass

    def input_comment(self, new_comment: Comment):
        """
        Insert new_submission into the database.
        """
        pass
