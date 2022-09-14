from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Home', navbar.text)
        self.assertIn('About us', navbar.text)
        self.assertIn('How to use', navbar.text)
        self.assertIn('Create', navbar.text)
        self.assertIn('Review', navbar.text)

        logo_btn = navbar.find('a', text='Song DALL-E')
        self.assertEqual(logo_btn.attrs['href', '/'])

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href', '/'])

        about_us_btn = navbar.find('a', text='About Us')
        self.assertEqual(about_us_btn.attrs['href'], '/about_us/')

        how_to_use_btn = navbar.find('a', text='How to use')
        self.assertEqual(how_to_use_btn.attrs['href'], '/how_to_use/')

        create_btn = navbar.find('a', text='Create')
        self.assertEqual(create_btn.attrs['href'], '/create/')

        blog_btn = navbar.find('a', text='Review')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

    def test_post_list(self):
        # 1.1. 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        # 1.2. 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 1.3. 페이지 타이틀은 'Song DALL-E'이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Song DALL-E')
        # 1.4. 내비게이션 바가 있다.
        # navbar = soup.nav
        # 1.5. Home, About Us, How to user, Create, Review라는 문구가 내비게이션 바에 있다.
        # self.assertIn('Home', navbar.text)
        # self.assertIn('About us', navbar.text)
        # self.assertIn('How to use', navbar.text)
        # self.assertIn('Create', navbar.text)
        # self.assertIn('Review', navbar.text)
        self.navbar_test(soup)

        # 2.1. 포스트(게시물)가 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # 2.2. main area에 '아직 게시물이 없습니다.'라는 문구가 나타난다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 3.1. 포스트가 2개 있다면
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            author=self.user_trump
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            author=self.user_obama
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3.2. 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        # 3.3. main area에 포스트 2개의 제목이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 3.4. '아직 게시물이 없습니다.'라는 문구는 더 이상 나타나지 않는다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

    def test_post_detail(self):
        # 0.   Post가 하나 있다.
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            author=self.user_trump,
        )
        # 0.1  그 포스트의 url은 'blog/1/' 이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 1.   첫 번째 post의 detail 페이지 테스트
        # 1.1  첫 번째 post url로 접근하면 정상적으로 작동한다. (status code: 200)
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1.2  post_list 페이지와 똑같은 네비게이션 바가 있다.
        # navbar = soup.nav  # beautifulsoup를 이용하면 간단히 페이지의 태그 요소에 접근이 가능합니다.
        # self.assertIn('Home', navbar.text)
        # self.assertIn('About us', navbar.text)
        # self.assertIn('How to use', navbar.text)
        # self.assertIn('Create', navbar.text)
        # self.assertIn('Review', navbar.text)
        self.navbar_test(soup)

        # 1.3  첫 번째 post의 title이 브라우저 탭에 표기되는 페이지 title에 있다.
        self.assertIn(post_001.title, soup.title.text)

        # 1.4  첫 번째 post의 title이 post-area에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        # 1.5  첫 번째 post의 작성자(author)가 post-area에 있다.
        # 아직 작성 불가
        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # 1.6  첫 번째 post의 content가 post-area에 있다.
        self.assertIn(post_001.content, post_area.text)
