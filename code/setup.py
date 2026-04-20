from setuptools import setup, find_packages

def read_requirements(path="requirements.txt"):
    with open(path) as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="linear_and_nonlinear_kf",
    version="0.1.0",
    description="Linear and Nonlinear Kalman Filter implementation",
    author="Marco Todescato",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=read_requirements()
)