# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import sys
from os import linesep
from knack.util import CLIError
from azext_iot.constants import EVENT_LIB, VERSION
from azext_iot.common.utility import test_import
from azext_iot.common.config import get_uamqp_ext_version, update_uamqp_ext_version
from azext_iot.common.pip import install
from azext_iot.common._homebrew_patch import HomebrewPipPatch
from azure.cli.core._profile import Profile
from azure.cli.core.mock import DummyCli
from azext_iot.tests.settings import UserTypes


def ensure_uamqp(config, yes=False, repair=False):
    if get_uamqp_ext_version(config) != EVENT_LIB[1] or repair or not test_import(EVENT_LIB[0]):
        profile = Profile(cli_ctx=DummyCli())
        subscription = profile.get_subscription()
        user = subscription["user"]

        # System user cannot provide input so interactive flow is skipped and dependency is updated
        if not yes and user["type"] != UserTypes.servicePrincipal.value:
            input_txt = ('Dependency update ({} {}) required for IoT extension version: {}. {}'
                         'Continue? (y/n) -> ').format(EVENT_LIB[0], EVENT_LIB[1], VERSION, linesep)
            i = input(input_txt)
            if i.lower() != 'y':
                sys.exit('User has declined update...')

        print('Updating required dependency...')
        with HomebrewPipPatch():
            # The version range defined in this custom_version parameter should be stable
            try:
                install(EVENT_LIB[0], compatible_version='{}'.format(EVENT_LIB[1]))
                update_uamqp_ext_version(config, EVENT_LIB[1])
                print('Update complete. Executing command...')
            except RuntimeError as e:
                print('Failure updating {}. Aborting...'.format(EVENT_LIB[0]))
                raise CLIError(e)
