import pytest
from unittest.mock import patch, MagicMock
from PIL import Image


# ─── _trim_messages ──────────────────────────────────────────────

class TestTrimMessages:
    def test_empty_list(self):
        from gigachatapi import _trim_messages
        assert _trim_messages([]) == []

    def test_short_history_not_trimmed(self):
        from gigachatapi import _trim_messages
        msgs = [
            {"role": "user", "content": "Привет"},
            {"role": "assistant", "content": "Здравствуйте"},
        ]
        result = _trim_messages(msgs)
        assert len(result) == 2

    def test_long_history_trimmed(self):
        from gigachatapi import _trim_messages
        # ~20000 символов — больше лимита 4000*4=16000
        msgs = [
            {"role": "user", "content": "А" * 5000},
            {"role": "assistant", "content": "Б" * 5000},
            {"role": "user", "content": "В" * 5000},
            {"role": "assistant", "content": "Г" * 5000},
        ]
        result = _trim_messages(msgs)
        assert len(result) < 4

    def test_preserves_order(self):
        from gigachatapi import _trim_messages
        msgs = [
            {"role": "user", "content": "Один"},
            {"role": "assistant", "content": "Два"},
            {"role": "user", "content": "Три"},
        ]
        result = _trim_messages(msgs)
        assert [m["content"] for m in result] == ["Один", "Два", "Три"]


# ─── is_image_request ────────────────────────────────────────────

class TestIsImageRequest:
    def test_naarissuj(self):
        from gigachatapi import is_image_request
        assert is_image_request("нарисуй кота") is True

    def test_cartinku(self):
        from gigachatapi import is_image_request
        assert is_image_request("сгенерируй картинку") is True

    def test_plain_text(self):
        from gigachatapi import is_image_request
        assert is_image_request("расскажи про Python") is False

    def test_case_insensitive(self):
        from gigachatapi import is_image_request
        assert is_image_request("НАРИСУЙ собаку") is True


# ─── get_access_token ────────────────────────────────────────────

class TestGetAccessToken:
    @patch("gigachatapi.requests.post")
    def test_success(self, mock_post):
        from gigachatapi import get_access_token
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"access_token": "tok_123"}
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        token = get_access_token()
        assert token == "tok_123"

    @patch("gigachatapi.requests.post")
    def test_failure(self, mock_post):
        from gigachatapi import get_access_token
        mock_post.side_effect = Exception("Network error")

        token = get_access_token()
        assert token is None


# ─── send_prompt ─────────────────────────────────────────────────

class TestSendPrompt:
    @patch("gigachatapi.generate_image")
    def test_image_request_delegates(self, mock_gen):
        from gigachatapi import send_prompt
        mock_gen.return_value = Image.new("RGB", (10, 10))

        result = send_prompt(
            [{"role": "user", "content": "нарисуй кота"}],
            "tok_123"
        )
        mock_gen.assert_called_once_with("нарисуй кота", "tok_123")
        assert isinstance(result, Image.Image)

    @patch("gigachatapi.requests.post")
    def test_text_request(self, mock_post):
        from gigachatapi import send_prompt
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": "Ответ модели"}}]
        }
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = send_prompt(
            [{"role": "user", "content": "Привет"}],
            "tok_123"
        )
        assert result == "Ответ модели"

    @patch("gigachatapi.requests.post")
    def test_api_error_returns_none(self, mock_post):
        from gigachatapi import send_prompt
        mock_post.side_effect = Exception("Timeout")

        result = send_prompt(
            [{"role": "user", "content": "Привет"}],
            "tok_123"
        )
        assert result is None
