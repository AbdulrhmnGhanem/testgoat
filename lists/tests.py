from django.test import TestCase


class SmokeTest(TestCase):

    def bad_math(self):
        self.assertEqual(1+1, 3)