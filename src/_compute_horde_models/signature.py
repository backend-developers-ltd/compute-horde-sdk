import abc
import base64
import hashlib
import json
import re
import time
import typing
from typing import ClassVar

import bittensor
from pydantic import BaseModel, JsonValue, field_serializer, field_validator


class Signature(BaseModel, extra="forbid"):
    # has defaults to allow easy instantiation
    signature_type: str = ""
    signatory: str = ""  # identity of the signer (e.g. sa58 address if signature_type == "bittensor")
    timestamp_ns: int = 0  # UNIX timestamp in nanoseconds
    signature: bytes

    @field_validator("signature")
    @classmethod
    def validate_signature(cls, signature: str) -> bytes:
        return base64.b64decode(signature)

    @field_serializer("signature")
    def serialize_signature(self, signature: bytes) -> str:
        return base64.b64encode(signature).decode("utf-8")


class SignedFields(BaseModel):
    executor_class: str
    docker_image: str
    raw_script: str
    args: str
    env: dict[str, str]
    use_gpu: bool

    volumes: list[JsonValue]
    uploads: list[JsonValue]

    @staticmethod
    def from_facilitator_sdk_json(data: JsonValue):
        data = typing.cast(dict[str, JsonValue], data)

        signed_fields = SignedFields(
            executor_class=str(data.get("executor_class")),
            docker_image=str(data.get("docker_image", "")),
            raw_script=str(data.get("raw_script", "")),
            args=str(data.get("args", "")),
            env=typing.cast(dict[str, str], data.get("env", None)),
            use_gpu=typing.cast(bool, data.get("use_gpu")),
            volumes=typing.cast(list[JsonValue], data.get("volumes", [])),
            uploads=typing.cast(list[JsonValue], data.get("uploads", [])),
        )
        return signed_fields


def signature_to_headers(signature: Signature, prefix: str = "X-CH-") -> dict[str, str]:
    """
    Converts the signature to headers

    :param signature: Signature object
    :return: headers dict
    """
    return {
        f"{prefix}Signature-Type": signature.signature_type,
        f"{prefix}Signatory": signature.signatory,
        f"{prefix}Timestamp-NS": str(signature.timestamp_ns),
        f"{prefix}Signature": base64.b64encode(signature.signature).decode("utf-8"),
    }


def hash_message_signature(payload: bytes | JsonValue, signature: Signature) -> bytes:
    """
    Hashes the message to be signed with the signature parameters

    :param payload: payload to be signed
    :param signature: incomplete signature object with Signature parameters
    :return:
    """
    if not isinstance(payload, bytes):
        payload = json.dumps(payload, sort_keys=True).encode("utf-8")

    hasher = hashlib.blake2b()
    hasher.update(signature.timestamp_ns.to_bytes(8, "big"))
    hasher.update(payload)
    return hasher.digest()


_REMOVE_URL_SCHEME_N_HOST_RE = re.compile(r"^\w+://[^/]+")


def signature_payload(method: str, url: str, headers: dict[str, str], json: JsonValue | None = None) -> JsonValue:
    reduced_url = _REMOVE_URL_SCHEME_N_HOST_RE.sub("", url)
    return {
        "action": f"{method.upper()} {reduced_url}",
        "json": json,
    }


class SignatureScheme(abc.ABC):
    signature_type: ClassVar[str]

    def payload_from_request(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        json: JsonValue | None = None,
    ):
        return signature_payload(
            method=method,
            url=url,
            headers=headers,
            json=json,
        )


class Signer(SignatureScheme):
    def sign(self, payload: JsonValue | bytes) -> Signature:
        signature = Signature(
            signature_type=self.signature_type,
            signatory=self.get_signatory(),
            timestamp_ns=time.time_ns(),
            signature=b"",
        )
        payload_hash = hash_message_signature(payload, signature)
        signature.signature = self._sign(payload_hash)
        return signature

    def signature_for_request(
        self, method: str, url: str, headers: dict[str, str], json: JsonValue | None = None
    ) -> Signature:
        return self.sign(self.payload_from_request(method, url, headers=headers, json=json))

    @abc.abstractmethod
    def _sign(self, payload: bytes) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    def get_signatory(self) -> str:
        raise NotImplementedError


class BittensorWalletSigner(Signer):
    signature_type = "bittensor"

    def __init__(self, wallet: bittensor.wallet | bittensor.Keypair | None = None):
        if isinstance(wallet, bittensor.Keypair):
            keypair = wallet
        else:
            keypair = (wallet or bittensor.wallet()).hotkey
        self._keypair = keypair

    def _sign(self, payload: bytes) -> bytes:
        signature: bytes = self._keypair.sign(payload)
        return signature

    def get_signatory(self) -> str:
        signatory: str = self._keypair.ss58_address
        return signatory
