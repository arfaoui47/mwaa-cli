# Pull base image
FROM python:3.8
# Set environment varibles
WORKDIR /code/

# Install dependencies
COPY app/requirements.txt /code/
RUN pip install -r requirements.txt
COPY app/ /code/
EXPOSE 8000
CMD ["python", "app/main.py"]