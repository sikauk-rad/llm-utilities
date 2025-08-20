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
def get_optimal_uintype(
    number: int | float,
) -> Literal['uint8', 'uint16', 'uint32', 'uint64', 'float32', 'float64']:

    """
    Return the optimal unsigned integer or float type for a given non-negative number.

    The function determines the smallest unsigned integer or float type that can
    represent the input number without loss of precision.

    Parameters
    ----------
    number : int or float
        The non-negative number to evaluate.

    Returns
    -------
    Literal['uint8', 'uint16', 'uint32', 'uint64', 'float32', 'float64']
        The name of the optimal unsigned integer or float type.

    Raises
    ------
    ValueError
        If the input number is negative.

    Examples
    --------
    >>> get_optimal_uintype(42)
    'uint8'
    >>> get_optimal_uintype(100000)
    'uint16'
    >>> get_optimal_uintype(1e10)
    'uint64'
    >>> get_optimal_uintype(1e40)
    'float64'
    """

    if number < 0:
        raise ValueError("Input number must be non-negative.")
    elif number <= 255:
        return 'uint8'
    elif number <= 65535:
        return 'uint16'
    elif number <= 4294967295:
        return 'uint32'
    elif number <= 18446744073709551615:
        return 'uint64'
    elif number <= 3.4028235e+38:
        return 'float32'
    else:
        return 'float64'


@beartype
def get_optimal_intype(
    number: int | float,
) -> Literal['int8', 'int16', 'int32', 'int64', 'float32', 'float64']:
    """
    Return the optimal signed integer or float type for a given number.

    The function determines the smallest signed integer or float type that can
    represent the input number without loss of precision.

    Parameters
    ----------
    number : int or float
        The number to evaluate.

    Returns
    -------
    Literal['int8', 'int16', 'int32', 'int64', 'float32', 'float64']
        The name of the optimal signed integer or float type.

    Examples
    --------
    >>> get_optimal_intype(42)
    'int8'
    >>> get_optimal_intype(-100)
    'int8'
    >>> get_optimal_intype(40000)
    'int16'
    >>> get_optimal_intype(1e10)
    'int64'
    >>> get_optimal_intype(1e40)
    'float64'
    """

    if number <= 127 and number >= -128:
        return 'int8'
    elif number <= 32767 and number >= -32768:
        return 'int16'
    elif number <= 2147483647 and number >= -2147483648:
        return 'int32'
    elif number <= 9223372036854775807 and number >= -9223372036854775808:
        return 'int64'
    elif number <= 3.4028235e+38 and number >= -3.4028235e+38:
        return 'float32'
    else:
        return 'float64'


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


def check_keys_not_missing(
    required_keys: Iterable[Hashable],
    mapping: Mapping,
    mapping_name: str | None = None,
) -> None:

    """
    Check if all required keys are present in the given mapping.

    Args:
        required_keys (Iterable[Hashable]): An iterable of keys that must be present in the mapping.
        mapping (Mapping[Hashable, Any]): The mapping (e.g., dictionary) to check against.
        mapping_name (Optional[str]): An optional name for the mapping, used in the error message.

    Raises:
        KeyError: If any required keys are missing from the mapping, an error is raised with a message indicating which keys are missing and from which mapping they are expected.
    """

    if not isinstance(required_keys, Set):
        required_keys = {*required_keys}
    missing_keys = required_keys - mapping.keys()
    if not missing_keys:
        return

    missing_keys_str = ", ".join([*map(str, missing_keys)])
    error_suffix = f' in {mapping_name}.' if mapping_name else '.'
    raise KeyError(f'missing keys {missing_keys_str}{error_suffix}')


def load_id_from_env(
    env_variable_name: str,
) -> uuid.UUID:

    """
    Load a UUID from an environment variable.

    Args:
        env_variable_name (str): The name of the environment variable that contains the UUID.

    Returns:
        uuid.UUID: The UUID loaded from the environment variable.

    Raises:
        KeyError: If the environment variable is not set.
        ValueError: If the value of the environment variable is not a valid UUID.
    """

    if env_variable_name not in environ.keys():
        raise KeyError(f'{env_variable_name} not found in environment variables.')
        
    try:
        return uuid.UUID(getenv(env_variable_name))
    except (TypeError, ValueError):
        raise ValueError(f'The value of {env_variable_name} not a valid UUID.')


def load_config_from_path(
    config_path: PathLike,
    required_keys: Iterable[str],
    config_uuid: uuid.UUID,
) -> dict[str, Any]:

    """
    Load configuration from a JSON file specified in an environment variable.

    Args:
        config_path (PathLike): The path to the configuration file, which must be a JSON.
        required_keys (Iterable[str]): A collection of keys that must be present in the configuration.
        config_uuid (uuid.UUID): The UUID to load the configuration for.

    Returns:
        dict: The configuration corresponding to the provided UUID.

    Raises:
        FileNotFoundError: If the config_path file does not exist.
        TypeError: If the specified file is not a JSON file.
        KeyError: If the config_uuid is not found in the configuration or if required keys are missing.
    """

    if not isinstance(config_path, Path):
        config_path = Path(config_path)

    if not config_path.is_file():
        raise FileNotFoundError(
            f'{config_path} not found.'
        )

    elif config_path.suffix != '.json':
        raise TypeError(
            f'{config_path} must be a .json file.'
        )

    with open(file=config_path, mode='rb') as configs_bytesio:
        configs = json.decode(configs_bytesio.read())

    for config_uuid_, config in configs.items():
        try:
            config_uuid_ = uuid.UUID(config_uuid_)
        except (ValueError, TypeError):
            continue
    
        if config_uuid == config_uuid_:
            break
    else:
        raise KeyError(f'config_uuid {config_uuid} not found as key in app_config.')

    check_keys_not_missing(
        required_keys = required_keys,
        mapping = config,
        mapping_name = 'config'
    )

    return config