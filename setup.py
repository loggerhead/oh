from setuptools import setup

setup(
    name='oh',
    version='0.1.0',
    description='A simple TCP/UDP echo server',
    author='loggerhead',
    author_email='lloggerhead@gmail.com',
    url='https://github.com/loggerhead/oh',
    keywords=('debug', 'echo', 'TCP', 'UDP'),
    entry_points='''
        [console_scripts]
        oh=serve:main
    ''',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ]
)
