from django.test import TestCase
from django.contrib.auth.models import User
from .models import TodoModel
# Create your tests here.

class TodoTest(TestCase):
    """Test model methods."""
    user = None

    def setUp(self):
        self.user = User.objects.create(
            username='test'
        )

    def test_check_user(self):
        todo, created = TodoModel.objects.create_for_user(
            user="I am a user",
            name="Test Todo"
        )
        self.assertFalse(created)


    def test_create_todo(self):
        """Test Todo creation."""
        todo, created = TodoModel.objects.create_for_user(
            user=self.user,
            name="Test Todo"
        )
        self.assertTrue(createv=True)
        todo, created = TodoModel.objects.create_for_user(user=self.user, description="Test")
        self.assertFalse(created) # No name passed

    def test_update_for_user(self):
        """Test todo update."""
        todo, created = TodoModel.objects.create_for_user(user=self.user, name="Test todo")
        todo, updated = TodoModel.objects.update_for_user(user=user, id=todo.pk, name="Test updated")
        self.assertTrue(updated) 
        todo, updated = TodoModel.objects.update_for_user(user=user, id=todo.pk, description="")
        self.assertTrue(updated) # description is not null, so it should be updated
        todo, updated = TodoModel.objects.update_for_user(user=user, id=todo.pk)
        self.assertFalse(updated) # No parameter to update

    def test_delete_for_user(self):
        todo, created = TodoModel.objects.create_for_user(user=self.user, name="Test todo")
        todo, deleted = TodoModel.objects.delete_for_user(user=self.user)
        self.assertTrue(deleted=True)