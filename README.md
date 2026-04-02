# ZTP Krak\u00f3w (Home Assistant)

\ud83d\udea7 **Wersja Deweloperska (Work In Progress)** \ud83d\udea7
*Ta integracja jest we wczesnej fazie rozwoju. Zosta\u0142a wygenerowana automatycznie i wymaga jeszcze test\u00f3w. Mo\u017ce zawiera\u0107 b\u0142\u0119dy lub nie dzia\u0142a\u0107 zgodnie z oczekiwaniami.*

Integracja dla [Home Assistant](https://www.home-assistant.io/) pobieraj\u0105ca dane z krakowskiego systemu TTSS (MPK / ZTP Krak\u00f3w). Pozwala na \u015bledzenie tablicy odjazd\u00f3w na \u017cywo z wybranych przystank\u00f3w tramwajowych i autobusowych.

## Funkcje
- \ud83d\ude8e **Odjazdy na \u017cywo**: Pobiera aktualny czas przyjazdu / odjazdu (w minutach).
- \ud83d\udee3 **Wsparcie Config Flow**: \u0141atwe dodawanie przystank\u00f3w z poziomu interfejsu (brak konieczno\u015bci grzebania w `configuration.yaml`).
- \ud83d\udd04 **Osobne \u017ar\u00f3d\u0142a dla tramwaj\u00f3w i autobus\u00f3w**: Obs\u0142uga zar\u00f3wno TTSS MPK (autobusy) jak i ZTP (tramwaje).
- \ud83d\udcca **S\u0142ownik w atrybutach**: Dzi\u0119ki zwracanej li\u015bcie mo\u017cesz z \u0142atwo\u015bci\u0105 formatowa\u0107 tablic\u0119 odjazd\u00f3w w Markdown, flex-table-card lub innych customowych kartach Lovelace.

## Instalacja

### Przez HACS (Rekomendowane)

1. Otw\u00f3rz **HACS** w swoim Home Assistant.
2. Wejd\u017a w zak\u0142adk\u0119 **Integracje** (Integrations).
3. Kliknij trzy kropki w prawym g\u00f3rnym rogu i wybierz **Custom repositories** (Niestandardowe repozytoria).
4. Wklej URL tego repozytorium (np. `https://github.com/tw-zs/ha-ztp-krakow`).
5. Jako kategoria wybierz **Integration**.
6. Kliknij `ADD` (Dodaj).
7. Znajd\u017a integracj\u0119 "ZTP Krak\u00f3w" na li\u015bcie w HACS i j\u0105 pobierz.
8. Zrestartuj Home Assistanta.

## Konfiguracja

Z poziomu interfejsu:
1. Wejd\u017a w Ustawienia -> Urz\u0105dzenia i us\u0142ugi -> **Integracje**
2. Kliknij **Dodaj integracj\u0119** (Add integration)
3. Wyszukaj **ZTP Krak\u00f3w**
4. Wype\u0142nij formularz:
   - **Nazwa**: Dowolna w\u0142asna nazwa przystanku (np. "Teatr Bagatela")
   - **ID przystanku**: Numeryczny identyfikator. Mo\u017cna go znale\u017a\u0107 w URL klikaj\u0105c przystanek na stronie [Autobus\u00f3w](http://ttss.mpk.krakow.pl/) lub [Tramwaj\u00f3w](http://www.ttss.krakow.pl/) (zwr\u00f3\u0107 uwag\u0119 na parametr `?stop=ID` - np. `317`).
   - **Typ**: Wybierz, czy jest to przystanek autobusowy czy tramwajowy.

## U\u017cycie w Dashboardzie (Karta Markdown)

W Home Assistant wszystkie kolejne odjazdy znajduj\u0105 si\u0119 w atrybucie `departures`. Mo\u017cesz u\u017cy\u0107 standardowej karty Markdown z poni\u017cszym kodem, aby stworzy\u0107 tablic\u0119:

```yaml
type: markdown
title: Odjazdy - Teatr Bagatela
content: >
  | Linia | Kierunek | Czas | Minuty | Status |
  | :---: | :--- | :---: | :---: | :---: |
  {% for departure in state_attr('sensor.przystanek_teatr_bagatela', 'departures') %}
    | **{{ departure.line }}** | {{ departure.direction }} | {{ departure.time }} | **{{ departure.minutes }}** | *{{ departure.status }}* |
  {% endfor %}
```

## Podzi\u0119kowania

Integracja inspirowana publicznymi API Krakowa oraz wspania\u0142\u0105 spo\u0142eczno\u015bci\u0105 Home Assistant Polska.
