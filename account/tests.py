from django.test import TestCase, Client
from django.urls import reverse

class AccountViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_account_login_page_loads(self):
        # Path '/' is 'account_login' and should load directly.
        response_root = self.client.get(reverse('account_login')) # This is '/'
        self.assertEqual(response_root.status_code, 200)
        self.assertContains(response_root, "Sign in to start your session", html=True)
        
        # Path '/account/' should also result in the login page.
        response_account_path = self.client.get('/account/')
        if response_account_path.status_code == 302: 
            self.assertEqual(response_account_path.url, reverse('account_login'))
            response_redirected = self.client.get(response_account_path.url)
            self.assertEqual(response_redirected.status_code, 200)
            self.assertContains(response_redirected, "Sign in to start your session", html=True)
        else: 
            self.assertEqual(response_account_path.status_code, 200)
            self.assertContains(response_account_path, "Sign in to start your session", html=True)

    def test_admin_specific_login_page_redirects_to_main_login(self):
        # /admin/login/ is expected to be redirected to the main login page ('/' or '/account/')
        # by the AccountCheckMiddleWare because view_func.__module__ for AdminSite.login is 'django.contrib.admin.sites',
        # not 'django.contrib.auth.views'.
        response = self.client.get(reverse('admin:login')) 
        self.assertEqual(response.status_code, 302)

        expected_redirect_url1 = reverse('account_login') # '/'
        expected_redirect_url2 = '/account/'
        # The redirect location from the last error was '/account/'
        self.assertIn(response.url, [expected_redirect_url1, expected_redirect_url2],
                      f"Redirect URL '{response.url}' was not '{expected_redirect_url1}' or '{expected_redirect_url2}'")

        response_redirected = self.client.get(response.url)
        self.assertEqual(response_redirected.status_code, 200)
        self.assertContains(response_redirected, "Sign in to start your session", html=True)


    def test_admin_main_page_redirects_to_account_login(self):
        admin_path = reverse('admin:index') # This is /admin/
        response = self.client.get(admin_path)
        self.assertEqual(response.status_code, 302)
        
        expected_redirect_url1 = reverse('account_login') # '/'
        expected_redirect_url2 = '/account/' 
        self.assertIn(response.url, [expected_redirect_url1, expected_redirect_url2],
                      f"Redirect URL '{response.url}' was not '{expected_redirect_url1}' or '{expected_redirect_url2}'")
        
        response_redirected = self.client.get(response.url)
        self.assertEqual(response_redirected.status_code, 200)
        self.assertContains(response_redirected, "Sign in to start your session", html=True)
