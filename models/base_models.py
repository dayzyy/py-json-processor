class Model:
    def __init__(self, **kwargs) -> None:
        cls = self.__class__
        expected_attrs = cls.__annotations__

        missing = [key for key in expected_attrs if key not in kwargs]
        if missing:
            plural = 's' if len(missing) > 1 else ''
            raise ValueError(f"Missing attribute{plural} {missing} when instantiating class {cls.__name__!r}")

        for key, value in kwargs.items():
            if key not in expected_attrs.keys():
                raise ValueError(f"Unexpected attribute {key!r} when instantiating class {cls.__name__!r}")

            if not isinstance(value, expected_attrs[key]):
                raise TypeError(
                    f"Invalid type for attribute {key!r} when instantiating class {cls.__name__!r}: "
                    f"expected {expected_attrs[key]!r}, got {type(value)!r}"
                )

            setattr(self, key, value)
