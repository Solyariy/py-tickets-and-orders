from db.models import Order, Ticket, User, MovieSession
from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime


def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        movie_session = MovieSession.objects.get(
            pk=tickets[0].get("movie_session")
        )
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        tickets = [
            Ticket(
                row=data.get("row"),
                seat=data.get("seat"),
                movie_session=movie_session,
                order=order
            )
            for data in tickets
        ]
        Ticket.objects.bulk_create(tickets)
        order.tickets.set(tickets)
        order.save()
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
