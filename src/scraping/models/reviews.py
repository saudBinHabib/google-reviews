from dataclasses import dataclass, field

@dataclass(frozen=True)
class Review:
    reviewer_name: str = field()
    review_time: str = field()
    review: str = field(compare=False, hash=False)
    rating: int = field()
    reply: bool = field()
    reply_text: str = field(compare=False, hash=False)
    review_link: str = field()