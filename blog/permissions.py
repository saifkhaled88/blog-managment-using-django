from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    """
    Custom permission to allow only the author of a blog to edit or delete it.
    """
    def has_permission(self, request, view):
        # Allow only users with the 'author' role to create blogs
        if request.method in ['POST']:  
            print(f"User making request: {request.user}")
            return request.user.is_authenticated and request.user.role.lower() == 'author'  # Allow other actions to proceed
        return True

    def has_object_permission(self, request, view, obj):
        # Allow only the blog author to edit or delete their own blog
        return obj.user == request.user