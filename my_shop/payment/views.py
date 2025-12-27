import base64
import json
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .models import Order, Payment
from .utils import get_liqpay_context



def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    liqpay_context = get_liqpay_context(order)
    Payment.objects.create(
        order=order,
        liqpay_data=liqpay_context['data'],
        liqpay_signature=liqpay_context['signature']
    )

    return render(request, 'stors/payment.html', {
        'order': order,
        'liqpay_data': liqpay_context['data'],
        'liqpay_signature': liqpay_context['signature'],
    })

@api_view(['POST'])
def checkout(request):
    user = request.user
    total_price = request.data.get('total_price')

    if not total_price:
        return Response({"error": "total_price is required"}, status=400)

    order = Order.objects.create(
        user=user,
        total_price=total_price
    )

    send_mail(
        subject='Нове замовлення',
        message=f'Замовлення №{order.id} успішно створене.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=True,
    )

    return Response({
        "order_id": order.id,
        "payment_url": f"/payments/{order.id}/"
    })

@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def liqpay_callback(request):
    data = request.data.get('data')
    signature = request.data.get('signature')

    if not data or not signature:
        return Response({"error": "Invalid payload"}, status=400)

    try:
        decoded_data = base64.b64decode(data).decode()
        payload = json.loads(decoded_data)
    except Exception:
        return Response({"error": "Invalid data format"}, status=400)

    order_id = payload.get('order_id')
    status = payload.get('status')

    if not order_id:
        return Response({"error": "order_id missing"}, status=400)

    order = get_object_or_404(Order, id=order_id)

    if status in ('success', 'sandbox'):
        order.status = 'paid'
    elif status in ('failure', 'error', 'expired'):
        order.status = 'failed'
    elif status == 'reversed':
        order.status = 'failed'  # або refunded
    else:
        order.status = 'failed'

    order.save()

    return Response({"status": "ok"})

