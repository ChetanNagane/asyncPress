FROM nginx:bookworm

RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 8000

COPY ./config/nginx/nginx.conf /etc/nginx/conf.d

COPY . /app/