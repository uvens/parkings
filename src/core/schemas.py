from __future__ import annotations

from typing import Union

from pydantic import BaseModel

from phonenumbers import PhoneNumber as _PhoneNumber
from phonenumbers import NumberParseException, PhoneNumberFormat
from phonenumbers import format_number, is_possible_number, parse


class PhoneNumber(_PhoneNumber):
    @classmethod
    def __get_validators__(cls): # noqa
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, PhoneNumber]) -> _PhoneNumber: # noqa
        if isinstance(v, _PhoneNumber):
            return v
        try:
            number = parse(v, 'RU')
        except NumberParseException as ex:
            raise ValueError(f'Invalid phone number: {v}') from ex
        if not is_possible_number(number):
            raise ValueError(f'Invalid phone number: {v}')
        return number

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None: # noqa
        field_schema.update(
            type='string',
            # pattern='^SOMEPATTERN?$',
            examples=['+49123456789'],
        )

    def json_encode(self) -> str:
        return format_number(self, PhoneNumberFormat.E164)


class BaseSchema(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        min_anystr_length = 0
        orm_mode = True


class PhoneNumberSchema(BaseSchema):
    region: str
    national: str
    international: str
    e164: str
