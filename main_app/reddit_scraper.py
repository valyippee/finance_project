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
        self._comment_repository = CommentRepository(init_engine)
        self._submission_repository = SubmissionRepository(init_engine)
        self._mention_repository = MentionRepository(init_engine)

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
                self._scrape_submission(submission)
                self.count_mentions_and_populate_table(submission.title + submission.selftext,
                                                       datetime.fromtimestamp(submission.created_utc).strftime(datetime_fmt),
                                                       submission.id, False)

    def scrape_comments_between(self, start_date, end_date) -> None:
        """
        Get submissions after the given datetime and
        input those submissions into the database.

        Count mentions and update them into the database too.
        """
        comments = self._api.search_comments(after=start_date,
                                             before=end_date,
                                             subreddit=self.subreddit, limit=1)
        for comment in comments:
            if self._submission_repository.find_by_id(comment.link_id) is None:
                submission = self._reddit.submission(id=comment.link_id)
                self._scrape_submission(submission)
            if self._comment_repository.find_by_id(comment.id) is None:
                self._scrape_comment(comment)
                self.count_mentions_and_populate_table(comment.body,
                                                       datetime.fromtimestamp(comment.created_utc).strftime(datetime_fmt),
                                                       comment.id,
                                                       True)

    def _scrape_submission(self, submission) -> None:
        """
        Input a submission (praw object) into the database.
        """
        sub_datetime = datetime.fromtimestamp(submission.created_utc).strftime(datetime_fmt)
        try:
            new_submission = Submission(submission_id=submission.id, dt=sub_datetime,
                                        selftext=submission.selftext, title=submission.title)
            self._submission_repository.input_submission(new_submission)
        except SQLAlchemyError as err:
            error = str(err.__dict__['orig'])
            logger.exception(f"Submission with id {submission.id} not successfully added to the database. "
                             f"Error: {error}")

    def _scrape_comment(self, comment) -> None:
        """
        Input a comment (praw object) into the database.
        """
        comment_datetime = datetime.fromtimestamp(comment.created_utc).strftime(datetime_fmt)
        try:
            new_comment = Comment(comment_id=comment.id,
                                  dt=comment_datetime,
                                  body=comment.body,
                                  score=comment.score,
                                  submission_id=comment.link_id)
            self._comment_repository.input_comment(new_comment)
        except SQLAlchemyError as err:
            error = str(err.__dict__['orig'])
            logger.exception(f"Comment with id {comment.id} not successfully added to the database. "
                             f"Error: {error}")

    def count_mentions_and_populate_table(self, text: str,
                                          dt: str, link_id: str, from_comment: bool) -> None:
        """
        Given a text body (of a comment or of a submission), find out what companies were mentioned.

        Note: Multiple mentions of the same company in the same text body is considered one mention.
        """
        all_name_variations = self._stock_repository.find_all_name_variations()
        for name_variations, in all_name_variations:
            for name in name_variations:
                if name in text:
                    stock_id = self._stock_repository.find_by_ticker(name_variations[0]).id
                    if from_comment:
                        comment_id, submission_id = link_id, None
                    else:
                        comment_id, submission_id = None, link_id
                    try:
                        new_mention = Mention(stock_id=stock_id, dt=dt,
                                              comment_id=comment_id, submission_id=submission_id,
                                              from_comment=from_comment)
                        self._mention_repository.input_mention(new_mention)
                    except SQLAlchemyError as err:
                        error = str(err.__dict__['orig'])
                        if from_comment:
                            logger.exception(f"Mention with stock_id {stock_id}, comment_id {link_id}, "
                                             f"and datetime {dt} not successfully added to the database. "
                                             f"Error: {error}")
                        else:
                            logger.exception(
                                f"Mention with stock_id {stock_id}, submission_id {link_id}, "
                                f"and datetime {dt} not successfully added to the database. "
                                f"Error: {error}")
                    break

    def get_live_comments_and_submissions(self):
        """
        Retrieve all live comments from self.subreddit.

        If the submission that the comment belongs to has not been inputted into the database,
        retrieve that submission too.
        """
        logger.info("Reddit Scraper comments stream started at " + datetime.now().strftime(datetime_fmt))

        for comment in self._praw_subreddit.stream.comments():
            # scrape submission first, if it has not been scraped
            if self._submission_repository.find_by_id(comment.link_id) is None:
                submission = self._reddit.submission(id=comment.link_id)
                self._scrape_submission(submission)
            # scrape the comment
            if self._comment_repository.find_by_id(comment.id) is None:
                self._scrape_comment(comment)

        logger.info("Reddit Scraper comments stream ended at " + datetime.now().strftime(datetime_fmt))


if __name__ == "__main__":
    scraper = RedditScraper("wallstreetbets", engine)
    # start_date = int(datetime(2020, 1, 1).timestamp())
    # end_date = int(datetime(2020, 1, 2).timestamp())
