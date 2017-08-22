from setuptools import setup


setup(
    name="gdeploy_config_generator",
    version="0.0.1",
    author="smit thakkar",
    author_email="smitthakkar96@gmail.com",
    description=("A small utility that would help you to generate gdeploy config files"),
    packages=[
                'gdeploy_config_generator'
            ],
    license="BSD",
    keywords="gdeploy, gdeploy config generator",
    url="https://github.com/smitthakkar96/gdeploy-config-generator",
    install_requires=['jinja2'],
    include_package_data=True,
    zip_safe=False,
    scripts=[
        'bin/gdeploy_config_generator'
    ]
)
