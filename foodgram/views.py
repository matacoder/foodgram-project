from django.shortcuts import render


def server_error(request):
    return render(request, "misc/500.html", status=500)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def tech(request):
    return render(
        request,
        "misc/tech.html",
        {}
    )