import json
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from .models import Product


def _sample_product_kwargs(user):
  return {
    "user": user,
    "name": "Sample Ball",
    "price": 100000,
    "description": "A durable training ball.",
    "category": "football",
    "thumbnail": "https://example.com/ball.jpg"
  }


class MainViewTests(TestCase):
  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user(username="tester", password="secret")

  def test_show_json_requires_no_auth(self):
    Product.objects.create(**_sample_product_kwargs(self.user))
    response = self.client.get(reverse("main:show_json"))
    self.assertEqual(response.status_code, 200)
    data = response.json()
    self.assertEqual(1, len(data))
    self.assertEqual(self.user.username, data[0]["user_username"])

  def test_show_json_mine_requires_login(self):
    response = self.client.get(reverse("main:show_json_mine"))
    self.assertEqual(response.status_code, 302)

    Product.objects.create(**_sample_product_kwargs(self.user))
    self.client.force_login(self.user)
    response = self.client.get(reverse("main:show_json_mine"))
    self.assertEqual(response.status_code, 200)
    data = response.json()
    self.assertEqual(1, len(data))
    self.assertEqual(self.user.id, data[0]["user_id"])
    self.assertEqual(self.user.username, data[0]["user_username"])

  def test_create_product_flutter_assigns_user_from_username(self):
    payload = {
      "username": self.user.username,
      "name": "Flutter Boots",
      "description": "High grip soles.",
      "category": "shoes",
      "thumbnail": "https://example.com/boots.jpg",
      "price": 250000
    }
    response = self.client.post(
      reverse("main:create_product_flutter"),
      data=json.dumps(payload),
      content_type="application/json"
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Product.objects.filter(user=self.user).count(), 1)

  def test_show_json_mine_flutter_honors_username_query(self):
    Product.objects.create(**_sample_product_kwargs(self.user))
    response = self.client.get(reverse("main:show_json_mine_flutter"), {"username": self.user.username})
    self.assertEqual(response.status_code, 200)
    data = response.json()
    self.assertEqual(data["count"], 1)
    self.assertEqual(len(data["products"]), 1)
    self.assertEqual(self.user.username, data["products"][0]["user_username"])

  def test_create_product_flutter_validates_price(self):
    payload = {
      "username": self.user.username,
      "name": "Faulty Item",
      "description": "",
      "category": "football",
      "thumbnail": "",
      "price": ""
    }
    response = self.client.post(
      reverse("main:create_product_flutter"),
      data=json.dumps(payload),
      content_type="application/json"
    )
    self.assertEqual(response.status_code, 400)