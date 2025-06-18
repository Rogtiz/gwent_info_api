FROM python:3.9

WORKDIR /gwent_info_api

COPY ./requirements.txt /gwent_info_api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /gwent_info_api/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]