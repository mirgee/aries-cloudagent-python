"""An object for containing the connection request/response DID information."""

from marshmallow import EXCLUDE, fields
from peerdid.dids import DIDDocument
from .....connections.models.diddoc import LegacyDIDDoc
from .....messaging.models.base import BaseModel, BaseModelSchema
<<<<<<< HEAD
from .....messaging.valid import ANY_DID_EXAMPLE, ANY_DID_VALIDATE
>>>>>>> main


class DIDDocWrapper(fields.Field):
    """Field that loads and serializes DIDDoc."""

    def _serialize(self, value, attr, obj, **kwargs):
        """
        Serialize the DIDDoc.

        Args:
            value: The value to serialize

        Returns:
            The serialized LegacyDIDDoc

        """
        return value.serialize()

    def _deserialize(self, value, attr=None, data=None, **kwargs):
        """
        Deserialize a value into a LegacyDIDDoc.

        Args:
            value: The value to deserialize

        Returns:
            The deserialized value
        """
        dd = None
        if value["id"].startswith("did:peer:2"):
            dd = DIDDocument.deserialize(value)
        else:  # if sov
            dd = LegacyDIDDoc.deserialize(value)
        return dd


class ConnectionDetail(BaseModel):
    """Class representing the details of a connection."""

    class Meta:
        """ConnectionDetail metadata."""

        schema_class = "ConnectionDetailSchema"

    def __init__(self, *, did: str = None, did_doc: DIDDocument = None, **kwargs):
        """
        Initialize a ConnectionDetail instance.

        Args:
            did: DID for the connection detail
            did_doc: DIDDoc for connection detail

        """
        super().__init__(**kwargs)
        self._did = did
        self._did_doc = did_doc

    @property
    def did(self) -> str:
        """
        Accessor for the connection DID.

        Returns:
            The DID for this connection

        """
        return self._did

    @property
    def did_doc(self) -> LegacyDIDDoc:
        """
        Accessor for the connection DID Document.

        Returns:
            The DIDDoc for this connection

        """
        return self._did_doc


class ConnectionDetailSchema(BaseModelSchema):
    """ConnectionDetail schema."""

    class Meta:
        """ConnectionDetailSchema metadata."""

        model_class = ConnectionDetail
        unknown = EXCLUDE

    did = fields.Str(
        data_key="DID",
        required=False,
        validate=ANY_DID_VALIDATE,
        metadata={
            "description": "DID for connection detail",
            "example": ANY_DID_EXAMPLE,
        },
    )
    # JS this could accept DIDDocWrapper OR another wrapper of peerdid.dids.DIDDocument
    did_doc = DIDDocWrapper(
        data_key="DIDDoc",
        required=False,
        metadata={
            "description": "DID document for connection detail",
        },
    )
