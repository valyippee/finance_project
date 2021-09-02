from db.submission_repository import SubmissionRepository
from db.base_db import Submission
from base_test_db import engine
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def test_input_submission():
    submission_repo = SubmissionRepository(engine)
    created_utc = 1577940990
    new_time = datetime.fromtimestamp(created_utc).strftime("%Y-%m-%d %H:%M:%S")
    print(type(new_time))
    new_sub = Submission(submission_id="eitlom3",
                         dt=new_time,
                         selftext="Hey everybody,\n\nI've recently started programming with Python and I",
                         title='Glad to have found this sub.')
    try:
        submission_repo.input_submission(new_sub)
    except SQLAlchemyError as err:
        error = str(err.__dict__['orig'])
        print(error)


test_input_submission()
