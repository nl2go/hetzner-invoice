FROM python:3.8-alpine3.10 as builder
RUN pip install --upgrade pip
RUN apk add --no-cache gfortran g++
RUN pip install poetry==0.12.*
COPY . /app
WORKDIR /app
RUN poetry install

FROM python:3.8-alpine3.10
COPY --from=builder /app /app
WORKDIR /app
CMD ["./invoice/etl.py"]
