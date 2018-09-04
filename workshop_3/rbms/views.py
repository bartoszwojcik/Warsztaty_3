from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rbms.models import Room, Booking
import datetime

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

today = datetime.date.today()


def check_room_bookings(room_object):
    room_bookings = Booking.objects.filter(
        room=room_object, date__gte=today
    ).order_by("date")

    html = ""
    if room_bookings:
        html += "<ul>"
        # Add reserved dates
        for booking in room_bookings:
            html += f"<li>{booking.date}</li>"
        html += "</ul>"
    else:
        html += "Brak rezerwacji."
    return html


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
        {check_room_bookings(room)}
        """

        return HttpResponse(start_template.format(room_display_html))
    except ObjectDoesNotExist:
        return HttpResponse("Nie ma sali o tym numerze.")


def view_all(request):
    room_data = Room.objects.all().order_by("name")

    table_rows = ""
    for room in room_data:

        check_booking = Booking.objects.filter(
            date=today, room=room
        )
        if check_booking:
            reservation_status = """
            <td style="text-align: center; background-color: #E6B0AA;">Zajęte
            </td>"""
        else:
            reservation_status = """
            <td style="text-align: center; background-color: #ABEBC6;">Wolne
            </td>"""

        table_rows += f"""
        <tr style="border: 1px solid black">
            <td>
                <a href="/room/{room.id}">{room.name}</a>
            </td>
            {reservation_status}
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


@csrf_exempt
def reserve_room(request, id):
    try:
        room_data = Room.objects.get(id=id)
    except:
        return HttpResponse("Nie ma sali o tym numerze.")

    projector_available = "Tak" if room_data.has_projector is True else "Nie"

    reservation_response = f"""
        <h2>Rezerwacja sali: {room_data.name}</h2>
        <p>Liczba miejsc: {room_data.seats}</p>
        <p>Projektor: {projector_available}</p>
        <form action="#" method="POST">
            <label>Zarezerwuj salę na dzień:<br>
            <input type="date" name="reservation_date" min="{today}">
            </label><br><br>
            <label>Komentarz (opcjonalny):<br>
            <input type="text" name="comment" style="height: 4em; width: 600px">
            </label> <br><br>
            <button name="submit">Rezerwuj</button>
        </form><br>
        <p>Zajęta w dniach:</p> 
        {check_room_bookings(room_data)}
        """

    if request.method == "GET":
        return HttpResponse(start_template.format(reservation_response))
    elif request.method == "POST":
        if request.POST.get("reservation_date") is None\
                or request.POST.get("reservation_date") == "":
                return HttpResponse("Nie wprowadzono poprawnych danych.")

        # Modify date format, then check
        year, month, day = map(
            int, request.POST.get("reservation_date").split("-")
        )
        if datetime.date(year, month, day) < today:
            return HttpResponse("Wprowadzono błędną datę.")

        # Check existing bookings
        check_bookings = Booking.objects.filter(
            date=datetime.date(year, month, day), room=room_data
        )
        if check_bookings:
            return HttpResponse(
                "To pomieszczenie jest już zarezerwowane w tym dniu."
            )

        # Create a room booking
        Booking.objects.create(
            date=request.POST.get("reservation_date"),
            comment=request.POST.get("comment"),
            room=room_data
        )

        return redirect(reverse("view_all"))


@csrf_exempt
def room_search(request):

    @csrf_exempt
    def room_search_form():
        search_html = f"""
            <h2>Wyszukiwarka wolnych sal</h2>
            <p>Poniżej wprowadź paramety wyszukiwania.</p>
            <br><br>
            <form method="GET" action="#">
                <label>Nazwa sali:
                    <input type="text" name="room_name">
                </label><br><br>
                <label>Minimalna liczba miejsc:
                    <input type="number" name="room_seats" min=1>
                </label><br><br>
                <label>Data:
                    <input type="date" name="search_date"
                     min={today} value={today}>
                </label><br><br>
                <label>Z projektorem?
                    <select name="has_projector">
                        <option value=True>Tak</option>
                        <option selected value=False>Nie</option>
                    </select>
                </label><br><br>
                <button type="submit" name="search" value=1>Szukaj</button>
            </form>
            """
        return search_html

    def search_results(s_room_name=None, s_room_seats=None,
                       s_search_date=today, s_has_projector=None):

        # Retrieve room data
        search_result_data = Room.objects.all()

        # Application of search filters one by one. Each step limits results.
        # 1. Name search
        if s_room_name:
            search_result_data = search_result_data.filter(
                name__icontains=s_room_name)

        # 3. Seat search
        if s_room_seats:
            search_result_data = search_result_data.filter(
                seats__gte=s_room_seats
            )

        # 4. Projector search
        if s_has_projector == "True":
            search_result_data = search_result_data.filter(
                has_projector=True
            )

        # 5. Date search. Allows history search.
        room_bookings = Booking.objects.filter(date=s_search_date)
        for booking in room_bookings:
            search_result_data = search_result_data.exclude(
                id=booking.room.id
            )

        # Build result list
        search_result_output = ""
        if not search_result_data:
            search_result_output = """
            Brak wolnych sal dla podanych kryteriów wyszukiwania.
            """
        else:
            search_result_output += "<p>Wolne sale w tym dniu:</p>"
            for element in search_result_data:
                search_result_output += f"""
                <li><a href="/room/reservation/{element.id}">
                {element.name}</a></li>
                """

        return search_result_output

    if request.method == "GET" and not request.GET.get("search"):
        return HttpResponse(
            start_template.format(room_search_form())
        )
    elif request.method == "GET" and int(request.GET.get("search")) == 1:
        return HttpResponse(
            start_template.format(room_search_form() + search_results(
                s_room_name=request.GET.get("room_name"),
                s_room_seats=request.GET.get("room_seats"),
                s_search_date=request.GET.get("search_date"),
                s_has_projector=request.GET.get("has_projector")
            ))
        )
