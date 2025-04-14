from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from orders_app.models import Order
from offers_app.models import Offer, OfferDetails
from profile_app.models import UserProfile
from reviews_app.models import Reviews



def create_and_login_test_user(self):
    self.user = User.objects.create_user(
        username='testuser', email='test@mail.com', is_staff=True) 
    self.token = Token.objects.create(user=self.user)
    self.client = APIClient()
    self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

def create_test_customer_userprofile(self):
    self.userprofile = UserProfile.objects.create(
        user=self.user,
        type='customer',
        username='testuser',
        email='test@mail.com'
    )

def create_SECOND_test_user(self):
    self.second_user = User.objects.create_user(
        username='second_testuser', email='second_test@mail.com')
    
def login_second_test_user(self):
    self.token = Token.objects.create(user=self.second_user)
    self.client = APIClient()
    self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


def create_test_business_userprofile(self):
    self.userprofile = UserProfile.objects.create(
        user=self.user,
        type='business',
        username='testuser',
        email='test@mail.com'
    )

def create_test_review(self):
    self.review = Reviews.objects.create(business_user= self.second_user,
    reviewer = self.user,
    rating= 2,
    description= "Alles war toll!")

def create_test_offer(self):
    self.offer = Offer.objects.create(
        user_id=self.user.id,
        title="Grafikdesign-Paket",
        image="",
        description="Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    )


def create_test_offerdetails(self):
    self.offerdetails = OfferDetails.objects.create(
        offer_id=self.offer.id,
        title="Basic Design",
        revisions=2,
        delivery_time_in_days=5,
        price=100,
        features=["Logo Design", "Visitenkarte"],
        offer_type="basic"
    )

    self.offerdetails = OfferDetails.objects.create(
        offer_id=self.offer.id,
        title="Standard Design",
        revisions=5,
        delivery_time_in_days=7,
        price=200,
        features=["Logo Design", "Visitenkarte", "Briefpapier"],
        offer_type="standard"
    )

    self.offerdetails = OfferDetails.objects.create(
        offer_id=self.offer.id,
        title="Premium Design",
        revisions=10,
        delivery_time_in_days=10,
        price=500,
        features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
        offer_type="premium"
    )


def create_test_order(self):
    self.order = Order.objects.create(
        customer_user=self.user,
        business_user=self.second_user,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=[
            "Logo Design",
            "Visitenkarten"
        ],
        offer_type="basic",
        status="in_progress"
    )