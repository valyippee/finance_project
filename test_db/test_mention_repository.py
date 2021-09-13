"""
Test the functions in MentionRepository
"""
import datetime
from base_test_db import engine, Mention
from db.mention_repository import MentionRepository


def test_input_mention_normal():
    mention_table = MentionRepository(engine)
    mention_1 = Mention(mention_id=1, stock_id=1,
                        dt="2021-9-5 4:23:23", comment_id="1234",
                        submission_id="eitlom3", from_comment=True)
    mention_table.input_mention(mention_1)


def test_input_mention_none():
    mention_table = MentionRepository(engine)
    mention_1 = Mention(stock_id=2,
                        dt="2021-9-5 4:23:23", comment_id=None,
                        submission_id="eitlom3", from_comment=False)
    mention_table.input_mention(mention_1)


def test_input_mention_many():
    mention_table = MentionRepository(engine)
    for i in range(24, 60):
        mention_1 = Mention(stock_id=2,
                            dt=f"2021-9-5 4:{i}:23", comment_id=None,
                            submission_id="eitlom3", from_comment=False)
        mention_table.input_mention(mention_1)


def test_find_by_mention_id():
    mention_table = MentionRepository(engine)
    mention = mention_table.find_by_mention_id(1)
    print(mention.from_comment)


def test_filter_by_stock_and_dt():
    mention_table = MentionRepository(engine)
    mentions = mention_table.filter_by_stock_and_dt(2, "2021-9-5 4:26:23",
                                                    "2021-9-5 4:58:23")
    print(len(mentions))


def test_filter_by_stock_and_dt_none():
    mention_table = MentionRepository(engine)
    mentions = mention_table.filter_by_stock_and_dt(1, "2021-9-5 4:26:23",
                                                    "2021-9-5 4:58:23")
    print(mentions)
    print(len(mentions))


# test_input_mention_normal()
# test_input_mention_none()
# test_input_mention_many()
# test_find_by_mention_id()
# test_filter_by_stock_and_dt()
# test_filter_by_stock_and_dt_none()
