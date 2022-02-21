import setuptools

setuptools.setup(
    name="pyAp",
    version="0.1",
    author="Weiran Li & Yishen Zhang",
    author_email="wl413@cam.ac.uk & yishen.zhang@kuleuven.be",
    packages= setuptools.find_packages(
        exclude= ['example', 'contrib', 'input', 'tutorial']
        ),

    # package_dir= {'' : 'AlOlivThermo'},
    install_requires= [
    'pandas',
    'matplotlib',
    'numpy',
    'scipy'
    ]
)
