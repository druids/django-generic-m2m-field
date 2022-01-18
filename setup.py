from setuptools import setup, find_packages


setup(
    name='django-generic-m2m-field',
    version='0.0.7',
    description="Django generic many to many field library.",
    keywords='django, fields, generic',
    author='Lubos Matl',
    author_email='matllubos@gmail.com',
    url='https://github.com/druids/django-generic-m2m-field',
    license='MIT',
    package_dir={'generic_m2m_field': 'generic_m2m_field'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Czech',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    install_requires=[
        'django>=2.2.9,<3.2',
        'django-chamber>=0.5.3',
        'attrdict==2.0.1'
    ],
    zip_safe=False
)
