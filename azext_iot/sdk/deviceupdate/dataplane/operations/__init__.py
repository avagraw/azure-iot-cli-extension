# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator (autorest: 3.9.2, generator: @autorest/python@5.19.0)
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._device_update_operations import DeviceUpdateOperations
from ._device_management_operations import DeviceManagementOperations

from ._patch import __all__ as _patch_all
from ._patch import *  # type: ignore # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk
__all__ = [
    'DeviceUpdateOperations',
    'DeviceManagementOperations',
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()