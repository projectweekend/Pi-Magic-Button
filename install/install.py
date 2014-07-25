#!/usr/bin/env python

import subprocess


def main():
    # Install system dependencies
    subprocess.call(["apt-get", "update"])
    subprocess.call(["apt-get", "-y", "upgrade"])
    subprocess.call(["apt-get", "-y", "--force-yes", "install", "upstart"])
    subprocess.call(["apt-get", "-y", "install", "python-dev"])
    subprocess.call(["apt-get", "-y", "install", "python-pip"])
    subprocess.call(["pip", "install", "-r", "requirements.txt"])

    # Copy Upstart script
    subprocess.call(["cp", "./install/magic-button.conf", "/etc/init"])

    # Add empty config.yml
    open('config.yml', 'w+')


if __name__ == '__main__':
    main()
