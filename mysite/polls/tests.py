import datetime

from django.test import TestCase
from django.utils import timezone

from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
    
    # Test를 실행 할때는 def명 은 'test_'로 시작한다.
    def test_was_published_recently_with_future_question(self):
        # was_publicshed_recently() return False for questions whose pub_date is in the future
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        # was_published_recently() returns False for Questions whose pub_date is older than 1 day.
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        # was_published_recently() returns True for questions whose pub_date is within the last day.
        time = timezone.now() - datetime.timedelta(hours=23, minutes= 59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    # Create a question with the given 'question_text' and published 
    # the given number of 'days' offset to now
    # (negative for questions published in the past, 
    # positive for questions that have yet th be published).

    time=timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
   
class QuestionIndexViewTests(TestCase):
        # 사이트에서 관리자 입력 및 사용자 경험에 대한 이야기를 하는 테스트를 만들었고, 
        # 모든 상태와 시스템 상태의 모든 새로운 변경 사항에 대해 예상하는 결과가 출력 
        # 되는지 확인 한다.
      
        # Def Explain
        # create_question       : 질문 생성 함수
        # test_no_questions     : 질문을 생성하지 않지만 "No polls are available." 메시지 및 latest_question_list가 비어있음을 확인한다.
        # test_past_question    : 질문을 생성하고 그 질문이 리스트에 나타나는지 확인합니다.
        # test_future_question  : 미래의 pub_date로 질문을 만든다. 데이터베이스는 각 테스트 메소드마다 재설정되므로 첫 번째 질문은 더 이상 존재 하지 않으므로 다시 인덱스에 질문이 없어야 한다.
      
        # django.test.TestCase 클래스는 몇 가지 추가적인 선언 메소드를 제공한다.
        # assertContains()      : Response 인스턴스가 주어진 status_code를 생성하고 해당 텍스트가 응답 컨텐츠에 표시 되도록 지정한다.
        # assertQuerysetEqual() : 질의 집합 response가 특정 값 목록을 반환 하도록 지정합니다.
        # 을 사용한다.


    def test_no_questions(self):
        # If no questions exist, an appropriate message is displayed.

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        # Questions with a pub_date in the past are displayed on the index page
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ["<Question: Past question.>"]
        )

    def test_future_question(self):
        # Questions with a pub_date in the future aren't displayed on the index page.
        create_question(question_text="Future qestion.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        # Even if both past and future questions exist, only past questions are displayed.

        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ["<Question: Past question.>"]
        )

    def test_two_past_questions(self):
        # The questions index page may display multiple questions.
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ["<Question: Past question 2.>", "<Question: Past question 1.>"]
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)