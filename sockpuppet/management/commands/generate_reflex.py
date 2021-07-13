import keyword
from pathlib import Path

from django.core.management import CommandError
from django.template.loader import get_template

from ._base import BaseGenerateCommand
from ...utils import pascalcase

TEMPLATES = {
    "_reflex.py": "sockpuppet/scaffolds/reflex.py",
    "_controller.js": "sockpuppet/scaffolds/controller.js",
    ".js": "sockpuppet/scaffolds/application.js",
    ".py": "sockpuppet/scaffolds/view.py",
    ".html": "sockpuppet/scaffolds/template.html",
}


class Command(BaseGenerateCommand):
    help = "Scaffold for reflex. Includes javascript and python."

    def add_arguments(self, parser):
        parser.add_argument(
            "app_name",
            nargs=1,
            type=str,
            help="The app where the generated files should be placed",
        )
        parser.add_argument(
            "reflex_name",
            nargs="?",
            type=str,
            help="The name of the reflex and javascript controller",
            default="example",
        )

        parser.add_argument(
            "--javascript",
            dest="javascript",
            action="store_true",
            help="Include this to generate a setup than includes javascript with controllers",
        )
        parser.set_defaults(javascript=False)

    def handle(self, *args, **options):
        app_name = options["app_name"][0]
        reflex_name = options["reflex_name"].lower()
        using_javascript = options["javascript"]

        if not reflex_name.isidentifier():
            raise CommandError(
                f"The reflex name ({reflex_name}) must be a valid Python identifier."
            )

        if reflex_name == "_":
            raise CommandError("The reflex name must not be a single underscore.")

        if reflex_name in keyword.kwlist:
            raise CommandError(
                f"The reflex name ({reflex_name}) can't be a Python keyword."
            )
        module_path = self.lookup_app_path(app_name)
        self.module_path = Path(module_path)

        paths = [
            (False, "reflexes", "_reflex.py"),
            (True, "javascript", ".js"),
            (True, "javascript/controllers", "_controller.js"),
            (False, "views", ".py"),
            (False, "templates", ".html"),
        ]

        for without_js, path, suffix in paths:
            template_name = TEMPLATES[suffix]
            template = get_template(template_name)
            rendered = template.render(
                {
                    "class_name": pascalcase(reflex_name),
                    "reflex_name": reflex_name,
                    "using_javascript": using_javascript,
                }
            )
            if without_js and not using_javascript:
                # skipping these templates
                continue
            self.create_file(path, "{}{}".format(reflex_name, suffix), rendered)

        self.create_file("views", "__init__.py", "")
        self.create_file("reflexes", "__init__.py", "")
        self.call_stdout("Scaffolding generated!", _type="SUCCESS")
        if (self.module_path / "views.py").exists():
            msg = "We created a views directory which means that you need to move your initial views there"
            self.call_stdout("")
            self.call_stdout(msg, _type="WARNING")

        self.call_stdout("Last step is to add the view to urls.py", _type="SUCCESS")
