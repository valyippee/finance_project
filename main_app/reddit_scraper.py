import praw
from prawcore.exceptions import OAuthException, ResponseException
from psaw import PushshiftAPI
import main_app.config as config
from db.base_db import engine
from db.stock_repository import StockRepository
from db.comment_repository import CommentRepository
from db.submission_repository import SubmissionRepository
from db.mention_repository import MentionRepository
from base_db import Comment, Submission, Mention
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)
datetime_fmt = "%Y-%m-%d %H:%M:%S"


class RedditScraper:
    """
    Uses praw to scrape data from reddit. Calls DB interface to store
    data into the database.

    === Public Attributes ===
    subreddit: the subreddit that this RedditScraper is scraping from

    === Private attributes ===
    _reddit: an instance of Reddit from praw
    _api: an instance of PushShiftAPI
    _praw_subreddit: an authorized subreddit instance which is used to retrieve data
                from this subreddit
    _comment_repository: interacts with the comment table in the database
    _submission_repository: interacts with the submission table in the database
    _mention_repository: interacts with the mention table in the database
    """

    def __init__(self, subreddit: str, init_engine=engine):
        print(os.path.abspath(config.__file__))
        print(config.client_id)
        try:
            self._reddit = praw.Reddit(
                client_id=config.client_id,
                client_secret=config.client_secret,
                password=config.password,
                user_agent=config.user_agent,
                username=config.username
            )
        except OAuthException:
            logger.exception("User is not authenticated. Failed to create a RedditScraper instance.")
            raise
        except ResponseException:
            logger.exception("Failed to create a RedditScraper instance.")
            raise

        # used for psaw
        self._api = PushshiftAPI()
        self.subreddit = subreddit

        # used for praw
        self._praw_subreddit = self._reddit.subreddit(subreddit)

        self._stock_repository = StockRepository(init_engine)
        # self._comment_repository = CommentRepository(init_engine)
        self._submission_repository = SubmissionRepository(init_engine)
        # self._mention_repository = MentionRepository(init_engine)

    def scrape_submissions_between(self, start_date, end_date) -> None:
        """
        Get submissions after the given datetime and
        input those submissions into the database.

        Count mentions and update them into the database too.
        """
        submissions = self._api.search_submissions(after=start_date,
                                                   before=end_date,
                                                   subreddit=self.subreddit)
        for submission in submissions:
            if self._submission_repository.find_by_id(submission.id) is None:
                sub_datetime = datetime.fromtimestamp(submission.created_utc).strftime(datetime_fmt)
                try:
                    new_submission = Submission(submission_id=submission.id,
                                                dt=sub_datetime,
                                                selftext=submission.selftext,
                                                title=submission.title)
                    self._submission_repository.input_submission(new_submission)
                except SQLAlchemyError as err:
                    error = str(err.__dict__['orig'])
                    logger.exception(f"Submission with id {submission.id} not successfully added to the database. "
                                     f"Error: {error}")
                else:
                    self.count_mentions_and_populate_table(submission.title, sub_datetime, submission.id, False)
                    self.count_mentions_and_populate_table(submission.selftext, sub_datetime, submission.id, False)

    # def scrape_comments_between(self, start_date, end_date) -> None:
    #     """
    #     Get submissions after the given datetime and
    #     input those submissions into the database.
    #
    #     Count mentions and update them into the database too.
    #     """
    #     comments = self._api.search_comments(after=start_date,
    #                                          before=end_date,
    #                                          subreddit=self.subreddit, limit=1)
    #     for comment in comments:
    #         if self._submission_repository.find_by_id(comment.link_id) is None:
    #             self._scrape_submission_by_id(comment.link_id)
    #         if self._comment_repository.find_by_id(comment.id) is None:
    #             comment_datetime = datetime.fromtimestamp(comment.created_utc).strftime(datetime_fmt)
    #             try:
    #                 new_comment = Comment(comment_id=comment.id,
    #                                       dt=comment_datetime,
    #                                       body=comment.body,
    #                                       score=comment.score,
    #                                       submission_id=comment.link_id)
    #                 self._comment_repository.input_comment(new_comment)
    #             except SQLAlchemyError as err:
    #                 error = str(err.__dict__['orig'])
    #                 logger.exception(f"Comment with id {comment.id} not successfully added to the database. "
    #                                  f"Error: {error}")
    #             else:
    #                 self.count_mentions_and_populate_table(comment.body, comment_datetime, comment.id, True)

    def _scrape_submission_by_id(self, submission_id) -> None:
        """
        Get submission by id and input it into the database.

        Count mentions accordingly.

        Note: this function should only be called if the comments were retrieved
        before the submission is. The submission will then be retrieved before
        inputting the comment into the table to maintain database integrity
        (foreign keys constraints).
        """
        submission = self._reddit.submission(id=submission_id)
        sub_datetime = datetime.fromtimestamp(submission.created_utc).strftime(datetime_fmt)
        try:
            new_submission = Submission(submission_id=submission_id, dt=sub_datetime,
                                        selftext=submission.selftext, title=submission.title)
            self._submission_repository.input_submission(new_submission)
        except SQLAlchemyError as err:
            error = str(err.__dict__['orig'])
            logger.exception(f"Submission with id {submission.id} not successfully added to the database. "
                             f"Error: {error}")

    def count_mentions_and_populate_table(self, text: str,
                                          dt: str, link_id: str, from_comment: bool) -> None:
        """
        Given a text body (of a comment or of a submission), find out what companies were mentioned.

        Note: Multiple mentions of the same company in the same text body is considered one mention.
        """
        all_name_variations = self._stock_repository.find_all_name_variations()
        for name in all_name_variations:
            print(name)


    def get_live_comments(self):
        """
        Retrieve all live comments from self.subreddit.

        If the submission that the comment belongs to has not been inputted into the database,
        retrieve that submission too.
        """
        pass


if __name__ == "__main__":
    scraper = RedditScraper("learnpython")
    # start_date = int(datetime(2020, 1, 1).timestamp())
    # end_date = int(datetime(2020, 1, 2).timestamp())

    # print(scraper.scrape_submissions_between(start_date, end_date))
