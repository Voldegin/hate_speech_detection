from setuptools import setup
from sys import platform

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

if platform == "darwin":
    platform_requires = ["tensorflow-macos==2.9.2"]
else:
    platform_requires = ["tensorflow==2.8.2"]

entry_points = {
    'console_scripts': [
        'detect-hate-speech=main:main'
    ]
}

if __name__ == '__main__':
    setup(
        name='hate_speech_app',
        install_requires=install_requires + platform_requires,
        entry_points=entry_points
    )
