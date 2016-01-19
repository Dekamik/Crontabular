from setuptools import setup

setup(
    name="Crontabular",
    description="A small program for easily creating cronjobs",
    version="0.1.1",
    license="MIT",
    platforms="Unix",
    requires=[
        "python-crontab"
    ]
)