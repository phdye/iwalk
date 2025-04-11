from setuptools import setup, find_packages

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class BDistWheelCommand(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False  # adjust if needed

    cmdclass = {'bdist_wheel': BDistWheelCommand}
except ImportError:
    cmdclass = {}

setup(
    name="iwalk",
    version="0.1",
    packages=find_packages("src", include=["iwalk", "iwalk.*"]),
    package_dir={"": "src"},
    cmdclass=cmdclass,
)
