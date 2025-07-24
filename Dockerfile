# Stage 1: Backend (FastAPI)
FROM python:3.10-slim AS backend
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Stage 2: Frontend (Streamlit)
FROM python:3.10-slim AS frontend
WORKDIR /frontend
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY frontend ./frontend

# Final Stage: Combined
FROM python:3.10-slim
WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend /frontend /frontend
EXPOSE 8000 8501
CMD ["/bin/bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"] 