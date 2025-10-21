###🌐 Analiza Wskaźników OECD - Interaktywny Dashboard
Aplikacja w Pythonie zbudowana przy użyciu frameworku Dash (Plotly), która dostarcza interaktywny pulpit nawigacyjny (Dashboard) do wizualnej analizy kluczowych wskaźników społeczno-ekonomicznych krajów OECD.

Ten panel pozwala na dynamiczną eksplorację danych i łatwe wykrywanie korelacji oraz trendów.

Kluczowe Funkcje ✨
Interaktywne Wykresy: Wykresy są dynamiczne (można powiększać, przybliżać, najeżdżać kursorem) dzięki bibliotece Plotly.

Filtrowanie i Suwaki: Użytkownik może filtrować kraje na podstawie zakresu PKB per capita za pomocą suwaka, co pozwala skupić się na bogatszych lub biedniejszych gospodarkach.

Analiza Korelacji: Wykresy korelacji pokazują zależności między np. Konsumpcją a Nierównościami dochodowymi, z możliwością zmiany zmiennej kolorującej (np. Stopa bezrobocia).

Porównanie Wieków Emerytalnych: Umożliwia porównanie wieku emerytalnego kobiet i mężczyzn w wybranych przez użytkownika krajach za pomocą rozwijanej listy.

Złożona Wizualizacja: Pierwszy wykres prezentuje zależność PKB per capita od Długości życia, używając dodatkowo rozmiaru punktów do kodowania liczby samobójstw, co ułatwia wielowymiarową analizę.

Dane 📊
Aplikacja wczytuje dane z pliku OECD.xlsx (musi znajdować się w katalogu głównym) i przetwarza kilkanaście wskaźników ekonomicznych i społecznych.
