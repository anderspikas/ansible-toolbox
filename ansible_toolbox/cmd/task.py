from __future__ import absolute_import

import logging
import tempfile
import subprocess

from ansible_toolbox.base import BaseApp

LOG = logging.getLogger(__name__)


class App (BaseApp):
    def build_argument_parser(self):
        p = super(App, self).build_argument_parser()
        p.add_argument('tasklist')
        return p

    def main(self):
        args = self.parse_args()
        template = self.get_template('tasklist.yml')

        with tempfile.NamedTemporaryFile(dir='.') as fd:
            fd.write(template.render(
                tasklist=args.tasklist,
                hosts=args.hosts,
                gather=args.gather,
            ))

            fd.flush()

            cmd = ['ansible-playbook', fd.name]
            cmd.extend(self.build_command_line(args))
            subprocess.call(cmd)


def main():
    App().main()
