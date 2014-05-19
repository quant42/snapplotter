from distutils.core import setup

setup(
    name="snapplotter",
    version="1.0.0",
    description="Visualization of snap output files.",
    author="Yann Spoeri",
    author_email="yann_spoeri@web.de",
    py_modules=["msaXReader", "snap2XReader"],
    scripts=["snapplotter"],
    data_files=[ ("share/man/man1", ["snapplotter.1"]) ]
)
