from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rbms.models import Room, Booking

# Simple general website form with added menu
start_template = """
<html>
    <body>
        <h4 style="margin-bottom: 0px">Room Booking Management System</h4>
        <ul style="list-style-type: none;">
            <li style="display: inline;">
                <a href="/">Home</a> &nbsp
            </li>
            <li style="display: inline;">
                <a href="/room/new">Dodaj nową salę</a> &nbsp
                </li>
            <li style="display: inline;">
                <a href="/search">Wyszukaj salę</a> &nbsp
            </li>
        </ul>
        <p>&nbsp</p>
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
                <option value="False">Nie</option>
            </select>
        </label><br><br>
        <input type="submit" name="send" value="Stwórz">
    </form>
    """

room_list_table = """
<table style="border: 1px solid black; border-collapse: collapse" >
    <thead>
        <tr style="border: 1px solid black; border-collapse: collapse">
            <th style="border: 1px solid black">Nazwa pomieszczenia &nbsp</th>
            <th style="border: 1px solid black">Status dostępności &nbsp</th>
            <th style="border: 1px solid black">Rezerwacja &nbsp</th>
            <th style="border: 1px solid black">Edycja &nbsp</th>
            <th style="border: 1px solid black">Usuwanie &nbsp</th>
        </tr>
    </thead>
    <tbody>
        {}
    </tbody>
</table>
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

            return redirect(reverse("view_all"))

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
        """

    if room_data.has_projector is True:
        room_modify_html += """<option selected value="True">Tak</option>
                    <option value="False">Nie</option>"""
    else:
        room_modify_html += """<option value="True">Tak</option>
                            <option selected value="False">Nie</option>"""

    room_modify_html += """</select>
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
            return redirect(reverse("view_all"))
        else:
            return HttpResponse("Brakuje danych w formularzu.")


def delete_room(request, id):
    try:
        marked_room = Room.objects.get(id=id)
        marked_room.delete()
        return redirect(reverse("view_all"))
    except ObjectDoesNotExist:
        return HttpResponse("Nie ma sali o tym numerze.")


def show_room(request, id):
    try:
        room = Room.objects.get(id=id)
        projector_available = "Tak" if room.has_projector is True else "Nie"

        room_display_html = f"""
        <h2>{room.name}</h2>
        <p>Liczba miejsc: {room.seats}</p>
        <p>Projektor: {projector_available}</p>
        <p><a href="/room/reservation/{room.id}">Zarezerwuj</a></p>
        <p>Zajęta w dniach:</p>
        <ul>
        """

        # Add reserved dates
        room_display_html += ""

        # Or no reservations

        # Finish list
        room_display_html += "</ul>"

        return HttpResponse(start_template.format(room_display_html))
    except ObjectDoesNotExist:
        return HttpResponse("Nie ma sali o tym numerze.")


def view_all(request):
    room_data = Room.objects.all().order_by("name")

    table_rows = ""
    for room in room_data:
        table_rows += f"""
        <tr style="border: 1px solid black">
            <td>
                <a href="/room/{room.id}">{room.name}</a>
            </td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">
                <a href="/room/reservation/{room.id}">Rezerwuj</a>
            </td>
            <td style="text-align: center;">
                <a href="/room/modify/{room.id}">Modyfikuj</a>
            </td>
            <td style="text-align: center;">
                <a href="/room/delete/{room.id}">Usuń</a>
            </td>
        </tr>
        """

    return HttpResponse(
        start_template.format(room_list_table.format(table_rows))
    )


def reserve_room(request, id):
    try:
        room = Room.objects.get(id=id)
    except:
        return HttpResponse("Nie ma sali o tym numerze.")


    # może najpier zrobić rezerwowanie, z testami. A późneij testować blokadę.

    # Czy rezerwacja jest już zrobiona/zajęcia

    # Czy data jest z przeszłości

    # Jeśli błąd, to info o błędzie

    return redirect(reverse("view_all"))



def room_search(request):
    # Zrobić jak movies

    # Wyszukiwanie po: nazwa, minimalna pojemność, dzień, obecność rzutnika
    # metodą get
    # rezultat to lista wolnych sal. Jeśli nie ma, to napisz że brak wolnych w tym terminie i o podanych kryteriach

    return HttpResponse("Nothing yet.")

# ToDo: Na stronie głównej status danego dnia. Dzisiaj? Zajęte lub wolne.
# ToDo: Na stronie sali lista dni kiedy sala jest zajęta, bez dni które minęły.
# ToDo: Na stronie rezerwacji sali lista dni zajętych, bez minionych.

