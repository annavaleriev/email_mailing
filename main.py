from django.shortcuts import render

from services.models import SendMail, Client


def home_page(request):
    total_sendmail = SendMail.objects.count()
    total_sendmail_is_active = SendMail.objects.filter(is_active=True).count()
    total_clients = Client.objects.count()

    # all_articles = list(Blog.objects.all())
    # random_articles = random.sample(all_articles, 3)

    context = {
        "total_sendmail": total_sendmail,
        "total_sendmail_is_active": total_sendmail_is_active,
        "total_clients": total_clients,
        # "random_articles": random_articles,
    }

    return render(request, "includes/header.html", context)
