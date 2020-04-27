import subprocess

from django.template.loader import get_template

from ._base import BaseGenerateCommand


class Command(BaseGenerateCommand):
    help = "Generate scaffolding to compile javascript."

    def handle(self, *args, **options):
        build = 'add-project-script -n "build" -v "webpack --mode production"'
        watch = 'add-project-script -n "watch" -v "webpack --watch --info-verbosity verbose"'
        args = 'npm install -g add-project-script'.split(' ')
        subprocess.check_call(args, shell=False)
        subprocess.check_call(build.split(' '), shell=True)
        subprocess.check_call(watch.split(' '), shell=True)
        subprocess.check_call('npm uninstall -g add-project-script'.split(' '))

        npm_pkg = 'npm install -save-dev glob sockpuppet-js stimulus_reflex webpack webpack-cli'
        subprocess.check_call(npm_pkg.split(' '))

        template = get_template('sockpuppet/scaffolds/webpack.html')
        rendered = template.render({})
        self.create_file('', 'webpack.config.js', rendered)

        self.call_stdout('Scaffolding generated!', _type='SUCCESS')
