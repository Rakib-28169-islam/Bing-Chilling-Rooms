class UserProxy:
    def __init__(self, user):
        self.user = user
        self.permissions = self.get_role_permissions()

    def get_role_permissions(self):
        role_permissions = {
            "admin": ["browse_listings", "manage_users", "view_reports", "delete_account"],
            "host": ["browse_listings", "create_listing", "manage_bookings", "view_earnings"],
            "guest": ["browse_listings", "book_accommodation"],
        }
        return role_permissions.get(self.user.__class__.__name__.lower(), [])

    def execute(self, action, *args):
        if action in self.permissions and hasattr(self.user, action):
            return getattr(self.user, action)(*args)
        return f"Access Denied! {self.user.username} cannot perform {action}."