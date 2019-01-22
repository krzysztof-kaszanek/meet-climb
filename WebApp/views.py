import datetime

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from WebApp.forms import UpdateWspinacz,\
    DodajWyjazd,\
    WyslijPotwierdzeniePrzelewu,\
    WyslijUbezpieczenie
from WebApp.models import Wspinacz,\
    Wyjazd,\
    UczestnikWyjazdu,\
    PosiadaSprzet, Wiadomosc,\
    Kurs,\
    Instruktor,\
    UczestnikKursu


def index(request):
    return render(request, 'base.html', {})


def profil(request):
    wspinacz = Wspinacz.objects.get(user=request.user)
    instance = get_object_or_404(Wspinacz, id=wspinacz.id)
    sprzet = PosiadaSprzet.objects.all().filter(wspinacz=wspinacz)
    if request.method == 'POST':
        form = UpdateWspinacz(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save(commit=False)
            form.user_id = request.user.id
            form.save()
            return redirect('/')
    else:
        form = UpdateWspinacz()
    return render(request, 'profil.html', {'form': form, 'wspinacz': wspinacz, 'sprzet': sprzet})


def wyjazdy(request, sortowanie):
    if sortowanie == 'data_malejaco':
        wyjazdy_all = Wyjazd.objects.filter(data_rozpoczecia__gte=datetime.date.today()).order_by('-data_rozpoczecia')
    elif sortowanie == 'data_rosnaco':
        wyjazdy_all = Wyjazd.objects.filter(data_rozpoczecia__gte=datetime.date.today()).order_by('data_rozpoczecia')
    else:
        wyjazdy_all = Wyjazd.objects.filter(data_rozpoczecia__gte=datetime.date.today())
    return render(request, 'wyjazdy.html', {'wyjazdy': wyjazdy_all})


def dodaj_wyjazd(request):
    form = DodajWyjazd(request.POST or None, request=request)
    if form.is_valid():
        form.save()
        return redirect('/wyjazdy/')
    return render(request, 'dodaj_wyjazd.html', {'form': form})


def szczegoly_wyjazdu(request, wyjazd_id):
    wyjazd = Wyjazd.objects.get(pk=wyjazd_id)
    uczestnicy = UczestnikWyjazdu.objects.filter(wyjazd_id=wyjazd.id, status_zgloszenia='zaakc')
    dostepny_sprzet = []
    for uczestnik in uczestnicy:
        print(uczestnik.wspinacz.id)
        wspinacz = Wspinacz.objects.get(pk=uczestnik.wspinacz.id)
        sprzet = PosiadaSprzet.objects.filter(wspinacz_id=wspinacz.id)
        for item in sprzet:
            dostepny_sprzet.append(item)
    return render(request, 'szczegoly_wyjazdu.html',
                  {'wyjazd': wyjazd, 'uczestnicy': uczestnicy, 'sprzet': dostepny_sprzet})


def wyloguj(request):
    logout(request)
    return redirect('index')


def zglos_na_wyjazd(request, wyjazd_id):
    wspinacz = Wspinacz.objects.get(user=request.user)
    UczestnikWyjazdu.objects.create(wspinacz=wspinacz,
                                    wyjazd_id=wyjazd_id,
                                    status_zgloszenia='oczek')
    return render(request, 'zgloszenie_wyslane.html', {})


def przegladaj_zgloszenia(request):
    wspinacz = Wspinacz.objects.get(user=request.user)
    zgloszenia = UczestnikWyjazdu.objects.all().filter(status_zgloszenia='oczek',
                                                       wyjazd__organizator=wspinacz)
    return render(request, 'zgloszenia.html', {'zgloszenia': zgloszenia})


def zaakceptuj_zgloszenie(request, zgloszenie_id):
    zgloszenie = UczestnikWyjazdu.objects.get(pk=zgloszenie_id)
    zgloszenie.status_zgloszenia = 'zaakc'
    zgloszenie.save()
    zalogowany_wspinacz = Wspinacz.objects.get(user=request.user)
    Wiadomosc.objects.create(nadawca=zalogowany_wspinacz,
                             odbiorca=zgloszenie.wspinacz,
                             tytul='Zgłoszenie zaakceptowane',
                             wiadomosc='Twoje zgłoszenie na wyjazd: "' + zgloszenie.wyjazd.tytul +
                             '" zostało zaakceptowane przez organizatora!')
    return redirect('przegladaj_zgloszenia')


def odrzuc_zgloszenie(request, zgloszenie_id):
    zgloszenie = UczestnikWyjazdu.objects.get(pk=zgloszenie_id)
    zgloszenie.status_zgloszenia = 'odrz'
    zgloszenie.save()
    zalogowany_wspinacz = Wspinacz.objects.get(user=request.user)
    Wiadomosc.objects.create(nadawca=zalogowany_wspinacz, odbiorca=zgloszenie.wspinacz,
                             tytul='Zgłoszenie odrzucone',
                             wiadomosc='Twoje zgłoszenie na wyjazd: "' + zgloszenie.wyjazd.tytul +
                             '" zostało odrzucone przez organizatora')
    return redirect('przegladaj_zgloszenia')


def zaakceptuj_zapis(request, zapis_id):
    zapis = UczestnikKursu.objects.get(pk=zapis_id)
    zapis.status_zgloszenia = 'odrz'
    zapis.save()
    zalogowany_wspinacz = Wspinacz.objects.get(user=request.user)
    Wiadomosc.objects.create(nadawca=zalogowany_wspinacz, odbiorca=zapis.wspinacz,
                             tytul='Zapisano na kurs',
                             wiadomosc='Twoje zgłoszenie na kurs: "' +
                             zapis.kurs.get_rodzaj_kursu_display() +
                             '" zostało zaakceptowane przez instruktora!')
    return redirect('przegladaj_zapisy_na_kursy')


def odrzuc_zapis(request, zapis_id):
    zapis = UczestnikKursu.objects.get(pk=zapis_id)
    zapis.status_zapisu = 'odrz'
    zapis.save()
    zalogowany_wspinacz = Wspinacz.objects.get(user=request.user)
    Wiadomosc.objects.create(nadawca=zalogowany_wspinacz, odbiorca=zapis.wspinacz,
                             tytul='Nie udało się zapisać na kurs',
                             wiadomosc='Niestety, nie udało się zapisać na wybrany kurs: "' +
                             zapis.kurs.get_rodzaj_kursu_display() + '". Skontaktuj się z instruktorem')
    return redirect('przegladaj_zapisy_na_kursy')


def przegladaj_wiadomosci(request):
    wspinacz = Wspinacz.objects.get(user=request.user)
    wiadomosci = Wiadomosc.objects.all().filter(odbiorca=wspinacz).order_by('-data_wyslania')
    return render(request, 'wiadomosci.html', {'wiadomosci': wiadomosci})


def czytaj_wiadomosc(request, wiadomosc_id):
    wiadomosc = Wiadomosc.objects.get(pk=wiadomosc_id)
    if not wiadomosc.przeczytana:
        wiadomosc.przeczytana = True
        wiadomosc.save()
    return render(request, 'wiadomosc.html', {'wiadomosc': wiadomosc})


def pobierz_potwierdzenie(request, zapis_id):
    zapis = UczestnikKursu.objects.get(pk=zapis_id)
    filename = zapis.potwierdzenie_wplaty.file.name.split('/')[-1]
    response = HttpResponse(zapis.potwierdzenie_wplaty.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def pobierz_ubezpieczenie(request, wspinacz_id):
    wspinacz = Wspinacz.objects.get(pk=wspinacz_id)
    filename = wspinacz.ubezpieczenie.file.name.split('/')[-1]
    response = HttpResponse(wspinacz.ubezpieczenie.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def kursy(request, sortowanie):
    if sortowanie == 'data_malejaco':
        kursy_all = Kurs.objects.filter(data_rozpoczecia__gte=datetime.date.today()).order_by('-data_rozpoczecia')
    elif sortowanie == 'data_rosnaco':
        kursy_all = Kurs.objects.filter(data_rozpoczecia__gte=datetime.date.today()).order_by('data_rozpoczecia')
    else:
        kursy_all = Kurs.objects.filter(data_rozpoczecia__gte=datetime.date.today())
    return render(request, 'kursy.html', {'kursy': kursy_all})


def szczegoly_kursu(request, kurs_id):
    kurs = Kurs.objects.get(pk=kurs_id)
    instruktor = kurs.instruktor
    cena_os = int(kurs.cena / kurs.limit_osob)
    return render(request, 'szczegoly_kursu.html', {'kurs': kurs, 'instruktor': instruktor, 'cena_os': cena_os})


def zapisz_na_kurs(request, kurs_id):
    wspinacz = Wspinacz.objects.get(user=request.user)
    kurs = Kurs.objects.get(pk=kurs_id)
    wyslij_email('Dane do przelewu', 'Nr konta: 12345678, kwota: ' + str(int(kurs.cena / kurs.limit_osob)) + 'zł',
                 wspinacz.user.email)

    if request.method == 'POST':
        form = WyslijPotwierdzeniePrzelewu(request.POST, request.FILES)
        if form.is_valid():
            uczestnik_kursu = form.save(commit=False)
            uczestnik_kursu.wspinacz = wspinacz
            uczestnik_kursu.kurs = kurs
            form.save()
            return redirect('/kursy/zapisz_ubezpieczenie/' + str(kurs_id))
    else:
        form = WyslijPotwierdzeniePrzelewu()
    return render(request, 'zapisz_potwierdzenie_przelewu.html', {'form': form})


def zapisz_ubezpieczenie(request, kurs_id):
    if request.method == 'POST':
        form = WyslijUbezpieczenie(request.POST, request.FILES)
        if form.is_valid():
            ubezpieczenie = request.FILES['ubezpieczenie']
            Wspinacz.objects.filter(user=request.user).update(ubezpieczenie=ubezpieczenie)
            wiadomosc = 'Operacja zakończona pomyślnie! Oczekuj na odpowiedź instruktora'
            return render(request, 'base.html', {'wiadomosc': wiadomosc})
    else:
        form = WyslijUbezpieczenie()
    return render(request, 'zapisz_ubezpieczenie.html', {'form': form})


def wyslij_email(temat, wiadomosc, odbiorca):
    send_mail(
        temat,
        wiadomosc,
        'krzysztof.kaszanek@gmail.com',
        [odbiorca],
        fail_silently=False,
    )


def przegladaj_zapisy_na_kursy(request):
    wspinacz = Wspinacz.objects.get(user=request.user)
    instruktor = Instruktor.objects.get(wspinacz_ptr=wspinacz)
    zapisy = UczestnikKursu.objects.all().filter(status_zapisu='oczek', kurs__instruktor=instruktor)
    return render(request, 'zapisy_na_kursy.html', {'zapisy': zapisy})
