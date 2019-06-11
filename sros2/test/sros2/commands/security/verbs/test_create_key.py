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


def test_create_key():
    with tempfile.TemporaryDirectory() as keystore_dir:
        # First, create the keystore
        assert cli.main(argv=['security', 'create_keystore', keystore_dir]) == 0

        # Now using that keystore, create a keypair
        assert cli.main(argv=['security', 'create_key', keystore_dir, '/test_node']) == 0

        assert os.path.isdir(os.path.join(keystore_dir, 'test_node'))

        expected_files = [
            'cert.pem', 'permissions.xml', 'permissions_ca.cert.pem', 'request.cnf', 'req.pem',
            'permissions.p7s', 'key.pem', 'identity_ca.cert.pem', 'governance.p7s', 'ecdsaparam'
        ]
        for expected_file in expected_files:
            assert os.path.isfile(os.path.join(keystore_dir, 'test_node', expected_file))
