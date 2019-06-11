# Copyright 2019 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile

from ros2cli import cli


def test_create_keystore():
    with tempfile.TemporaryDirectory() as keystore_dir:
        assert cli.main(argv=['security', 'create_keystore', keystore_dir]) == 0
        expected_files = [
            'governance.p7s', 'index.txt', 'ca.cert.pem', 'ca_conf.cnf', 'ecdsaparam',
            'governance.xml', 'ca.key.pem', 'serial'
        ]
        for expected_file in expected_files:
            assert os.path.isfile(os.path.join(keystore_dir, expected_file))
