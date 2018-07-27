from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rbms.models import Room, Booking

start_template = """
<html>
    <body>
        <ul>
            <li><a href="">Dodaj nową salę</a></li>
        </ul>
        <div>
            {}
        </div>
    </body>
</html>
"""

room_add_form = """
    <form action="#" method="POST">
        <label>Nazwa sali:
            <input type="text" name="name">
        </label><br><br>
        <label>Liczba miejsc siedzących:
            <input type="number" name="seats">
        </label><br><br>
         <label>Czy ma projektor?
            <select name="has_projector">
                <option value="True">Tak</option>
                <option value="True">Nie</option>
            </select>
        </label><br><br>
        <input type="submit" name="send" value="Stwórz">
    </form>
    """

@csrf_exempt
def new_room(request):
    if request.method == "GET":
        return HttpResponse(start_template.format(room_add_form))
    elif request.method == "POST":
        if request.POST.get("name") and request.POST.get("seats"):
            Room.objects.create(
                name=request.POST.get("name"),
                seats=int(request.POST.get("seats")),
                has_projector=request.POST.get("has_projector")
            )
            return HttpResponse("Sala dodana. Tutaj powinien być link do listy sal.")
        else:
            return HttpResponse("Brakuje danych w formularzu.")


@csrf_exempt
def modify_room(request, id):

    try:
        room_data = Room.objects.get(id=id)
    except ObjectDoesNotExist:
        return Http404

    room_modify_html = f"""
        <form action="#" method="POST">
            <label>Nazwa sali:
                <input type="text" name="name" value={room_data.name}>
            </label><br><br>
            <label>Liczba miejsc siedzących:
                <input type="number" name="seats" value={room_data.seats}>
            </label><br><br>
             <label>Czy ma projektor?
                <select name="has_projector"  value={room_data.has_projector}>
                    <option value="True">Tak</option>
                    <option value="True">Nie</option>
                </select>
            </label><br><br>
            <input type="submit" name="send" value="Modyfikuj">
        </form>
        """

    if request.method == "GET":
        return HttpResponse(start_template.format(room_modify_html))
    elif request.method == "POST":
        if request.POST.get("name") and request.POST.get("seats"):
            room_data.name = request.POST.get("name")
            room_data.seats = request.POST.get("seats")
            room_data.has_projector = request.POST.get("has_projector")
            room_data.save()
            return HttpResponse("Sala zmodyfikowana. Tutaj powinien być link do listy sal.")
        else:
            return HttpResponse("Brakuje danych w formularzu.")


def delete_room(request, id):

    return HttpResponse("Nothing yet.")


def show_room(request, id):

    return HttpResponse("Nothing yet.")


def view_all(request):

    return HttpResponse("Nothing yet.")
