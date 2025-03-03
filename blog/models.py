from django.db import models
from django.utils.timezone import now

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)   
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, blank=True, null=True)   
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=now, blank=True)

    # Add these attributes to make Django's authentication system work
    is_active = models.BooleanField(default=True)  # Required for authentication
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_superuser = models.BooleanField(default=False)  # Required for admin access


    # These attributes are required to make Django happy
    REQUIRED_FIELDS = ['email']  # Required when creating a user
    USERNAME_FIELD = 'username'  # Used for authentication

    def __str__(self):
        return self.username
    
    # Make Django happy without using its auth system
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def has_perm(self, perm, obj=None):
        """Grant all permissions to superusers."""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Grant app-level permissions to superusers."""
        return self.is_superuser

    def get_username(self):
        return self.username

    class Meta:
        managed = True
        db_table = 'users'



class Categories(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'categories'



class Blogs(models.Model):
    blog_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(blank=True, default=now)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)  # Change category_id to category
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # Change user_id to user

    class Meta:
        managed = True
        db_table = 'blogs'


# class BlogCategories(models.Model):
#     blog = models.ForeignKey(Blogs, on_delete= models.CASCADE)
#     category = models.ForeignKey(Categories, models.DO_NOTHING)     

#     class Meta:
#         managed = False
#         db_table = 'blog_categories'

class Comments(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(blank=True, default=now)
    blog = models.ForeignKey(Blogs, on_delete= models.CASCADE)
    user = models.ForeignKey(Users, on_delete= models.CASCADE)

    class Meta:
        managed = True
        db_table = 'comments'
