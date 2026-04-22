import logging

log = logging.getLogger(__name__)


def validate_user(user: dict) -> bool:
    required = {"id", "name", "username", "email", "company", "address"}
    if not required.issubset(user.keys()):
        return False
    if not isinstance(user["id"], int):
        return False
    if not isinstance(user.get("company"), dict):
        return False
    if not isinstance(user.get("address"), dict):
        return False
    return True


def validate_post(post: dict) -> bool:
    required = {"id", "userId", "title", "body"}
    if not required.issubset(post.keys()):
        return False
    if not isinstance(post["id"], int) or not isinstance(post["userId"], int):
        return False
    return True


def validate_comment(comment: dict) -> bool:
    required = {"id", "postId", "name", "email", "body"}
    if not required.issubset(comment.keys()):
        return False
    if not isinstance(comment["id"], int) or not isinstance(comment["postId"], int):
        return False
    return True


def validate_and_filter(
    records: list[dict],
    validator,
    entity: str,
) -> list[dict]:
    """Фильтрует записи прошедшие валидацию, логирует отброшенные."""
    valid = [r for r in records if validator(r)]
    invalid_count = len(records) - len(valid)
    if invalid_count:
        log.warning(f"{entity}: skipped {invalid_count} invalid record(s)")
    return valid