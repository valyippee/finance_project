"""
Test the functions in CommentRepository
"""
import datetime
from base_test_db import engine, Comment
from db.comment_repository import CommentRepository


def test_input_comment():
    comment_table = CommentRepository(engine)
    comment_1 = Comment(comment_id="1234", dt="2021-9-5 4:23:23",
                        body="JD 150USD @eoy", score=1000,
                        submission_id="eitlom3")
    comment_table.input_comment(comment_1)


def test_find_by_id():
    comment_table = CommentRepository(engine)
    comment = comment_table.find_by_id("1234")
    print(comment.body)


# test_input_comment()
# test_find_by_id()
