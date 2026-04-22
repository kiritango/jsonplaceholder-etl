import pytest
from validator import validate_user, validate_post, validate_comment, validate_and_filter

VALID_USER = {
    "id": 1, "name": "Ivan", "username": "ivan", "email": "i@i.ru",
    "phone": "123", "website": "i.ru",
    "company": {"name": "Co"},
    "address": {"street": "Lenina 1", "city": "Moscow"},
}

VALID_POST = {"id": 1, "userId": 1, "title": "Title", "body": "Body"}
VALID_COMMENT = {"id": 1, "postId": 1, "name": "Name", "email": "e@e.ru", "body": "Body"}


class TestValidateUser:
    def test_valid(self):
        assert validate_user(VALID_USER) is True

    def test_missing_field(self):
        user = {**VALID_USER}
        del user["email"]
        assert validate_user(user) is False

    def test_invalid_id_type(self):
        assert validate_user({**VALID_USER, "id": "abc"}) is False

    def test_company_not_dict(self):
        assert validate_user({**VALID_USER, "company": "Co"}) is False

    def test_address_not_dict(self):
        assert validate_user({**VALID_USER, "address": "Lenina"}) is False


class TestValidatePost:
    def test_valid(self):
        assert validate_post(VALID_POST) is True

    def test_missing_field(self):
        post = {**VALID_POST}
        del post["title"]
        assert validate_post(post) is False

    def test_invalid_id_type(self):
        assert validate_post({**VALID_POST, "id": "abc"}) is False


class TestValidateComment:
    def test_valid(self):
        assert validate_comment(VALID_COMMENT) is True

    def test_missing_field(self):
        comment = {**VALID_COMMENT}
        del comment["postId"]
        assert validate_comment(comment) is False


class TestValidateAndFilter:
    def test_filters_invalid(self):
        records = [VALID_USER, {"id": "bad"}]
        result = validate_and_filter(records, validate_user, "users")
        assert len(result) == 1

    def test_all_valid(self):
        records = [VALID_USER]
        result = validate_and_filter(records, validate_user, "users")
        assert len(result) == 1

    def test_all_invalid(self):
        records = [{"id": "bad"}]
        result = validate_and_filter(records, validate_user, "users")
        assert len(result) == 0
