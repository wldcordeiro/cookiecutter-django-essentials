import os
import shutil
import unittest
from os.path import exists, dirname, join

import sh

from cookiecutter.main import cookiecutter


class DjangoCookieTestCase(unittest.TestCase):

    root_dir = dirname(dirname(__file__))
    ctx = {}
    destpath = None

    def generate_project(self, extra_context=None):
        ctx = {
            "project_name": "My Test Project",
            "repo_name": "my_test_project",
            "repo_url": "https://github.com/test/test",
            "author_name": "Test Author",
            "author_github_username": "@yourusername",
            "email": "test@example.com",
            "description": "A short description of the project.",
            "domain_name": "example.com",
            "version": "0.1.0",
            "timezone": "UTC",
            "now": "2015/01/13",
            "year": "2015",
            "port": "8080",
            "database_name": "database",
            "database_user": "dbuser",
            "database_password": "password",
            "use_whitenoise": "y"
        }
        if extra_context:
            assert isinstance(extra_context, dict)
            ctx.update(extra_context)

        self.ctx = ctx
        self.destpath = join(self.root_dir, self.ctx['repo_name'])

        cookiecutter(template='./', checkout=None, no_input=True, extra_context=ctx)

        # Build a list containing absolute paths to the generated files
        paths = [os.path.join(dirpath, file_path)
                 for dirpath, subdirs, files in os.walk(self.destpath)
                 for file_path in files]
        return paths

    def clean(self):
        if exists(self.destpath):
            shutil.rmtree(self.destpath)
        sh.cd(self.root_dir)

    def tearDown(self):
        self.clean()
