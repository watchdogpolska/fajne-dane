from django.contrib.auth.models import User


def user1() -> User:
    user, _ = User.objects.get_or_create(
        username="test_user",
        email="test_user@test.com",
        password="password"
    )
    return user
