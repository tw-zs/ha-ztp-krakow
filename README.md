# ZTP Kraków (Home Assistant)

🚧 **Wersja Deweloperska (Work In Progress)** 🚧
*Ta integracja jest we wczesnej fazie rozwoju. Została wygenerowana automatycznie i wymaga jeszcze testów. Może zawierać błędy lub nie działać zgodnie z oczekiwaniami.*

Integracja dla [Home Assistant](https://www.home-assistant.io/) pobierająca dane z krakowskiego systemu TTSS (MPK / ZTP Kraków). Pozwala na śledzenie tablicy odjazdów na żywo z wybranych przystanków tramwajowych i autobusowych.

## Funkcje
- 🚎 **Odjazdy na żywo**: Pobiera aktualny czas przyjazdu / odjazdu (w minutach).
- 🛣 **Wsparcie Config Flow**: Łatwe dodawanie przystanków z poziomu interfejsu (brak konieczności grzebania w `configuration.yaml`).
- 🔄 **Osobne źródła dla tramwajów i autobusów**: Obsługa zarówno TTSS MPK (autobusy) jak i ZTP (tramwaje).
- 📊 **Słownik w atrybutach**: Dzięki zwracanej liście możesz z łatwością formatować tablicę odjazdów w Markdown, flex-table-card lub innych customowych kartach Lovelace.

## Instalacja

### Przez HACS (Rekomendowane)

1. Otwórz **HACS** w swoim Home Assistant.
2. Wejdź w zakładkę **Integracje** (Integrations).
3. Kliknij trzy kropki w prawym górnym rogu i wybierz **Custom repositories** (Niestandardowe repozytoria).
4. Wklej URL tego repozytorium (np. `https://github.com/tw-zs/ha-ztp-krakow`).
5. Jako kategoria wybierz **Integration**.
6. Kliknij `ADD` (Dodaj).
7. Znajdź integrację "ZTP Kraków" na liście w HACS i ją pobierz.
8. Zrestartuj Home Assistanta.

## Konfiguracja

Z poziomu interfejsu:
1. Wejdź w Ustawienia -> Urządzenia i usługi -> **Integracje**
2. Kliknij **Dodaj integrację** (Add integration)
3. Wyszukaj **ZTP Kraków**
4. Wypełnij formularz:
   - **Nazwa**: Dowolna własna nazwa przystanku (np. "Teatr Bagatela")
   - **ID przystanku**: Numeryczny identyfikator. Można go znaleźć w URL klikając przystanek na stronie [Autobusów](http://ttss.mpk.krakow.pl/) lub [Tramwajów](http://www.ttss.krakow.pl/) (zwróć uwagę na parametr `?stop=ID` - np. `317`).
   - **Typ**: Wybierz, czy jest to przystanek autobusowy czy tramwajowy.

## Użycie w Dashboardzie (Karta Markdown)

W Home Assistant wszystkie kolejne odjazdy znajdują się w atrybucie `departures`. Możesz użyć standardowej karty Markdown z poniższym kodem, aby stworzyć tablicę:

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

## Podziękowania

Integracja inspirowana publicznymi API Krakowa oraz wspaniałą społecznością Home Assistant Polska.
