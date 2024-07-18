import setuptools

setuptools.setup(
    name="pyAp",
    version="v0.2",
    author="Weiran Li & Yishen Zhang",
    author_email="wl413@cam.ac.uk & yishen.zhang@rice.edu",
    packages= setuptools.find_packages(
        exclude= ['example', 'contrib', 'input', 'tutorial']
        ),


    install_requires= [
    'pandas',
    'matplotlib',
    'numpy',
    'scipy',
    'seaborn',
    'periodictable'
    ]
)
