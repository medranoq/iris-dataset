FROM python:3.12-slim-bullseye AS base
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev\
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN mkdir /back-end
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install "uvicorn[standard]" gunicorn

#FROM base AS production
#COPY . /back-end
#RUN mkdir -p /back-end/static
#EXPOSE 80
#CMD ["uvicorn", "main:back-end", "--host", "0.0.0.0", "--port", "80"]