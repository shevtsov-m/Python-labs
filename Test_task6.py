import pytest

from Task6 import (
    hash_password,
    User,
    Administrator,
    RegularUser,
    GuestUser,
    AccessControl
)

def test_hash_password_same_input():
    password = "Password123"

    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 == hash2


def test_hash_password_different_input():
    hash1 = hash_password("Password123")
    hash2 = hash_password("Password456")

    assert hash1 != hash2


def test_user_initialization():
    user = User("Alex", "Password123")

    assert user.username == "Alex"
    assert user.is_active is True
    assert user.password_hash != "Password123"


def test_verify_password_correct():
    user = User("Alex", "Password123")

    assert user.verify_password("Password123") is True


def test_verify_password_incorrect():
    user = User("Alex", "Password123")

    assert user.verify_password("WrongPassword") is False

def test_ban_user_success():
    admin = Administrator("Admin", "Admin123", True, ["ban_users"])
    user = User("Alex", "Password123")

    result = admin.ban_user(user)

    assert result is True
    assert user.is_active is False


def test_ban_user_without_permission():
    admin = Administrator("Admin", "Admin123", True, ["manage_users"])
    user = User("Alex", "Password123")

    result = admin.ban_user(user)

    assert result is False
    assert user.is_active is True



def test_delete_user_success():
    admin = Administrator("Admin", "Admin123", True, ["delete_users"])
    access_control = AccessControl()
    user = User("Alex", "Password123")

    access_control.add_user(user)

    result = admin.delete_user(user, access_control)

    assert result is True
    assert "Alex" not in access_control.users


def test_delete_user_without_permission():
    admin = Administrator("Admin", "Admin123", True, ["ban_users"])
    access_control = AccessControl()
    user = User("Alex", "Password123")

    access_control.add_user(user)

    result = admin.delete_user(user, access_control)

    assert result is False
    assert "Alex" in access_control.users


def test_delete_user_not_found():
    admin = Administrator("Admin", "Admin123", True, ["delete_users"])
    access_control = AccessControl()
    user = User("Alex", "Password123")

    result = admin.delete_user(user, access_control)

    assert result is False


def test_regular_user_initialization():
    user = RegularUser(
        "Alex",
        "Password123",
        True,
        "2026-10-20",
        5,
        "alex@mail.com"
    )

    assert user.username == "Alex"
    assert user.last_login == "2026-10-20"
    assert user.login_count == 5
    assert user.email == "alex@mail.com"
    assert user.is_active is True


def test_update_profile_success():
    user = RegularUser(
        "Alex", "Password123", True,
        "2026-10-20", 5, "alex@mail.com"
    )

    result = user.update_profile("Alexander", "new@mail.com")

    assert result is True
    assert user.username == "Alexander"
    assert user.email == "new@mail.com"


def test_update_profile_inactive():
    user = RegularUser(
        "Alex", "Password123", False,
        "2026-10-20", 5, "alex@mail.com"
    )

    result = user.update_profile("Alexander", "new@mail.com")

    assert result is False
    assert user.username == "Alex"
    assert user.email == "alex@mail.com"


def test_update_profile_registered_user():
    user = RegularUser(
        "Alex", "Password123", True,
        "2026-10-20", 5, "alex@mail.com"
    )

    access_control = AccessControl()
    access_control.add_user(user)

    result = user.update_profile(
        "Alexander",
        "new@mail.com",
        access_control
    )

    assert result is True
    assert "Alex" not in access_control.users
    assert "Alexander" in access_control.users
    assert access_control.users["Alexander"] is user


def test_update_profile_existing_username():
    user1 = RegularUser(
        "Alex", "Password123", True,
        "2026-10-20", 5, "alex@mail.com"
    )

    user2 = RegularUser(
        "Peter", "Password456", True,
        "2026-10-20", 3, "peter@mail.com"
    )

    access_control = AccessControl()
    access_control.add_user(user1)
    access_control.add_user(user2)

    result = user1.update_profile(
        "Peter",
        "new@mail.com",
        access_control
    )

    assert result is False
    assert user1.username == "Alex"
    assert "Alex" in access_control.users
    assert "Peter" in access_control.users


def test_guest_user_initialization():
    guest = GuestUser(
        "Guest",
        "Guest123",
        True,
        ["settings", "user_management"]
    )

    assert guest.username == "Guest"
    assert guest.is_active is True
    assert guest.access_restrictions == ["settings", "user_management"]


def test_check_access_allowed():
    guest = GuestUser("Guest", "Guest123", True, ["settings"])

    result = guest.check_access("main_page")

    assert result is True


def test_check_access_denied():
    guest = GuestUser("Guest", "Guest123", True, ["settings"])

    result = guest.check_access("settings")

    assert result is False


def test_check_access_inactive():
    guest = GuestUser("Guest", "Guest123", False, [])

    result = guest.check_access("main_page")

    assert result is False


def test_access_control_initialization():
    access_control = AccessControl()

    assert access_control.users == {}


def test_add_user_success():
    access_control = AccessControl()
    user = User("Alex", "Password123")

    result = access_control.add_user(user)

    assert result is True
    assert access_control.users["Alex"] is user


def test_add_user_duplicate():
    access_control = AccessControl()

    user1 = User("Alex", "Password123")
    user2 = User("Alex", "Password456")

    access_control.add_user(user1)
    result = access_control.add_user(user2)

    assert result is False
    assert access_control.users["Alex"] is user1


def test_authenticate_user_success():
    access_control = AccessControl()
    user = User("Alex", "Password123")

    access_control.add_user(user)

    result = access_control.authenticate_user("Alex", "Password123")

    assert result is user


def test_authenticate_user_wrong_password():
    access_control = AccessControl()
    user = User("Alex", "Password123")

    access_control.add_user(user)

    result = access_control.authenticate_user("Alex", "WrongPassword")

    assert result is None


def test_authenticate_user_not_found():
    access_control = AccessControl()

    result = access_control.authenticate_user("Max", "Password123")

    assert result is None


def test_authenticate_user_inactive():
    access_control = AccessControl()
    user = User("Alex", "Password123", False)

    access_control.add_user(user)

    result = access_control.authenticate_user("Alex", "Password123")

    assert result is None


