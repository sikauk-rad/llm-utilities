from enum import StrEnum
from typing import TypedDict


class Role(StrEnum):
    """
    Enum representing the possible roles in a conversation.

    Attributes:
        SYSTEM: The system role, typically used for system-level instructions or prompts.
        ASSISTANT: The assistant role, representing the AI or chatbot.
        USER: The user role, representing the end user interacting with the assistant.
    """
    SYSTEM = 'system'
    ASSISTANT = 'assistant'
    USER = 'user'


class AzureMessageType(TypedDict):
    """
    TypedDict representing a message in a conversation, including its role and content.

    Attributes:
        role (Role): The role of the message sender (system, assistant, or user).
        content (str): The textual content of the message.
    """
    role: Role
    content: str


class AzureMessageCountType(TypedDict):
    """
    TypedDict representing a message in a conversation, including its role, content, and token count.

    Attributes:
        role (Role): The role of the message sender (system, assistant, or user).
        content (str): The textual content of the message.
        tokens (int): The number of tokens in the content.
    """
    role: Role
    content: str
    tokens: int


class AzureMessageIDType(TypedDict):
    """
    TypedDict representing a message in a conversation, including its role, content, and unique ID.

    Attributes:
        role (Role): The role of the message sender (system, assistant, or user).
        content (str): The textual content of the message.
        id (int): A unique identifier for the message.
    """
    role: Role
    content: str
    id: int


class AzureMessageIDCountType(TypedDict):
    """
    TypedDict representing a message in a conversation, including its role, content, and unique ID.

    Attributes:
        role (Role): The role of the message sender (system, assistant, or user).
        content (str): The textual content of the message.
        id (int): A unique identifier for the message.
        tokens (int): The number of tokens in the content.
    """
    role: Role
    content: str
    id: int
    tokens: int