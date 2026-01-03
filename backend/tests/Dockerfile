FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY tests/requirements.txt ./test-requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r test-requirements.txt

COPY . .

CMD ["python", "-m", "pytest", "tests/", "-v"]