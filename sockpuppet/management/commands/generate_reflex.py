from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template


TEMPLATES = {
    '_reflex.py': 'sockpuppet/scaffolds/reflex.py',
    '_controller.js': 'sockpuppet/scaffolds/controller.js',
    '.js': 'sockpuppet/scaffolds/application.js',
    '.py': 'sockpuppet/scaffolds/view.py',
    '.html': 'sockpuppet/scaffolds/template.html'
}


class Command(BaseCommand):
    help = "Scaffold for reflex. Includes javascript and python."

    def add_arguments(self, parser):
        parser.add_argument(
            'app_name', nargs=1, type=str,
            help='The app where the generated files should be placed'
        )
        parser.add_argument(
            'reflex_name', nargs='?', type=str,
            help='The name of the reflex and javascript controller',
            default='example'
        )

    def call_stdout(self, msg, _type='WARNING'):
        style = getattr(self.style, _type)
        self.stdout.write(style(msg))

    def create_file(self, folder, filename, contents):
        filepath = self.module_path / folder / filename
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

    def handle(self, *args, **options):
        app_name = options['app_name'][0]
        reflex_name = options['reflex_name']
        try:
            config = apps.get_app_config(app_name)
        except LookupError as e:
            raise CommandError(str(e))

        module_path = config.module.__path__[0]
        self.module_path = Path(module_path)

        paths = [
            ('reflexes', '_reflex.py'),
            ('javascript', '.js'),
            ('javascript/controllers', '_controller.js'),
            ('views', '.py'),
            ('templates', '.html')
        ]

        for path, suffix in paths:
            template_name = TEMPLATES[suffix]
            template = get_template(template_name)
            rendered = template.render({'reflex_name': reflex_name})
            self.create_file(path, '{}{}'.format(reflex_name, suffix), rendered)

        self.create_file('views', '__init__.py', '')
        self.create_file('reflexes', '__init__.py', '')
        self.call_stdout('Scaffolding generated!', _type='SUCCESS')
