import os
import subprocess
import sys
from setuptools import setup
from setuptools.command.install import install as _install

class PostInstallCommand(_install):
    """Post-installation for installation mode."""
    def run(self):
        _install.run(self)
        # Run your post-install script
        print("Running post-install script...")
        try:
            # The script is in the 'scripts' directory relative to setup.py
            script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'post_install.py')
            
            # Use sys.executable to ensure the script runs with the same Python interpreter
            # as the installation.
            subprocess.check_call([sys.executable, script_path])
        except subprocess.CalledProcessError as e:
            print(f"Post-install script failed with error: {e}", file=sys.stderr)
            # Exit with a non-zero code to indicate failure to the installer
            sys.exit(1)

setup(
    cmdclass={
        'install': PostInstallCommand,
    }
)
