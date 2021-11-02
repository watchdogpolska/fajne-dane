from users.models.user import User


def user1(is_active=False) -> User:
    user = User.objects.filter(email="test_user@test.com").first()
    if not user:
        user = User.objects.create_user(
            email="test_user@test.com",
            password="password",
            first_name="Test",
            last_name="User"
        )
    if is_active:
        user.is_active = True
        user.save()
    return user
