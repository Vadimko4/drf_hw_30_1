from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentDetailSerializer, PaymentSerializer, UserSerializer
from users.services import convert_rub_to_dollars, create_stripe_product_and_price


# class PaymentCreateAPIView(CreateAPIView):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
#
#     def perform_create(self, serializer):
#         payment = serializer.save(user=self.request.user)
#         amount_in_dollars = convert_rub_to_dollars(payment.amount)
#         price = create_stripe_price(amount_in_dollars)
#         session_id, payment_link = create_stripe_session(price)
#         payment.session_id = session_id
#         payment.link = payment_link
#         payment.save()


# class PaymentViewSet(ModelViewSet):
#     queryset = Payment.objects.all()
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
#     filterset_fields = ("course", "lesson", "type",)
#     ordering_fields = ("-date",)
#
#     def get_serializer_class(self):
#         if self.action == "retrieve":
#             return PaymentDetailSerializer
#         return PaymentSerializer
#
#     def perform_create(self, serializer):
#         payment = serializer.save(user=self.request.user)
#         amount_in_dollars = convert_rub_to_dollars(payment.amount)
#         price = create_stripe_price(amount_in_dollars)
#         session_id, payment_link = create_stripe_session(price)
#         payment.session_id = session_id
#         payment.link = payment_link
#         payment.save()


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ("course", "lesson", "type",)
    ordering_fields = ("-date",)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer

    def perform_create(self, serializer):
        # Сохраняем платеж с пользователем
        payment = serializer.save(user=self.request.user)

        # Если платеж через Stripe
        if payment.type == 'transaction':
            # Создаем продукт, цену и сессию в Stripe
            session_id, payment_link = create_stripe_product_and_price(payment)

            if not session_id:
                raise serializers.ValidationError("Ошибка создания платежной сессии")

            # Сохраняем данные из Stripe
            payment.session_id = session_id
            payment.link = payment_link
            payment.save()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password) #  устанавливаем пароль пользователю в захешированном виде
        user.save()
