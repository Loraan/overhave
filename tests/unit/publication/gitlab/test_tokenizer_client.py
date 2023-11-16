from typing import Callable

import pytest
from faker import Faker
from pydantic import ValidationError

from overhave.publication import TokenizerClient
from overhave.publication.gitlab import TokenizerClientSettings
from overhave.publication.gitlab.tokenizer.client import InvalidUrlException, TokenizerRequestParamsModel


class TestTokenizerClient:
    """Tests for :class:`TokenizerClient`."""

    @pytest.mark.parametrize(
        ("initiator", "remote_key", "remote_key_name"),
        [("kek", None, "peka"), (None, "lol", "peka"), (None, None, "pepe")],
    )
    def test_tokenizer_settings_validation_raises_error(
        self, test_tokenizer_client_settings_factory: Callable[[], TokenizerClientSettings]
    ) -> None:
        with pytest.raises(ValidationError):
            test_tokenizer_client_settings_factory()

    @pytest.mark.parametrize(("initiator", "remote_key", "remote_key_name"), [("peka", "pepe", "sad-pepe")])
    def test_tokenizer_settings_validation_not_raises_error(
        self, test_tokenizer_client_settings_factory: Callable[[], TokenizerClientSettings]
    ) -> None:
        test_tokenizer_client_settings_factory()

    @pytest.mark.parametrize(("initiator", "remote_key", "id"), [("peka", "pepe", 1)])
    def test_tokenizer_request_params_model_get_params_successfully(
        self,
        test_tokenizer_request_params_model_factory: Callable[[], TokenizerRequestParamsModel],
        faker: Faker,
        initiator: str,
        remote_key: str,
        id: int,
    ) -> None:
        model = test_tokenizer_request_params_model_factory()
        remote_key_name = faker.word()
        params = model.get_request_params(remote_key_name)

        assert params == {"initiator": initiator, "id": id, remote_key_name: remote_key}

    @pytest.mark.parametrize(
        ("url", "initiator", "remote_key", "remote_key_name"), [(None, "lol", "pepe", "angry-pepe")]
    )
    def test_tokenizer_client_get_token_invalid_url(
        self, test_tokenizer_client_settings_disabled_factory: Callable[[], TokenizerClientSettings]
    ) -> None:
        settings = test_tokenizer_client_settings_disabled_factory()

        client = TokenizerClient(settings)

        with pytest.raises(InvalidUrlException):
            client.get_token(777)
