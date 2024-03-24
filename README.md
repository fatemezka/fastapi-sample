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

#### User APIs

```http
  POST /token
  POST /user/register
  PUT /user/{user_id}
  PUT /user/change_password/{user_id}
  DELETE /user/{user_id}
  GET /user/me
  POST /user/logout
```

#### Lawer APIs

```http
  POST /lawyer/register
  GET /lawyer/all
  GET /lawyer/{lawyer_id}
  GET /lawyer/specialty/all
```

#### Question APIs

```http
  GET /question/all
  GET /question/{question_id}
  POST /question
  DELETE /question/{question_id}
  GET /question/category/all
  GET /question/{question_id}/answer/all
  POST /question/{question_id}/answer
```

#### Province & City APIs

```http
  GET /province/all
  GET /city/all
  
```

## Some Details

In this project I used FastAPI python framework and SqlAlchemy as ORM to posgresql database.
And alembic as database migration.
