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

import configparser
import os
import tempfile
from xml.etree import ElementTree

from ros2cli import cli


def test_create_keystore():
    def check_governance_p7s(generated_file):
        # TODO
        pass

    def check_index_txt(generated_file):
        lines = generated_file.readlines()
        assert len(lines) == 0

    def check_ca_cert_pem(generated_file):
        lines = generated_file.readlines()
        assert lines[0] == '-----BEGIN CERTIFICATE-----\n'
        assert lines[-1] == '-----END CERTIFICATE-----\n'

    def check_ca_conf(generated_file):
        config = configparser.ConfigParser()
        config.read_file(generated_file)
        assert config.sections() == [
            ' ca ',
            ' CA_default ',
            ' policy_match ',
            ' local_ca_extensions ',
            ' req ',
            ' req_distinguished_name ',
            ' root_ca_extensions ',
        ]

    def check_ecdsaparam(generated_file):
        lines = generated_file.readlines()
        assert lines[0] == '-----BEGIN EC PARAMETERS-----\n'
        assert lines[-1] == '-----END EC PARAMETERS-----\n'

    def check_governance_xml(generated_file):
        # validates valid XML
        ElementTree.parse(generated_file)

    def check_ca_key_pem(generated_file):
        lines = generated_file.readlines()
        assert lines[0] == '-----BEGIN PRIVATE KEY-----\n'
        assert lines[-1] == '-----END PRIVATE KEY-----\n'

    with tempfile.TemporaryDirectory() as keystore_dir:
        assert cli.main(argv=['security', 'create_keystore', keystore_dir]) == 0
        expected_files = (
            ('governance.p7s', check_governance_p7s),
            ('index.txt', check_index_txt),
            ('ca.cert.pem', check_ca_cert_pem),
            ('ca_conf.cnf', check_ca_conf),
            ('ecdsaparam', check_ecdsaparam),
            ('governance.xml', check_governance_xml),
            ('ca.key.pem', check_ca_key_pem),
            ('serial', None),
        )

        for expected_file, file_validator in expected_files:
            path = os.path.join(keystore_dir, expected_file)
            assert os.path.isfile(path), 'Expected output file %s was not found.' % expected_file
            if file_validator:
                with open(path, 'r') as generated_file:
                    file_validator(generated_file)
