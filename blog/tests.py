from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            category=self.category_programming,
            author=self.user_trump
        )

        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music,
            author=self.user_obama
        )

        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='category가 없을 수도 있죠.',
            author=self.user_obama
        )

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card)

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
        # Post가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual(soup.title.text, 'Song DALL-E')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')  # id가 post-1인 div를 찾아서, 그 안에
        self.assertIn(self.post_001.title, post_001_card.text)  # title이 있는지
        self.assertIn(self.post_001.category.name, post_001_card.text)  # category가 있는지
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)  # 작성자명이 있는지

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)

        # Post가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')  # id가 main-area인 div태그를 찾습니다.
        self.assertIn('아직 게시물이 없습니다', main_area.text)

    def test_post_detail(self):
        # 0.   Post가 하나 있다.
        # 0.1  그 포스트의 url은 'blog/1/' 이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 1.   첫 번째 post의 detail 페이지 테스트
        # 1.1  첫 번째 post url로 접근하면 정상적으로 작동한다. (status code: 200)
        response = self.client.get(self.post_001.get_absolute_url())
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

        self.category_card_test(soup)

        # 1.3  첫 번째 post의 title이 브라우저 탭에 표기되는 페이지 title에 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 1.4  첫 번째 post의 title이 post-area에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.mname, post_area.text)

        # 1.5  첫 번째 post의 작성자(author)가 post-area에 있다.
        # 아직 작성 불가
        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # 1.6  첫 번째 post의 content가 post-area에 있다.
        self.assertIn(self.post_001.content, post_area.text)

    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absoulte_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.cateogry_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)

        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_create_post(self):
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Song DALL-E', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)