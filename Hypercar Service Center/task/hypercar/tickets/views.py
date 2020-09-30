from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

menu = [
    {
        "action": "Change oil",
        "link": "change_oil"
    },
    {
        "action": "Inflate tires",
        "link": "inflate_tires"
    },
    {
        "action": "Get diagnostic test",
        "link": "diagnostic"
    }
]

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class Menu(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'get_ticket/menu.html', context={'menu': menu})


cars_line = {
    "change_oil": [],
    "inflate_tires": [],
    "diagnostic": []
}
ticket_num = 0

class TicketView(View):
    def get(self, request, service, *args, **kwargs):
        count = 0
        time_for_oil = len(cars_line["change_oil"]) * 2
        time_for_tires = len(cars_line["inflate_tires"]) * 5
        time_for_diag = len(cars_line["diagnostic"]) * 30

        for key in cars_line:
            for _value in cars_line[key]:
                count += 1

        if service == "change_oil":
            wait = time_for_oil
            ticket = count + 1
            cars_line["change_oil"].append(ticket)
            return render(request, 'get_ticket/details.html', context={"wait": wait, "ticket": ticket})
        elif service == "inflate_tires":
            wait = time_for_oil + time_for_tires
            ticket = count + 1
            cars_line["inflate_tires"].append(ticket)
            return render(request, 'get_ticket/details.html', context={"wait": wait, "ticket": ticket})
        elif service == "diagnostic":
            wait = time_for_oil + time_for_tires + time_for_diag
            ticket = count + 1
            cars_line["diagnostic"].append(ticket)
            return render(request, 'get_ticket/details.html', context={"wait": wait, "ticket": ticket})


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        change_oil = len(cars_line["change_oil"])
        inflate_tires = len(cars_line["inflate_tires"])
        diagnostic = len(cars_line["diagnostic"])
        context = {"change_oil": change_oil, "inflate_tires": inflate_tires, "diagnostic": diagnostic}
        return render(request, 'get_ticket/operator_menu.html', context)

    def post(self, request, *args, **kwargs):
        global ticket_num
        if len(cars_line["change_oil"]) > 0:
            ticket_num = cars_line["change_oil"].pop(0)
        elif len(cars_line["inflate_tires"]) > 0:
            ticket_num = cars_line["inflate_tires"].pop(0)
        elif len(cars_line["diagnostic"]) > 0:
            ticket_num = cars_line["diagnostic"].pop(0)
        else:
            ticket_num = 0
        return redirect('/next')


class Next(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'get_ticket/next.html', context={"ticket": ticket_num})
