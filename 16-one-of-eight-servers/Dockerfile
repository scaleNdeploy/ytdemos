FROM python:3.11-slim
WORKDIR /app
COPY server.py orders_v1.py ./
RUN mv orders_v1.py orders.py
CMD ["python", "server.py"]
