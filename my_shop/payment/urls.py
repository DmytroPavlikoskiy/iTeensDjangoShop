from django.urls import path
from payment import views
from .views import (liqpay_callback,
                    # get_payment_data
                )


urlpatterns = [
   path('liqpay/callback/', liqpay_callback, name='liqpay-callback'),
#    path('liqpay/data/<int:order_id>/', get_payment_data, name='liqpay-data'),
] 