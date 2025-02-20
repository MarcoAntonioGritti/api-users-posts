from datetime import datetime
from http import HTTPStatus

from sqlalchemy import func, inspect

from apirestfull_curso.src.models import Post, User, db
from apirestfull_curso.src.views.post import PostSchema


def test_get_post_success_admin(client, create_post_test, access_token_admin):
    post = create_post_test

    response = client.get(
        f"/posts/get/{post.id}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    post_schema = PostSchema()

    assert response.status_code == HTTPStatus.OK
    assert response.json == post_schema.dump(post)


def test_get_post_not_found(client, access_token_admin):
    invalid_post = -1

    response = client.get(
        f"/users/get/{invalid_post}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_list_posts_success_access_admin(client, create_post_test, access_token_admin):
    post = create_post_test

    response = client.get(
        "/posts/list", headers={"Authorization": f"Bearer {access_token_admin}"}
    )

    posts = db.session.execute(db.select(Post)).scalars()

    post_schema = PostSchema(many=True)

    assert response.status_code == HTTPStatus.OK
    assert response.json == post_schema.dump(posts)


def test_create_post(client, access_token_admin):
    data = {
        "title": "titulo teste",
        "body": "livro muito bom",
        "created": "2025-01-17T12:00:00",
        "author_id": 1,
    }

    response = client.post(
        "/posts/create",
        json=data,
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "Post created!"}
    assert db.session.execute(db.select(func.count(Post.id))).scalar() == 1


def test_update_post_success(client, create_post_test, access_token_admin):
    post_create = create_post_test
    post = db.session.execute(db.select(Post).where(Post.id == 1)).scalar()

    new_data = {
        "title": "titulo teste",
        "body": "livro muito bom",
        "author_id": 1,
    }

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in new_data:
            setattr(post, column.key, new_data[column.key])

    db.session.commit()

    response = client.patch(
        f"/posts/update/{post.id}",
        json=new_data,
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "author_id": post.author_id,
    }


def test_update_post_forbidden(client, create_post_test, access_token_normal):
    post_create = create_post_test
    post = db.session.execute(db.select(Post).where(Post.id == 1)).scalar()

    new_data = {
        "title": "titulo teste",
        "body": "livro muito bom",
        "author_id": 1,
    }

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in new_data:
            setattr(post, column.key, new_data[column.key])

    db.session.commit()

    response = client.patch(
        f"/posts/update/{post.id}",
        json=new_data,
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {"message": "User dont have access."}


def test_update_post_success(client, access_token_admin):
    invalid_post = -1

    new_data = {
        "title": "titulo teste",
        "body": "livro muito bom",
        "author_id": 1,
    }

    response = client.patch(
        f"/posts/update/{invalid_post}",
        json=new_data,
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_post_success(client, create_post_test, access_token_admin):
    post = create_post_test
    response = client.delete(
        f"/posts/delete/{post.id}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.json == None
    assert post.id is not Post


def test_delete_post_forbidden(client, create_post_test, access_token_normal):
    post = create_post_test

    response = client.delete(
        f"/posts/delete/{post.id}",
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {"message": "User dont have access."}


def test_delete_post_not_found(client, access_token_admin):

    invalid_post = -1

    response = client.delete(
        f"/posts/delete/{invalid_post}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
