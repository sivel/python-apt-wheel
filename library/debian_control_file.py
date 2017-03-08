#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2017, Matt Martz <matt@sivel.net>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = """
---
module: debian_control_file
author: Matt Martz
version_added: "0.0"
short_description: Provides information from a debian packaging control file
requirements:
    - python >= 2.6
    - python-debian
    - deb_pkg_tools
description:
    - Parses a debian packaging control file and provides information from all
      paragraphs for all packages
options:
    path:
        required: true
        description:
            - Path to the debian control file, usually located at C(debian/control)
"""

EXAMPLES = """
- name: Parse debian control file
  debian_control_file:
    path: /home/ubuntu/python-apt/debian/control
  register: control
"""

RETURN = """# """

from ansible.module_utils.basic import AnsibleModule
try:
    from debian.deb822 import Deb822
    from deb_pkg_tools import control
    HAS_DEB_PKG_TOOLS = True
except ImportError:
    HAS_DEB_PKG_TOOLS = False


def main():
    module = AnsibleModule(
        argument_spec={
            'path': {'type': 'path', 'required': True}
        }
    )

    if not HAS_DEB_PKG_TOOLS:
        module.fail_json(msg='The deb_pkg_tools is required for this module')

    with open(module.params['path']) as f:
        paragraphs = list(Deb822.iter_paragraphs(f))

    return_data = {
        'sources': {},
        'packages': {}
    }

    for paragraph in paragraphs:
        data = control.parse_control_fields(paragraph)
        package = data.get('Package')
        source = data.get('Source')
        key = 'packages' if package else 'sources'

        return_data[key][package or source] = item = {}

        for field in control.DEPENDS_LIKE_FIELDS:
            item[field] = list(getattr(data.get(field), 'names', []))

        for field in data:
            if field in control.DEPENDS_LIKE_FIELDS:
                continue
            item[field] = data.get(field)

    module.exit_json(**return_data)


if __name__ == '__main__':
    main()
