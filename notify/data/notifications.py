from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from notify.model import Notification
from user.model import User


# @capture_stderr()
def read_all(
    session: Session,
    user_id: int,
) -> Sequence[Notification]:

    query = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created.desc())
    )

    rslt = session.scalars(query).all()
    return rslt


def create(
    session: Session,
    note: Notification,
) -> Notification:

    # raise an exception if the user does not exist
    session.query(User).filter(User.id == note.user_id).one()

    session.add(note)
    session.commit()
    session.refresh(note)

    return note


def update_notification_as_read(session: Session, notification_id: int) -> Notification:
    note = session.query(Notification).where(Notification.id == notification_id).one()
    note.is_read = True
    session.add(note)
    session.commit()
    session.refresh(note)
    return note
