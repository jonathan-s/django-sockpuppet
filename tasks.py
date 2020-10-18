"""
TODO convert this into a task.

coverage: ## check code coverage quickly with the default Python
    coverage run --source sockpuppet runtests.py tests
    coverage report -m
    coverage html
    open htmlcov/index.html

"""
from invoke import task
from pathlib import Path
import json


@task
def clean_build(c):
    """
    Remove build artifacts
    """
    c.run("rm -fr build/")
    c.run("rm -fr dist/")
    c.run("rm -fr *.egg-info")


@task
def clean_pyc(c):
    """
    Remove python file artifacts
    """
    c.run("find . -name '*.pyc' -exec rm -f {} +")
    c.run("find . -name '*.pyo' -exec rm -f {} +")
    c.run("find . -name '*~' -exec rm -f {} +")


@task
def clean(c):
    """
    Remove python file and build artifacts
    """
    clean_build(c)
    clean_pyc(c)


@task
def integration(c):
    """
    Run integration tests
    """
    c.run("npm install")
    c.run("npm run build_test")
    c.run("python manage.py migrate")
    c.run("python manage.py runserver 2>&1 > /dev/null &")
    c.run("npm run cypress:run")


@task
def unittest(c):
    """
    Run unittests
    """
    c.run("python manage.py test")


@task
def lint(c):
    """
    Check style with flake8
    """
    c.run("flake8 sockpuppet tests")


@task(help={'bumpsize': 'Bump either for a "feature" or "breaking" change'})
def release(c, bumpsize=''):
    """
    Package and upload a release
    """
    path = Path.cwd()
    package_json = path / 'package.json'
    with package_json.open() as f:
        contents = json.loads(f.read())

    clean(c)
    if bumpsize:
        bumpsize = '--' + bumpsize

    c.run("bumpversion {bump} --no-input".format(bump=bumpsize))
    import sockpuppet
    version = sockpuppet.__version__

    contents['version'] = version
    with package_json.open(mode='w+') as f:
        f.write(json.dumps(contents, indent=4))

    c.run("git add package.json")
    c.run("git commit --amend --no-edit")

    c.run("npm publish")
    c.run("python setup.py sdist bdist_wheel")
    c.run("twine upload dist/*")

    c.run('git tag -a {version} -m "New version: {version}"'.format(version=version))
    c.run("git push --tags")
    c.run("git push origin master")
