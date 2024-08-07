"""Packaging of DialogueKit."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


packages = setuptools.find_packages(where="dialoguekit")

setuptools.setup(
    name="dialoguekit",
    version="0.0.9.dev2",
    author="Nolwenn Bernard, Krisztian Balog, Jafar Afzali, \
        Aleksander Drzewiecki and Shuo Zhang",
    author_email="author@example.com",
    description=(
        "Toolkit for building conversational information access systems."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iai-group/dialoguekit",
    project_urls={
        "Bug Tracker": "https://github.com/iai-group/dialoguekit/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(),
    package_data={
        "": [
            "*.joblib",
            "dialoguekit/nlu/models/satisfaction/*.joblib",
        ]
    },
    include_package_data=True,
    python_requires=">=3.9",
    zip_safe=False,
    install_requires=[
        "rasa>=3.0",
        "Flask>=2.3.2",
        "flask-socketio>=5.3.3",
        "Werkzeug>=2.3.3",
        "websockets<11.0",
    ],
)
