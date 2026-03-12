""" helper utils """
from django.utils import timezone
from booki.models import Reserve


def update_pending_reservations(user=None, library=None):
    """ Update pending reservations """
    current_time = timezone.now()
    if user:
        reservations = Reserve.objects.filter(status=Reserve.Status.PENDING, user=user)
    elif library:
        reservations = Reserve.objects.filter(status=Reserve.Status.PENDING, library=library)
    else:
        reservations = Reserve.objects.filter(status=Reserve.Status.PENDING)
    for reservation in reservations:
        if reservation.reject_at < current_time:
            reservation.status = Reserve.Status.REJECTED
            reservation.save()
