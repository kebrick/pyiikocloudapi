from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
VERSION = '0.0.25'
setup(
    name='pyiikocloudapi',
    version=VERSION,
    description='Python services for convenient work with iiko Transport / iiko cloud api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['pyiikocloudapi'],
    # packages=find_packages(where="src"),
    # package_dir={"": "src"},
    author='kebrick',
    author_email='ruban.kebr@gmail.com',
    license='MIT',
    project_urls={
        'Source': 'https://github.com/kebrick/pyiikocloupapi',
        'Tracker': 'https://github.com/kebrick/pyiikocloupapi/issues',
    },
    install_requires=['requests', 'pydantic'],

    python_requires='>=3.7',
    zip_safe=False
)
