from supermemo2 import first_review, review

from domain.entities.entities import WordReview


class SupermemoService:

    def first_review(self, quality: int, word_review: WordReview):
        self.check_quality(quality)
        r = first_review(quality)
        word_review.easiness = r["easiness"]
        word_review.interval = r["interval"]
        word_review.repetitions = r["repetitions"]
        word_review.review_datetime = r["review_datetime"]
        return word_review

    def review(self, quality: int, word_review: WordReview) -> WordReview:
        self.check_quality(quality)
        r = review(quality, word_review.easiness, word_review.interval, word_review.repetitions)
        word_review.easiness = r["easiness"]
        word_review.interval = r["interval"]
        word_review.repetitions = r["repetitions"]
        word_review.review_datetime = r["review_datetime"]
        return word_review

    def check_quality(self, quality: int):
        if quality < 0 or quality > 5:
            raise ValueError("Invalid quality value")
