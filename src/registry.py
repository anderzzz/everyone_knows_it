"""Registry class

"""


class Registry:
    """A simple read-only registry class for content or file content.

    """
    def __init__(self, registry: dict, read: bool = False):
        self.registry = registry
        self.read = read

    def get(self, *keys) -> str:
        if not self.read:
            return self._get(*keys)
        else:
            with open(self._get(*keys), 'r') as f:
                return f.read()

    def _get(self, *keys) -> str:
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
            raise ValueError(f'Missing key `"{key}"` in registry. Full key set: {keys}. Check the registry.')
        return value
