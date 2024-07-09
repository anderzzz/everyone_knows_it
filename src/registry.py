"""Registry class

"""


class Registry:
    """A simple read-only registry class for file content.

    """
    def __init__(self, registry: dict):
        self.registry = registry

    def get(self, *keys) -> str:
        """Get value from registry by one or several keys.

        Args:
            *keys: str
                One or several keys to traverse the registry.

        Returns:
            The text data

        """
        if len(keys) == 0:
            raise ValueError('At least one key must be provided')

        value = self.registry
        try:
            for key in keys:
                value = value[key]
        except KeyError:
            raise ValueError(f'Error at key `"{key}"` in keys: {keys}. Check the registry.')

        with open(value, 'r') as f:
            return f.read()
