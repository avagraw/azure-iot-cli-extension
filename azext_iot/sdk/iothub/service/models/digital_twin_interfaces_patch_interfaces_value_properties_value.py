# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DigitalTwinInterfacesPatchInterfacesValuePropertiesValue(Model):
    """DigitalTwinInterfacesPatchInterfacesValuePropertiesValue.

    :param desired:
    :type desired:
     ~service.models.DigitalTwinInterfacesPatchInterfacesValuePropertiesValueDesired
    """

    _attribute_map = {
        'desired': {'key': 'desired', 'type': 'DigitalTwinInterfacesPatchInterfacesValuePropertiesValueDesired'},
    }

    def __init__(self, **kwargs):
        super(DigitalTwinInterfacesPatchInterfacesValuePropertiesValue, self).__init__(**kwargs)
        self.desired = kwargs.get('desired', None)