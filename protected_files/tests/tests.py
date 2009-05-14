from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType


class ProtectedFileTest(TestCase):
    urls = 'protected_files.tests.urls'
    
    def setUp(self):
        super(ProtectedFileTest, self).setUp()
        self.users = []
        u = User.objects.create_user('has_perms', 'has_perms@testserver.com', '!')
        ct = ContentType.objects.get(app_label="auth", model="user")
        perm = Permission.objects.get(content_type=ct, codename='add_user')
        u.user_permissions.add(perm)
        self.users.append(u)
        
        u = User.objects.create_user('no_perms', 'no_perms@testserver.com', '!')
        self.users.append(u)
        
    def tearDown(self):
        for u in self.users:
            u.delete()
    
    def testPermUser(self):
        "User with permissions has access"
        # this test fails with cache middleware enabled
        # http://code.djangoproject.com/ticket/5176
        response = self.client.login(username='has_perms', password='!')
        response = self.client.get('/perms/file.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Accel-Redirect'], '/file.txt')
        
    def testAnonymousUser(self):
        "Anonymous users never have access"
        response = self.client.get('/perms/file.txt')
        self.assertEqual(response.status_code, 403)
        
    def testNoPermUser(self):
        "User without permissions is forbidden"
        response = self.client.login(username='no_perms', password='!')
        response = self.client.get('/perms/file.txt')
        self.assertEqual(response.status_code, 403)
        
    def testMultiLevelPath(self):
        "We can drill-down inside a directory"
        # this test fails with cache middleware enabled
        # http://code.djangoproject.com/ticket/5176
        response = self.client.login(username='has_perms', password='!')
        response = self.client.get('/perms/dir1/dir2/file.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Accel-Redirect'],
                                                '/dir1/dir2/file.txt')
                                
    def testAltRoot(self):
        "Specifying an alternate root directory"
        # this test fails with cache middleware enabled
        # http://code.djangoproject.com/ticket/5176
        response = self.client.login(username='has_perms', password='!')
        response = self.client.get('/alt-root/file.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Accel-Redirect'],
                                                '/alt/root/path/file.txt')
                          
    def testNoPerms(self):
        "Forbidden if permissions aren't specified"
        response = self.client.login(username='has_perms', password='!')
        response = self.client.get('/no-perms/file.txt')
        self.assertEqual(response.status_code, 403)
        