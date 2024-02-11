# Goodlawyer FastAPI Project

This project is like a law social media platform and it will be used by 2 types of people, lawyers who represent themselfs in this website and see the list of raw legal requests from clients and they can offer their price. on the other hands we have clients (normal people) who can ask their legal questions or ask their request from specific lawyer, so lawyer answer them.

## Install Package Dependencies:

 ```python
  pip3 install virtualenv

  virtualenv venv

  windows:
  venv\Scripts\activate

  linux:
  source venv/bin/activate

  pip3 install -r requirements.txt
```

## Deployment

To run this project first go to project directory and then:

```python
  uvicorn app.main:app --reload
```

then you project will run on port 8000 on localhost, so you can see the APIs documentation which is prepared by fastapi in these 2 urls:

1. http://localhost:8000/docs
2. http://localhost:8000/redoc


## Endpoints

#### User API

```http
  POST /user/login
  POST /user/register
  GET /user/all
  GET /user/{id}
```

#### Lawer API

```http
  POST /lawyer/register
  GET /lawyer/all
  GET /lawyer/{id}
```

#### Question API

```http
  GET /question/all
  GET /question/category/all
  GET /question/{id}/answer/all
  GET /question/{id}
  POST /question
  POST /question/{id}/answer
  DELETE /question/{id}
```

#### Request API

```http
  GET /request/all
  GET /request/subject/all
  GET /request/{id}
  POST /request
  DELETE /request/{id}
```

