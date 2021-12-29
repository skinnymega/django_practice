import datetime
from django.http import response
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

# Create your tests here.
class QuestionIndexViewsTests(TestCase):
    def test_no_questions(self):
        """ if there are no questions a proper message should display"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """ test for checking if question diplayed in index page is too old. returns true if question pub date is displayed"""
        q = create_question("mama mia?", -10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [q])

    def test_future_question(self):
        """test for checking if question displayd in index is in the future. returns true if question is not displayed"""
        create_question("Future of the guris?", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_questions(self):
        """if both exists, only past is displayed """
        create_question("guris?", 35)
        q = create_question("oliver?", -12)
        response = self.client.get(reverse('polls:index'))       
        self.assertQuerysetEqual(response.context['latest_question_list'], [q])

    def test_two_past_questions(self):
        """if there are 2 past questions, both are displayed"""
        q1 = create_question("oliver guris?", -5)
        q2 = create_question("oliver p?", -8)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [q1, q2])


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
            was_published_recently() returns false for questions whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
            was published recently () with question outsided the lower boundry (too old). returns false
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
            was_published_recently() with question within boundries. returns true
        """
        time = timezone.now()
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        f = create_question("ula ula?", 10)
        response = self.client.get(reverse('polls:detail', args=(f.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        p = create_question("mo mo mi?", -99)
        response = self.client.get(reverse('polls:detail', args=(p.id,)))
        self.assertContains(response, p.question_text)