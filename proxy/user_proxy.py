# proxy/user_proxy.py
class UserProxy:
    def __init__(self, user):
        self.user = user
        self.permissions = self.get_role_permissions()

    def get_role_permissions(self):
        # Check if user is None
        if not self.user:
            return []
            
        role_permissions = {
            "admin": ["browse_listings", "manage_users", "view_reports", "delete_account"],
            "host": ["browse_listings", "create_listing", "manage_bookings", "view_earnings", "delete_listing"],
            "guest": ["browse_listings", "book_accommodation"],
        }
        return role_permissions.get(self.user.getUserType().lower(), [])
        #return role_permissions.get(self.user.__class__.__name__.lower(), [])

    def execute(self, action, *args):
        # Check if user is None
        if not self.user:
            return "Access Denied! User not logged in."
            
        if action in self.permissions and hasattr(self.user, action):
            return getattr(self.user, action)(*args)
        return f"Access Denied! {self.user.getName()} cannot perform {action}."