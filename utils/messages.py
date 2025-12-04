from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MessageCode:
    CODE: str


class NormalMessages:
    GENERAL: dict[str, Any] = {}

    class SERVER:
        OK = MessageCode("NS001")
        LOGGED_OUT = MessageCode("NS002")
        LOGGED_IN = MessageCode("NS003")
        LOGGED_IN_CHALLENGE = MessageCode("NS004")


class ErrorMessages:
    class VALIDATION:
        REQUIRED_FIELD = MessageCode("EV001")
        INVALID_EMAIL = MessageCode("EV002")
        ITEM_NOT_FOUND = MessageCode("EV003")
        DISPLAY_ORDER_INVALID = MessageCode("EV004")
        METHOD_NOT_IMPLEMENTED = MessageCode("EV005")
        ALIAS_MUST_HAVE_4_TO_30_CHARACTERS = MessageCode("EV006")
        ALIAS_LAST_4_MUST_BE_4_DIGITS = MessageCode("EV007")
        ALIAS_ALREADY_EXISTS = MessageCode("EV008")
        INVALID_EMAIL_FORMAT = MessageCode("EV009")
        NAME_MUST_NOT_BE_EMPTY = MessageCode("EV010")
        DISPLAY_ORDER_INVALID = MessageCode("EV011")
        IMPOSIBLE_TO_CONVERT_ENTITY_TO_DICT = MessageCode("EV012")
        JWT_NOT_CONFIGURED_IN_ENV = MessageCode("EV015")
        CODE_MUST_BE_ALPHANUMERIC = MessageCode("EV017")
        INVALID_TAX_ID = MessageCode("EV018")
        TENANT_CODE_EXISTS = MessageCode("EV019")
        TENANT_EMAIL_ALREADY_EXISTS = MessageCode("EV020")
        TENANT_TAX_ID_EXISTS = MessageCode("EV021")
        NO_EVENTS_FOUND_FOR_VERIFICATION = MessageCode("EV022")
        ALIAS_NOT_FOUND = MessageCode("EV023")
        WORM_PRIVATE_KEY_INVALID = MessageCode("EV024")
        TENANT_NOT_FOUND = MessageCode("EV025")
        INVALID_ROUTING_CODE = MessageCode("EV026")

    class AUTH:
        UNAUTHORIZED = MessageCode("EA001")
        FORBIDDEN = MessageCode("EA002")
        ERROR_GENERATING_TOKEN = MessageCode("EA003")
        INVALID_TOKEN = MessageCode("EA004")
        TOKEN_NEED_TENANT_ID = MessageCode("EA005")
        TOKEN_EXPIRED = MessageCode("EA006")
        INVALID_CREDENTIALS = MessageCode("EA007")
        TENANT_INACTIVE = MessageCode("EA008")
        INVALID_API_KEY = MessageCode("EA009")
        TENANT_NOT_FOUND = MessageCode("EA010")
        TOKEN_REQUIRED = MessageCode("EA011")
        INVALID_AUTH_FORMAT = MessageCode("EA012")
        REGULATOR_ROLE_REQUIRED = MessageCode("EA013")
        CUB_PEPPER_NOT_SET = MessageCode("EA014")
        ALIAS_NOT_OWNED = MessageCode("EA015")


class MESSAGES:
    NORMAL = NormalMessages
    ERROR = ErrorMessages
