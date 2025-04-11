from dataclasses import dataclass, field


@dataclass
class ValidationError:
    """Model for validation errors."""
    loc: list
    msg: str
    type: str


@dataclass
class HTTPValidationError:
    """Model for HTTP validation errors."""
    detail: list[ValidationError] = field(default_factory=list)
