FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# ✅ Expose port 8000 for Koyeb health check
EXPOSE 8000

# ✅ Run the app on port 8000
CMD ["python", "main.py"]