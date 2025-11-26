from collections.abc import Iterable, Set, Hashable, Mapping
from os import getenv, environ, PathLike
from pathlib import Path
from typing import Literal, Any
import uuid

from beartype import beartype
from msgspec import json

from .datatypes import AzureMessageCountType, AzureMessageType


def check_all_arguments_are_none_or_not(
    *args,
) -> bool:

    """
    Check if all provided arguments are either None or not None.

    Args:
        *args: A variable number of arguments to check.

    Returns:
        bool: True if all arguments are None or all are not None; False otherwise.
    """

    all_none = [arg is None for arg in args]
    return not (any(all_none) and (not all(all_none)))


@beartype
def strip_token_count(
    message: AzureMessageCountType,
) -> AzureMessageType:

    """
    Strips the token count from a single Azure message.

    Args:
        message (AzureMessageCountType): A message containing a role and content, along with a token count.

    Returns:
        AzureMessageType: A message containing only the role and content.

    Example:
        >>> message = {'role': 'user', 'content': 'Hello, world!', 'token_count': 5}
        >>> stripped_message = strip_token_count(message)
        >>> print(stripped_message)
        {'role': 'user', 'content': 'Hello, world!'}
    """

    return AzureMessageType(
        role = message['role'],
        content = message['content'],
    )

@beartype
def strip_token_counts(
    messages: Iterable[AzureMessageCountType],
) -> list[AzureMessageType]:

    """
    Strips the token counts from a list of Azure messages.

    Args:
        messages (Iterable[AzureMessageCountType]): An iterable of messages, each containing a role, content, and token count.

    Returns:
        List[AzureMessageType]: A list of messages containing only the role and content.

    Example:
        >>> messages = [
        ...     {'role': 'user', 'content': 'Hello!', 'token_count': 3},
        ...     {'role': 'assistant', 'content': 'Hi there!', 'token_count': 4}
        ... ]
        >>> stripped_messages = strip_token_counts(messages)
        >>> print(stripped_messages)
        [{'role': 'user', 'content': 'Hello!'}, {'role': 'assistant', 'content': 'Hi there!'}]
    """

    return [*map(strip_token_count, messages)]