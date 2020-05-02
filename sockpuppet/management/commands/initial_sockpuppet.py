import subprocess

from django.template.loader import get_template
from subprocess import CalledProcessError

from ._base import BaseGenerateCommand


class Command(BaseGenerateCommand):
    help = "Generate scaffolding to compile javascript."

    def handle(self, *args, **options):
        install = 'npm install -g add-project-script'
        subprocess.check_call(install, shell=True)
        try:
            build = 'add-project-script -n "build" -v "webpack --mode production"'
            watch = 'add-project-script -n "watch" -v "webpack --watch --info-verbosity verbose"'
            subprocess.check_call(build, shell=True)
            subprocess.check_call(watch, shell=True)
        except CalledProcessError:
            msg = 'Build and watch already in package.json, so skipping these'
            self.call_stdout(msg)

        subprocess.check_call('npm uninstall -g add-project-script', shell=True)

        npm_pkg = 'npm install -save-dev glob sockpuppet-js stimulus_reflex webpack webpack-cli'
        subprocess.check_call(npm_pkg.split(' '))

        template = get_template('sockpuppet/scaffolds/webpack.html')
        rendered = template.render({})
        self.create_file('', 'webpack.config.js', rendered)
        self.call_stdout('Scaffolding generated!', _type='SUCCESS')
