# coding: utf-8
import setuptools

setuptools.setup(
    name='DeWorld',
    version='0.2.0',
    description='DEveloping WORLD - python world generator',
    long_description = open('README.rst').read(),
    url='https://github.com/Tiendil/deworld',
    author='Aleksey Yeletsky <Tiendil>',
    author_email='a.eletsky@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',

        'Natural Language :: English'],
    keywords=['gamedev', 'procedural content generation', 'game development', 'map', 'map generation', 'terrain', 'terrain generation'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    test_suite = 'tests',
    )
