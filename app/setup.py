from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

entry_points = {
    'console_scripts': [
        'detect-hate-speech=main:main'
    ]
}

if __name__ == '__main__':
    setup(
        name='hate_speech_app',
        install_requires=install_requires,
        entry_points=entry_points
    )
