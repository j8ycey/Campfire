from common.json import ModelEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


from .models import Activity, Event, UserVO
import json


class UserVOEncoder(ModelEncoder):
    model = UserVO
    properties = ["id", "username", "first_name", "last_name", "email"]


class ActivityEncoder(ModelEncoder):
    model = Activity
    properties = ["id", "name", "picture_url"]


class EventEncoder(ModelEncoder):
    model = Event
    properties = [
        "id",
        "name",
        "latitude",
        "longitude",
        "start",
        "end",
        "description",
        "owner",
        "activity",
        "attendees",
        "picture_url",
    ]
    encoders = {
        "activity": ActivityEncoder(),
        "owner": UserVOEncoder(),
        "attendees": UserVOEncoder(),
    }


# # Create your views here.
@require_http_methods(["GET"])
def list_all_uservos(request):
    if request.method == "GET":
        uservos = UserVO.objects.all()
        for user in uservos:
            print(user)

        return JsonResponse(
            {"UserVOs": uservos},
            encoder=UserVOEncoder,
            safe=False,
        )


# Create your views here.
@require_http_methods(["GET", "POST"])
def list_all_events(request):

    print("Hitting protected view")
    print("Hitting protected view")
    print("Hitting protected view")

    if request.method == "GET":
        events = Event.objects.all()
        return JsonResponse(
            {"Events": events},
            encoder=EventEncoder,
            safe=False,
        )
    if request.method == "POST":
        content = json.loads(request.body)
        content["owner"] = UserVO.objects.get(id=content["owner"])
        content["activity"] = Activity.objects.get(id=content["activity"])
        event = Event.objects.create(**content)
        return JsonResponse(
            {"Event": event},
            encoder=EventEncoder,
            safe=False,
        )


@require_http_methods(["GET", "PUT", "DELETE"])
def show_event(request, pk):
    if request.method == "GET":
        try:
            event = Event.objects.get(id=pk)
            return JsonResponse(
                {"Event": event},
                encoder=EventEncoder,
                safe=False,
            )
        except Event.DoesNotExist:
            return JsonResponse("Event does not exist.", status=400)
    elif request.method == "PUT":
        content = json.loads(request.body)
        event = Event.objects.get(id=pk)
        try:
            if "activity" in content:
                activity = Activity.objects.get(id=content["activity"])
                content["activity"] = activity
            if "owner" in content:
                owner = UserVO.objects.get(id=content["owner"])
                content["owner"] = owner
            if "attendees" in content:
                attendees_id_list = content["attendees"]
                for id in attendees_id_list:
                    attendees = UserVO.objects.get(id=id)
                    event.attendees.add(attendees)
            props = [
                "name",
                "activity",
                "owner",
                "description",
                "start",
                "end",
                "latitude",
                "longitude",
                "picture_url",
            ]
            for prop in props:
                if prop in content:
                    setattr(event, prop, content[prop])
            event.save()
            return JsonResponse(
                event,
                encoder=EventEncoder,
                safe=False,
            )

        except Event.DoesNotExist:
            response = JsonResponse({"message": "Does not exist"})
            response.status_code = 404
            return response

    elif request.method == "DELETE":
        Event.objects.get(id=pk).delete()
        count, _ = Event.objects.filter(id=pk).delete()
        return JsonResponse({"Deleted": count == 0})

    return render(request, "thispage.html")


@require_http_methods(["GET"])
def list_users_events(request, pk):
    if request.method == "GET":
        logged_in_user = UserVO.objects.filter(id=pk)
        events = Event.objects.all()
        users_events = []
        for event in events:
            if logged_in_user in event.attendees.objects.all():
                users_events.append(event)
        return JsonResponse(
            {"User's Events": users_events},
            encoder=EventEncoder,
            safe=False,
        )


@require_http_methods(["GET", "POST"])
def list_all_activities(request):
    if request.method == "GET":
        activities = Activity.objects.all()
        return JsonResponse(
            {"Activities": activities},
            encoder=ActivityEncoder,
            safe=False,
        )
    if request.method == "POST":
        content = json.loads(request.body)
        activities = Activity.objects.create(**content)
        return JsonResponse(
            {"Activities": activities},
            encoder=ActivityEncoder,
            safe=False,
        )


@require_http_methods(["GET", "PUT", "DELETE"])
def show_activity(request, pk):
    if request.method == "GET":
        try:
            activity = Activity.objects.get(id=pk)
            return JsonResponse(
                {"Activity": activity},
                encoder=ActivityEncoder,
                safe=False,
            )
        except Activity.DoesNotExist:
            return JsonResponse("Activity does not exist.", status=400)
    elif request.method == "PUT":
        content = json.loads(request.body)
        try:
            Activity.objects.filter(id=pk).update(**content)
            activity = Activity.objects.get(id=pk)
        except Activity.DoesNotExist:
            return JsonResponse("Activity does not exist", status=400)
        return JsonResponse(
            {"Activity": activity},
            encoder=ActivityEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        Activity.objects.get(id=pk).delete()
        count, _ = Activity.objects.filter(id=pk).delete()
        return JsonResponse({"Deleted": count == 0})
