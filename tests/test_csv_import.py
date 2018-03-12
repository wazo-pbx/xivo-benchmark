# -*- coding: utf-8 -*-
# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import os.path

from datetime import datetime, timedelta

from xivo_confd_client import Client

from . import constants

MAX_TIME = timedelta(seconds=120)

client = Client(constants.HOST,
                https=True,
                verify_certificate=False,
                port=9486,
                username='admin',
                password='proformatique')


def test_csv_import():
    start = datetime.now()
    result = upload_csv()
    stop = datetime.now()

    assert 'created' in result, 'Result should contains the created users:\n{}'.format(result)
    assert len(result['created']) == 100, 'Should have created 100 users\n{}'.format(result)
    assert stop - start <= MAX_TIME, "CSV import exceeded max time ({})".format(MAX_TIME)


def upload_csv():
    filepath = os.path.join(constants.ASSET_DIR, "100entries.csv")
    with open(filepath) as f:
        csvdata = f.read()
        return client.users.import_csv(csvdata)
