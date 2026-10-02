# Comprehensive Fixtures Library

A fixture is a function decorated with `@pytest.fixture` that runs before (and optionally after) each test. Use fixtures to manage state, test data, database transactions, mock clients, and external configurations.

## 1. Built-in Pytest Fixtures

Pytest includes several powerful built-in fixtures you can use:

- `tmp_path`: Provides a temporary directory unique to the test invocation.
- `capsys`: Captures writes to stdout and stderr.
- `monkeypatch`: Allows dynamic modification of classes, dictionaries, environment variables, etc.

```python
def test_file_write(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("content")
    assert p.read_text() == "content"
```

## 2. Advanced Fixture Sharing and Yielding

Using the `yield` statement allows you to separate the setup code from the teardown code:

```python
import pytest

@pytest.fixture
def resource_setup_teardown():
    # Setup: runs before test
    resource = setup_resource()
    yield resource
    # Teardown: runs after test finishes
    resource.cleanup()
```

## 3. Parametrizing Fixtures

You can run a test multiple times with different data inputs:

```python
import pytest

@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param

def test_square(number):
    assert number * number in [1, 4, 9]
```
