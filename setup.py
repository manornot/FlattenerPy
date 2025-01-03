from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name='FlattenerPy',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here if needed
    ],
    entry_points={
        "console_scripts": [
            "flatten = FlattenerPy.flattener:flatten_entry",
            "inflate = FlattenerPy.flattener:inflate_entry"
        ]
    },
    long_description="Flatten and inflate file structures",
    long_description_content_type="text/markdown",
)
