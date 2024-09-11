from enum import StrEnum


class WithdrawalOperationStatus(StrEnum):
    SUCCESSFULLY = 'SUCCESSFULLY'
    FAILURE = 'FAILURE'
    NOT_ENOUGH_RESOURCES = 'NOT_ENOUGH_RESOURCES'

class ReplenishmentOperationStatus(StrEnum):
    SUCCESSFULLY = 'SUCCESSFULLY'
    FAILURE = 'FAILURE'