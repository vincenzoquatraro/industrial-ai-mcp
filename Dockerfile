FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --trusted-host pypi.python.org \
    --trusted-host download.pytorch.org \
    --trusted-host download-r2.pytorch.org \
    --timeout 120 \
    torch==2.13.0 --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --trusted-host pypi.python.org \
    --timeout 120 \
    -r requirements.txt

COPY . .

CMD ["python", "-m", "app.main"]