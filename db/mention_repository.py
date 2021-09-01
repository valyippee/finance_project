from typing import Optional

from base_db import engine, Mention
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

class MentionRepository:
    """
    Manages interaction with the mention table in the database.
    """
    def __init__(self):
        pass

    def find_by_id(self, id: int) -> Optional[Mention]:
        """
        Returns a Mention that matches id. If such mention does
        not exist, return None.
        """
        pass

    def input_mention(self, new_mention: Mention):
        """
        Insert new_submission into the database.
        """
        pass
