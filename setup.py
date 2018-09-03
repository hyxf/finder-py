from os.path import join, dirname

from setuptools import setup, find_packages

# version
with open(join(dirname(__file__), 'finder/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

# requires
with open(join(dirname(__file__), 'requirements.txt'), 'rb') as f:
    deps = [x.decode('ascii').strip() for x in f.readlines() if x.strip()]

setup(
    name='finder-py',
    version=version,
    url='https://github.com/hyxf/finder-py',
    description='LAN file sharing',
    long_description='LAN file sharing, make it easy',
    author='hyxf',
    author_email='1162584980@qq.com',
    license='Apache 2.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'finder = finder.cmdline:execute'
        ]
    },
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=2.7.*',
    install_requires=deps
)
