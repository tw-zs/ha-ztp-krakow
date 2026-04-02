# ZTP Kraków (Home Assistant)

🚧 **Wersja Deweloperska (Work In Progress)** 🚧
*Ta integracja jest we wczesnej fazie rozwoju. Została wygenerowana automatycznie i wymaga jeszcze testów. Może zawierać błędy lub nie działać zgodnie z oczekiwaniami.*

Integracja dla [Home Assistant](https://www.home-assistant.io/) pobierająca dane z krakowskiego systemu TTSS (MPK / ZTP Kraków). Pozwala na śledzenie tablicy odjazdów na żywo z wybranych przystanków tramwajowych i autobusowych.

## Funkcje
- 🚎 **Odjazdy na żywo**: Pobiera aktualny czas przyjazdu / odjazdu i wspiera wbudowaną w Home Assistant klasę `timestamp`.
- 🗺️ **Pojazdy na Mapie**: Możesz zdefiniować śledzenie konkretnej linii. Wszystkie jej autobusy lub tramwaje pojawią się jako obiekty na wbudowanej w Home Assistant Mapie, pokazując ich obecną pozycję, kierunek i trasę!
- 🛣 **Wsparcie Config Flow**: Łatwe dodawanie przystanków z poziomu interfejsu z inteligentną listą (brak konieczności grzebania w `configuration.yaml`).
- 🔄 **Kierunki i Linie**: Dodając przystanek możesz odfiltrować wyniki tylko do wybranej linii lub tylko do określonego kierunku jazdy.
- 📊 **Słownik w atrybutach**: Dzięki zwracanej liście wszystkich odjazdów z danego przystanku, możesz z łatwością formatować tablicę odjazdów we własnych kartach.

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

Z poziomu interfejsu (Ustawienia -> Urządzenia i usługi -> Dodaj integrację):

### Tryb: Przystanek (Tablica odjazdów)
Wybierz z listy zintegrowany przystanek. Połączy to się z API ZTP i wygeneruje listę. Opcjonalnie w kolejnym kroku możesz zawęzić wyniki do określonej **Linii**, a w jeszcze następnym - do interesującego Cię **Kierunku**!
Zalecane użycie: Dodaj do Dashboardu natywną kartę "Encje". Home Assistant automatycznie sformatuje czasy odjazdów jako "Za 5 minut".

### Tryb: Linia (Pojazdy na Mapie)
Wpisz numer linii (np. "192" lub "50"). Integracja utworzy dynamiczne urządzenia śledzące dla każdego aktywnego pojazdu tej trasy w Krakowie. Wejdź w widok "Mapa" z bocznego menu w Home Assistant, a zobaczysz przemieszczające się ikony.

## Użycie zaawansowane w Dashboardzie (Karta Markdown)

W Home Assistant wszystkie kolejne odjazdy z danego przystanku znajdują się również w atrybucie `departures`. Możesz użyć standardowej karty Markdown, aby stworzyć całą tablicę odjazdów (ala tablice przystankowe w Krakowie):

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
