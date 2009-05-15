import os
 
from distutils.core import setup
 
def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == "":
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)
 
package_dir = "protected_files"
 
packages = []
for dirpath, dirnames, filenames in os.walk(package_dir):
    # ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith("."):
            del dirnames[i]
    if "__init__.py" in filenames:
        packages.append(".".join(fullsplit(dirpath)))
 
setup(name='django-protected-files',
    version='0.1',
    description='A Django application that lets you serve protected static files via your frontend server after authenticating against the Django user database.',
    author='Peter Baumgartner',
    author_email='pete@lincolnloop.com',
    url='http://github.com/lincolnloop/django-protected-files',
    packages=packages)