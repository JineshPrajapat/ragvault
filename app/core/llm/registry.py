class LLMRegistry:
    _providers: dict[str, type] = {}

    @classmethod
    def register(cls, name: str, provider_cls: type):
        cls._providers[name] = provider_cls

    @classmethod
    def get(cls, name: str):
        provider_cls  = cls._providers.get(name)
        if not provider_cls :
            raise ValueError(f"Provider '{name}' not registered.")
        return provider_cls()