from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class CreditUnion(models.Model):
    """
    Represents a unique credit union instance.
    This serves as the 'master' table for identifying the loan origin.
    """
    # CreditUnionID is automatically created as the primary key by Django
    name = models.CharField(max_length=255, unique=True, help_text="The full legal name of the credit union.")
    address = models.TextField(blank=True, help_text="The physical address.")
    contact_email = models.EmailField(blank=True, help_text="Main contact email for the union.")

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """
    Extends the default User model with a link to CreditUnion.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile', # Access the profile from a User object as user.profile
        help_text="The associated default Django user.",
        primary_key=True # Makes this model's primary key the same as the User's, ensuring 1-to-1 mapping
    )

    # This is the new field relating the User to a CreditUnion
    credit_union = models.ForeignKey(
        CreditUnion,
        on_delete=models.SET_NULL, # Or models.PROTECT, depending on your business rules
        null=True, # Allows the user to not be associated with a CreditUnion initially
        blank=True,
        related_name='users', # Access users from a CreditUnion object as cu.users.all()
        help_text="The Credit Union the user belongs to."
    )

    def __str__(self):
        return f"Profile for {self.user.username}"