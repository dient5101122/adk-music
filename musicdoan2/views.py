from django.shortcuts import render
from django.db.models import Case, When
from django.contrib.auth.models import User
from musics.models import Song
from musics.models import Watchlater


def index(request):
    song = Song.objects.all()[0:3]

    if request.user.is_authenticated:
        wl = Watchlater.objects.filter(user=request.user)
        ids = []
        for i in wl:
            ids.append(i.video_id)

        preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(ids)])
        watch = Song.objects.filter(song_id__in=ids).order_by(preserved)
        watch = reversed(watch)

    else:
        watch = Song.objects.all()[0:3]

    return render(request, 'index.html', {'song': song, 'watch': watch})
