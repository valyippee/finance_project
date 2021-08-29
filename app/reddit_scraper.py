import praw
from psaw import PushshiftAPI
import config
from db.comment_repository import CommentRepository
from db.submission_repository import SubmissionRepository
from db.mention_repository import MentionRepository
from base_db import Comment, Submission, Mention
import datetime


class RedditScraper:
    """
    Uses praw to scrape data from reddit. Calls DB interface to store
    data into the database.

    === Private attributes ===
    _api: an instance of PushShiftAPI
    _subreddit: an authorized subreddit instance which is used to retrieve data
                from this subreddit
    _comment_repository: interacts with the comment table in the database
    _submission_repository: interacts with the submission table in the database
    _mention_repository: interacts with the mention table in the database
    """

    def __init__(self, subreddit: str):
        reddit = praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            password=config.password,
            user_agent=config.user_agent,
            username=config.username
        )

        # used for psaw
        self._api = PushshiftAPI()
        self.subreddit = subreddit

        # used for praw
        self._praw_subreddit = reddit.subreddit(subreddit)

        self._comment_repository = CommentRepository()
        self._submission_repository = SubmissionRepository()
        self._mention_repository = MentionRepository()

    def get_submissions_between(self, start_date, end_date) -> None:
        """
        Get submissions after the given datetime and
        input those submissions into the database.

        Count mentions and update them into the database too.
        """
        submissions = self._api.search_submissions(after=start_date,
                                                   before=end_date,
                                                   subreddit=self.subreddit)
        for submission in submissions:
            print(submission)
            if self._submission_repository.find_by_id(submission.id) is not None:
                new_submission = Submission(submission_id=submission.id, dt=submission.created_utc,
                                            selftext=submission.selftext, title=submission.title)
                print(new_submission)
                self._submission_repository.input_submission(new_submission)
            # TODO: count mentions

    def get_comments_between(self, start_date, end_date) -> None:
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
                self._get_submission_by_id(comment.link_id)
            if self._comment_repository.find_by_id(comment.id) is not None:
                new_comment = Comment(comment_id=comment.id,
                                      dt=comment.created_utc,
                                      body=comment.body,
                                      score=comment.score,
                                      submission_id=comment.link_id)
                self._comment_repository.input_comment(new_comment)

            # TODO: count mentions

    def _get_submission_by_id(self, submission_id) -> None:
        """
        Get submission by id and input it into the database.

        Count mentions accordingly.

        Note: this function should only be called if the comments were retrieved
        before the submission is. The submission will be retrieved before
        inputting the comment into the table to maintain database integrity.
        """
        # TODO: find out how to find submission by id
        pass

    def count_mentions_and_populate_table(self, text: str) -> None:
        """
        Given a text body (of a comment or of a submission), find out how many mentions there are.

        Note: Multiple mentions of the same company in the same text body is considered one mention.
        """
        # TODO: write this function
        pass


if __name__ == "__main__":
    scraper = RedditScraper("learnpython")
    start_date = int(datetime.datetime(2020, 1, 1).timestamp())
    end_date = int(datetime.datetime(2020, 1, 2).timestamp())

    print(scraper.get_comments_between(start_date, end_date))

