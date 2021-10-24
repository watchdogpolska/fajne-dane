from users.models.user import User


def user1(is_active=False) -> User:
    user, _ = User.objects.get_or_create(
        username="test_user",
        email="test_user@test.com",
        password="password"
    )
    if is_active:
        user.is_active = True
        user.save()
    return user
