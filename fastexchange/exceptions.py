class BaseFinancialException(Exception):
    ...


class CantCompareException(BaseFinancialException):
    """Cannot compare two different currencies"""


class ConverterNotMapped(BaseFinancialException):
    """Converter Client does not support requested spefiec exchange"""
