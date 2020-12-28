from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class ManagementCommandTests(TestCase):
    def call_command(self, command, *args, **kwargs):
        out = StringIO()
        call_command(
            command,
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def test_generate_reflex_command(self):
        result = self.call_command('generate_reflex', 'example', 'test_reflex')
        # TODO assert that files were created successfully
        self.assertIn('Last step is to add the view to urls.py', result)

    def test_generate_reflex_javascript(self):
        result = self.call_command('generate_reflex', 'example', 'test_reflex', '--javascript')
        # TODO assert that files were created successfully
        self.assertIn('Last step is to add the view to urls.py', result)
