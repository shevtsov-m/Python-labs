
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password_hash = hash_password(password)
        self.is_active = is_active

    def verify_password(self, password):
        return self.password_hash == hash_password(password)


class Administrator(User):
    def __init__(self, username, password, is_active, permissions):
        super().__init__(username, password, is_active)
        self.permissions = permissions

    def ban_user(self, user):
        if 'ban_users' not in self.permissions:
            print("Permission denied")
            return False

        user.is_active = False
        print(f"User {user.username} has been deactivated")
        return True

    def delete_user(self, user, access_control):
        if 'delete_users' not in self.permissions:
            print("Permission denied")
            return False

        if access_control.users.get(user.username) is not user:
            print("User not found")
            return False

        del access_control.users[user.username]
        print(f"User {user.username} deleted")
        return True


class RegularUser(User):
    def __init__(self, username, password, is_active, last_login,
                 login_count, email):
        super().__init__(username, password, is_active)
        self.last_login = last_login
        self.login_count = login_count
        self.email = email

    def update_profile(self, username, email, access_control=None):
        if not self.is_active:
            print("Account is inactive")
            return False

        old_username = self.username

        if access_control is not None:
            if username != old_username and username in access_control.users:
                print("Username is already taken")
                return False

            if access_control.users.get(old_username) is self:
                del access_control.users[old_username]
                self.username = username
                self.email = email
                access_control.users[username] = self
                print("Profile updated")
                return True

        self.username = username
        self.email = email
        print("Profile updated")
        return True


class GuestUser(User):
    def __init__(self, username, password, is_active, access_restrictions):
        super().__init__(username, password, is_active)
        self.access_restrictions = access_restrictions

    def check_access(self, resource):
        if not self.is_active or resource in self.access_restrictions:
            print("Permission denied")
            return False

        print("Permission accepted")
        return True


class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        if user.username in self.users:
            print("Username is already registered")
            return False

        self.users[user.username] = user
        print(f"User {user.username} added")
        return True

    def authenticate_user(self, username, password):
        user = self.users.get(username)

        if user is not None:
            if user.is_active and user.verify_password(password):
                return user

        return None


access_control = AccessControl()



admin = Administrator(
    "Admin",
    "Admin123",
    True,
    ["ban_users", "delete_users", "manage_users"]
)

access_control.add_user(admin)



guest = GuestUser(
    "Guest",
    "Guest123",
    True,
    ["settings", "user_management"]
)

access_control.add_user(guest)



print("\n=== User registration ===")

user = RegularUser(
    username=input("Username: "),
    password=input("Password: "),
    is_active=True,
    last_login=input("Last login: "),
    login_count=int(input("Login count: ")),
    email=input("Email: ")
)

access_control.add_user(user)



print("\n=== Registered users ===")

for item in access_control.users.values():
    print(item.username, item.is_active)



print("\n=== Authentication ===")

username = input("Username: ")
password = input("Password: ")

result = access_control.authenticate_user(username, password)

if result is not None:
    print(f"Authentication successful: {result.username}")
else:
    print("Authentication error")



print("\n=== Wrong password test ===")

result = access_control.authenticate_user(user.username, "WrongPassword")

if result is None:
    print("Authentication error")



print("\n=== Profile update ===")

new_username = input("New username: ")
new_email = input("New email: ")

user.update_profile(new_username, new_email, access_control)

print(user.username, user.email)



print("\n=== Guest access ===")

guest.check_access("main_page")
guest.check_access("settings")
guest.check_access("user_management")



print("\n=== Administrator permissions ===")

limited_admin = Administrator(
    "Moderator",
    "Moderator123",
    True,
    ["manage_users"]
)

limited_admin.ban_user(guest)



print("\n=== User blocking ===")

admin.ban_user(user)

result = access_control.authenticate_user(user.username, password)

if result is None:
    print("User cannot authenticate: account is inactive")



print("\n=== User deletion ===")

admin.delete_user(user, access_control)

result = access_control.authenticate_user(user.username, password)

if result is None:
    print("User is not registered")



print("\n=== Final users ===")

for item in access_control.users.values():
    print(item.username, item.is_active)
