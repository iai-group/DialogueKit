# How to publish DialogueKit to PyPI

As of know we do not have a real integration test before publishing *DialogueKit*. Our current guidelines are as follows.

* Build

    ```shell
    python -m build
    ```

    This will create a *wheel* and a *tar* for publishing under dist/*

* Test publishing

    ```shell
    python -m twine upload --repository testpypi dist/*
    ```

    Publishes to test-pypi.

* Create a testing conda environment

    ```shell
    conda create --name dk_test python=3.7.12
    conda activate dk_test
    ```

    ```shell
    pip install rasa==3.0.8
    pip install pytest
    pip install -i https://test.pypi.org/simple/ dialoguekit
    ```

    This will install dialoguekit from test-pypi.
    Using this environment run the tests in the main repository.

* Publish to PyPI

    ```shell
    python -m twine upload --repository pypi dist/*
    ```

    This will publish the new build to PyPI.
