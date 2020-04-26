import subprocess

from django.test import TestCase
from django.conf import settings
from git import Repo


class JavascriptCommittedTest(TestCase):

    def test_all_javascript_is_committed_to_source_code(self):
        subprocess.call('npm run-script build'.split(' '))
        repo = Repo(settings.BASE_DIR)
        diff_result = repo.git.diff('sockpuppet/static/js/reflex-websocket.js')

        self.assertEqual(diff_result, '', 'Not all changes have been committed')

