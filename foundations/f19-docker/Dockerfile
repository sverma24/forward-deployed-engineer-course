# F19: package the F2 weather API so it runs the same way on any machine.
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi==0.162.0 uvicorn==0.54.0
COPY status_api.py .
EXPOSE 8090
CMD ["uvicorn", "status_api:app", "--host", "0.0.0.0", "--port", "8090"]
