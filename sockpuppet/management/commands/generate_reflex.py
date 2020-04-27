from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template

from ._base import BaseGenerateCommand


TEMPLATES = {
    '_reflex.py': 'sockpuppet/scaffolds/reflex.py',
    '_controller.js': 'sockpuppet/scaffolds/controller.js',
    '.js': 'sockpuppet/scaffolds/application.js',
    '.py': 'sockpuppet/scaffolds/view.py',
    '.html': 'sockpuppet/scaffolds/template.html'
}


class Command(BaseGenerateCommand):
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

    def handle(self, *args, **options):
        app_name = options['app_name'][0]
        reflex_name = options['reflex_name']

        module_path = self.lookup_app_path(app_name)
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
        if (self.module_path / 'views.py').exists():
            msg = 'We created a views directory which means that you need to move your initial views there'
            self.call_stdout('')
            self.call_stdout(msg, _type='WARNING')

        self.call_stdout("Last step is to add the view to urls.py", _type='SUCCESS')
