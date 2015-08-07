from setuptools import setup

setup(
    name="doc2pdf-test",
    version="0.0.1",
    url="https://github.com/andiwand/doc2pdf-test",
    license="GNU Lesser General Public License",
    author="Andreas Stefl",
    install_requires=["doc2pdf"],
    author_email="stefl.andreas@gmail.com",
    description="doc2pdf test script with nagios conventions",
    long_description="",
    package_dir={"": "src"},
    packages=["doc2pdf.test"],
    platforms="windows",
    entry_points={
        "console_scripts": ["doc2pdf-test = doc2pdf.test.cli:main"]
    },
)
