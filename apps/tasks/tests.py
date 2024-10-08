from django.test import TestCase
from django.urls import reverse
from apps.core.mixins import SetUpLoggedUserWithTaskMixin, SetUpLoggedUserWithStatusMixin
from apps.tasks.models import Task


class TaskIndexViewTest(SetUpLoggedUserWithTaskMixin, TestCase):

    def test_task_list_view_status_code(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)

    def test_task_list_view_template(self):
        response = self.client.get(reverse('tasks'))
        self.assertTemplateUsed(response, 'apps/tasks/tasks.html')

    def test_task_list_view_context(self):
        response = self.client.get(reverse('tasks'))
        self.assertIn('tasks', response.context)
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertEqual(response.context['tasks'][0].name, 'Test Task')


class TaskCreateViewTest(SetUpLoggedUserWithStatusMixin, TestCase):

    def test_create_task_view_status_code(self):
        response = self.client.get(reverse('tasks_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_task_success(self):
        data = {
            'name': 'New Task',
            'status': self.status.id,
            'description': 'Task description'
        }
        response = self.client.post(reverse('tasks_create'), data)
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(name='New Task').exists())


class TaskUpdateViewTest(SetUpLoggedUserWithTaskMixin, TestCase):

    def test_update_task_view_status_code(self):
        response = self.client.get(reverse('tasks_update',
                                           kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)

    def test_update_task_success(self):
        data = {
            'name': 'Updated Task',
            'status': self.status.id,
            'description': 'Updated description'
        }
        response = self.client.post(reverse('tasks_update',
                                            kwargs={'pk': self.task.pk}), data)
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated description')


class TaskDeleteViewTest(SetUpLoggedUserWithTaskMixin, TestCase):

    def test_delete_task_view_status_code(self):
        response = self.client.get(reverse('tasks_delete',
                                           kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)

    def test_delete_task_success(self):
        response = self.client.post(reverse('tasks_delete',
                                            kwargs={'pk': self.task.pk}))
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(name='Task to Delete').exists())


class TaskSingleViewTest(SetUpLoggedUserWithTaskMixin, TestCase):

    def test_task_detail_view_status_code(self):
        response = self.client.get(reverse('tasks_single',
                                           kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)

    def test_task_detail_view_template(self):
        response = self.client.get(reverse('tasks_single',
                                           kwargs={'pk': self.task.pk}))
        self.assertTemplateUsed(response, 'apps/tasks/task.html')

    def test_task_detail_view_context(self):
        response = self.client.get(reverse('tasks_single',
                                           kwargs={'pk': self.task.pk}))
        self.assertEqual(response.context['task'], self.task)
