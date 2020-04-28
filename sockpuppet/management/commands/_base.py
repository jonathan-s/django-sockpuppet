from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class BaseGenerateCommand(BaseCommand):

    def lookup_app_path(self, app_name):
        try:
            config = apps.get_app_config(app_name)
        except LookupError as e:
            raise CommandError(str(e))

        module_path = config.module.__path__[0]
        return module_path

    def call_stdout(self, msg, _type='WARNING'):
        style = getattr(self.style, _type)
        self.stdout.write(style(msg))

    def create_file(self, folder, filename, contents):
        if folder == '':
            base_path = Path.cwd()
        else:
            base_path = self.module_path

        filepath = base_path / folder / filename
        if filepath.exists():
            partial_path = '/'.join(filepath.parts[-4:])
            self.call_stdout('{} already exists, so it will be skipped'.format(partial_path))
            return

        try:
            filepath.parent.mkdir(parents=True)
        except FileExistsError:
            pass

        with filepath.open(mode='w') as f:
            f.write(contents)
