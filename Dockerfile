FROM python:3.12-slim
WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml .
COPY uvlock .

RUN uv sync --frozen

# COPY main.py test_main.py pytest.ini ./
# The upper line is commented because the shortest code is to copy all files using . .
COPY . .

EXPOSE 8000
LABEL NAME = "My FastAPI App"\
      VERSION = "1.0.0"\
      DESCRIPTION = "A simple FastAPI application"\
      AUTHOR = "Abdul Qadeer Khan"\
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]