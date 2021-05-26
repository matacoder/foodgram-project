# Foodgram: recipes social network
<img src="https://raw.githubusercontent.com/matacoder/matacoder/main/foodgram.png">

[![FOODGRAM workflow](https://github.com/matacoder/foodgram-project/actions/workflows/foodgram_workflow.yaml/badge.svg)](https://github.com/matacoder/foodgram-project/actions/workflows/foodgram_workflow.yaml)

You can see project at [https://cafe.matakov.com](https://cafe.matakov.com)

# What is this?

This is my diploma project for Yandex.Prakticum online school of backend development.

# How to deploy?

This project can be deployed using `docker-compose`. All files would be mounted to containers, and you would be able to see changes on-the-fly.
Here you can also find production version of `docker-compose.yaml`

# Stack

- Django
- Postgres
- Nginx
- Caddy
- Gunicorn

# Features

- Add/edit recipe with ingredients (django in atomic transactions mode)
- Add to cart (database based and session based approaches for unregistered users)
- Add to favorites
- Follow author
- Pagination
- CSV export
- PDF export
- Tags via GET-params

# What is Caddy?

It is a convenient way to run your site on a server. Just install it and put in `Caddyfile`:

`example.com`

`reverse_proxy 127.0.0.1:1111`

and it issues ssl certificate and run your site fully automatically at `example.com` domain
