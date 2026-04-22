import pytest
from unittest.mock import patch, Mock
from tenacity import RetryError
from fetcher import fetch


class TestFetch:
    def test_fetch_success(self):
        mock_response = Mock()
        mock_response.json.return_value = [{"id": 1, "name": "Ivan"}]
        mock_response.raise_for_status.return_value = None

        with patch("fetcher.requests.get", return_value=mock_response):
            result = fetch("users")

        assert result == [{"id": 1, "name": "Ivan"}]

    def test_fetch_raises_after_retries(self):
        """После исчерпания попыток tenacity бросает RetryError."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")

        with patch("fetcher.requests.get", return_value=mock_response):
            with pytest.raises(RetryError):
                fetch("nonexistent")

    def test_fetch_calls_correct_url(self):
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None

        with patch("fetcher.requests.get", return_value=mock_response) as mock_get:
            fetch("users")

        mock_get.assert_called_once()
        call_url = mock_get.call_args[0][0]
        assert "users" in call_url
