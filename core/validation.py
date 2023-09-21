from datetime import datetime

from core import models as core_models
from django.utils.translation import gettext as _
from django.db.models import Q

import logging

logger = logging.getLogger('dart')


def validate_event(event: core_models.Event) -> [core_models.ValidationError]:

    validation_errors = []

    actions = event.actions.all()

    # Don't validate aborted events
    if actions.filter(type=core_models.ActionType.aborted).exists():
        return validation_errors

    # Don't validate duplicates of the 'other' action_type
    distinct_actions = actions.exclude(type=core_models.ActionType.other).values_list('type', flat=True)

    for action_type in distinct_actions:
        if len(actions.filter(type=action_type)) > 1:
            message = _("Event contains duplicate actions")
            err = core_models.ValidationError(event=event, message=message, type=core_models.ErrorType.validation)
            validation_errors.append(err)
            break

    # Validate event does not have duplicate action types
    mission = event.mission
    if event.start_date is None or event.end_date is None:
        message = _("Event is missing start and/or end date")

        err = core_models.ValidationError(event=event, message=message, type=core_models.ErrorType.validation)
        validation_errors.append(err)
    elif event.start_date.date() < mission.start_date or event.start_date.date() > mission.end_date or \
            event.end_date.date() < mission.start_date or event.end_date.date() > mission.end_date:
        message = _("Action occurred outside of mission dates")
        message += " " + mission.start_date.strftime("%Y-%m-%d") + " - " + mission.end_date.strftime("%Y-%m-%d")

        err = core_models.ValidationError(event=event, message=message, type=core_models.ErrorType.validation)
        validation_errors.append(err)

    if event.instrument.type == core_models.InstrumentType.ctd:
        validation_errors += validate_ctd_event(event)
    elif event.instrument.type == core_models.InstrumentType.net:
        validation_errors += validate_net_event(event)

    return validation_errors


# returns a dictionary with keys 'errors' for events not associated with files
# and 'file_errors' for events that are associated with files
def validate_ctd_event(event: core_models.Event) -> [core_models.ValidationError]:

    validation_errors = []

    # Don't validate aborted events
    if event.actions.filter(type=core_models.ActionType.aborted).exists():
        return validation_errors

    if not event.sample_id:
        message = _("Missing a starting sample ID")
        err = core_models.ValidationError(event=event, message=message, type=core_models.ErrorType.validation)
        validation_errors.append(err)

    if not event.end_sample_id:
        message = _("Missing an ending sample ID")
        err = core_models.ValidationError(event=event, message=message, type=core_models.ErrorType.validation)
        validation_errors.append(err)

    return validation_errors


def validate_net_event(event: core_models.Event) -> [core_models.ValidationError]:

    validation_errors = []

    # Don't validate aborted events
    if event.actions.filter(type=core_models.ActionType.aborted).exists():
        return validation_errors

    if not event.attachments.filter(Q(name__iexact='202um') | Q(name__iexact='76um')).exists():
        message = _("Nets must have a '202um' or '76um' attachment")
        err = core_models.ValidationError(event=event, message=message, type=core_models.ErrorType.validation)
        validation_errors.append(err)
    elif not event.sample_id:
        message = _("Missing a starting sample ID")
        err = core_models.ValidationError(event=event, message=message, type=core_models.ErrorType.validation)
        validation_errors.append(err)
    elif event.attachments.filter(name__iexact='76um').exists():
        ctd_events = core_models.Event.objects.filter(instrument__type=core_models.InstrumentType.ctd)
        if not ctd_events.filter(end_sample_id=event.sample_id).exists():
            message = _("No CTD event with matching surface bottle. "
                        "Check the deck sheet to confirm this is a surface bottle")
            message += f" : {event.sample_id}"
            possible_match =ctd_events.filter(sample_id__lte=event.sample_id, end_sample_id__gte=event.sample_id)
            if possible_match.exists():
                message += _(", Likely matches event : ") + str(possible_match.first().event_id)

            err = core_models.ValidationError(event=event, message=message, type=core_models.ErrorType.validation)
            validation_errors.append(err)
    elif event.attachments.filter(name__iexact='202um').exists():
        ctd_events = core_models.Event.objects.filter(instrument__type=core_models.InstrumentType.ctd)
        if not ctd_events.filter(sample_id=event.sample_id).exists():
            message = _("No CTD event with matching bottom bottle. "
                        "Check the deck sheet to confirm this is a bottom bottle")
            message += f" : {event.sample_id}"
            possible_match =ctd_events.filter(sample_id__lte=event.sample_id, end_sample_id__gte=event.sample_id)
            if possible_match.exists():
                message += _(", Likely matches event : ") + str(possible_match.first().event_id)

            err = core_models.ValidationError(event=event, message=message, type=core_models.ErrorType.validation)
            validation_errors.append(err)

    return validation_errors


def validate_bottle_sample_range(event: core_models.Event, bottle_id: int) -> \
        list[core_models.ValidationError]:
    errors = []
    if event.instrument.type == core_models.InstrumentType.ctd and \
            (bottle_id > event.end_sample_id or bottle_id < event.sample_id):
        message = f"Warning: Bottle ID ({bottle_id}) for event {event.event_id} " \
                  f"is outside the ID range {event.sample_id} - {event.end_sample_id}"
        err = core_models.ValidationError(event=event, message=message, type=core_models.ErrorType.missing_id)
        errors.append(err)

    return errors
