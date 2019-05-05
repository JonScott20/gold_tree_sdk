from distutils.core import setup

setup(
    name='gold_tree_sdk',  # How you named your package folder (MyLib)
    packages=['gold_tree_sdk'],  # Chose the same as "name"
    version='0.1',
    # Start with a small number and increase it with every change you make
    license='MIT',
    # Chose a license from here:
    # https://help.github.com/articles/licensing-a-repository
    description='SDK to interact with the Gold Tree Solar Farm API.',
    # Give a short description about your library
    author='Jonathon Scott',  # Type in your name
    author_email='jonscott20@gmail.com',  # Type in your E-Mail
    url='https://github.com/JonScott20/gold_tree_sdk',
    # Provide either the link to your github or to your website
    download_url=(
        'https://github.com/JonScott20/' +
        'gold_tree_sdk/archive/v_01.tar.gz'
    ),  # I explain this later on
    keywords=[
        'Data',
        'SDK',
        'Solar',
        'API',
        'Cal Poly'
    ],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'pandas',
        'urllib',
        'datetime',
        'time',
        'json'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha",
        # "4 - Beta"
        # or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.6',
    ],
)
