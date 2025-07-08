from setuptools import setup, find_packages

setup(
    name="hyprpython",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "hypr-pull-class = hyprpython.cli:pull_window_by_class",
            "hypr-focus-class = hyprpython.cli:focus_window_by_class",
        ]
    },
)
