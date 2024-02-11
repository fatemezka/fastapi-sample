# Goodlawyer FastAPI Project

This project is like a law social media platform and it will be used by 2 types of people lawyers and clients. Lawyers who represent themselfs in this website and see the list of legal requests from clients and they can offer their price. On the other hand we have clients (normal user) who can ask their legal questions or ask their request from specific lawyer, so lawyers will answer them.

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

To run this project first make a file *.env* in the root of your project's directory and put *.env.template* keys in there and gave them proper values. as you know *.env.template* is just a template file to guide you what stuff should you have in your .env file and gave them some values.
And then:

```python
  uvicorn app.main:app --reload
```

then you project will run on port 8000 on localhost, so you can see the APIs documentation which is prepared by fastapi in these 2 urls:

1. http://localhost:8000/docs
2. http://localhost:8000/redoc

You can see error logs in *errors.log* file, which will create as you face an error.


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

## Some Details

In this project I used FastAPI python framework and SqlAlchemy as ORM to mysql database.
