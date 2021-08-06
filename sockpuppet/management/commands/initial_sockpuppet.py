import json
import subprocess

from django.template.loader import get_template
from subprocess import CalledProcessError

from ._base import BaseGenerateCommand


class Command(BaseGenerateCommand):
    help = "Generate scaffolding to compile javascript."

    def add_project_script(
        self, name: str, value: str, path: str = "", force: bool = False
    ):
        with open("package.json", "rw") as f:
            jsn = json.load(f)

            if not jsn.get("scripts"):
                jsn["scripts"] = {}
            else:
                if not force and jsn["scripts"].get("name"):
                    self.call_stdout("Skipping existing script '{}'" % name)

            jsn["scripts"]["name"] = value
            json.dump(jsn, f, indent=2)

    def handle(self, *args, **options):
        init = "npm init -y"
        subprocess.check_call(init, shell=True)
        try:
            self.add_project_script("build", "webpack --mode production")
            self.add_project_script("watch", "webpack --watch")
        except CalledProcessError:
            msg = "Build and watch already in package.json, so skipping these"
            self.call_stdout(msg)

        npm_pkg = "npm install -save-dev glob sockpuppet-js stimulus stimulus_reflex webpack webpack-cli"
        subprocess.check_call(npm_pkg.split(" "), shell=True)

        template = get_template("sockpuppet/scaffolds/webpack.html")
        rendered = template.render({})
        self.create_file("", "webpack.config.js", rendered)
        self.call_stdout("Scaffolding generated!", _type="SUCCESS")
