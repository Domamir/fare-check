# Sprawozdanie – Laboratorium 1
## Obliczanie wskaźnika NDVI na podstawie zobrazowań Sentinel-2 (Opole)

---

### 1. Wyszukanie zobrazowania w Copernicus Browser

Z użyciem platformy **Copernicus Browser** wyszukano zdjęcie satelitarne fragmentu mapy Polski – okolic miasta wojewódzkiego **Opole** (województwo opolskie). Ustawienia wyszukiwania:

- kolekcja danych: **Sentinel-2 L2A** (dane po korekcji atmosferycznej),
- maksymalne zachmurzenie: **30%**,
- data zobrazowania: **06.10.2026**.

![Copernicus Browser – wybór obszaru i parametrów](img/01_copernicus_browser.png)

---

### 2. Pobranie danych

W zakładce **Analytical** okna pobierania wybrano format **TIFF (32-bit float)**, rozdzielczość **10 m/px** oraz układ współrzędnych **WGS 84 (EPSG:4326)**. Pobrano:

- warstwy wizualizowane: **True color** oraz **NDVI** – jako materiał referencyjny do późniejszego sprawdzenia poprawności obliczeń,
- warstwy surowe (**RAW**): kanały **B04** i **B08**, potrzebne do samodzielnego wyliczenia NDVI.

![Okno pobierania danych – zakładka Analytical](img/02_pobieranie_danych.png)

---

### 3. Zdjęcie True Color

Kompozycja w barwach naturalnych (kanały B04, B03, B02). Widoczne są zabudowa Opola, rzeka Odra z kanałem, zbiorniki wodne, lasy oraz mozaika pól uprawnych.

![True Color](img/03_true_color.png)

---

### 4. Oryginalne NDVI z Copernicus Browser

Gotowa warstwa NDVI wygenerowana przez platformę Copernicus. Posłuży jako punkt odniesienia do porównania z warstwą obliczoną samodzielnie.

![Oryginalne NDVI](img/04_ndvi_oryginalne_qgis.png)

---

### 5. Wczytanie danych do QGIS

W programie **QGIS** wczytano pobrane pliki jako warstwy rastrowe, a ich nazwy zmieniono na czytelniejsze (`TrueColor`, `NDVI`, `B08`, `B04`). Panel warstw jest widoczny na zrzucie ekranu z punktu 4.

---

### 6. Warstwa NIR – kanał B08

Kanał **B08** Sentinel-2 to **bliska podczerwień (NIR)**, ok. 842 nm. Roślinność silnie odbija promieniowanie w tym zakresie, dlatego tereny zielone są jasne, a woda (która pochłania NIR) – niemal czarna.

![Kanał B08 – NIR](img/05_b08_nir.png)

---

### 7. Warstwa RED – kanał B04

Kanał **B04** Sentinel-2 to **światło czerwone (RED)**, ok. 665 nm. Chlorofil silnie pochłania światło czerwone, więc roślinność jest w tym kanale ciemna, a jaśniejsze są obszary odsłoniętej gleby i zabudowy (np. składowisko odpadów w północnej części kadru).

![Kanał B04 – RED](img/06_b04_red.png)

---

### 8. Obliczenie NDVI w Kalkulatorze rastra

Za pomocą narzędzia **Raster → Kalkulator rastra** obliczono znormalizowany różnicowy wskaźnik wegetacji (NDVI) z kanałów NIR i RED:

$$
NDVI = \frac{NIR - RED}{NIR + RED} = \frac{B08 - B04}{B08 + B04}
$$

Wyrażenie wpisane w kalkulatorze:

```
("B08@1" - "B04@1") / ("B08@1" + "B04@1")
```

Wartości NDVI mieszczą się w przedziale **od -1 do 1**:
- **< 0** – woda,
- **ok. 0 – 0,2** – gleba odsłonięta, zabudowa, drogi,
- **0,2 – 0,5** – roślinność rzadka lub słaba,
- **> 0,5** – gęsta, zdrowa roślinność (lasy, uprawy w pełni wegetacji).

---

### 9. Wynik – warstwa NDVI2

W wyniku obliczeń powstała nowa warstwa **NDVI2**, wyświetlona domyślnie w skali szarości. Jasne piksele oznaczają wysokie wartości NDVI (roślinność), ciemne – niskie (woda, zabudowa).

![Warstwa NDVI2 – skala szarości](img/07_ndvi2_skala_szarosci.png)

---

### 10. Nadanie stylu warstwie

W celu poprawy kontrastu i czytelności zmieniono styl warstwy NDVI2 na **pseudokolor jednopasmowy** z rampą kolorów od czerwieni do zieleni. Kolor czerwony oznacza wodę i obszary bez roślinności, pomarańczowy i jasnożółty – pola po zbiorach i zabudowę, a zielony – lasy, łąki i aktywne uprawy.

![NDVI2 po nadaniu stylu](img/08_ndvi2_styl.png)

---

### 11. Podsumowanie

W ramach laboratorium pozyskano zobrazowanie Sentinel-2 L2A okolic Opola z dnia 06.10.2026 i samodzielnie obliczono wskaźnik NDVI w programie QGIS. Proces obejmował:

1. wyszukanie zobrazowania w Copernicus Browser,
2. pobranie warstw referencyjnych (True Color, NDVI) oraz surowych kanałów B04 (RED) i B08 (NIR),
3. wczytanie danych do QGIS,
4. obliczenie NDVI w Kalkulatorze rastra ze wzoru (B08 − B04) / (B08 + B04),
5. nadanie wynikowej warstwie stylu kolorystycznego.

Otrzymana warstwa NDVI2 jest zgodna z oryginalnym NDVI z Copernicus Browser – w obu wyraźnie widać te same obszary: lasy i tereny zielone o wysokich wartościach, pola po zbiorach i zabudowę miejską o wartościach niskich oraz zbiorniki wodne i Odrę o wartościach ujemnych. Potwierdza to poprawność przeprowadzonych obliczeń. Wskaźnik NDVI pozwala w prosty sposób oceniać kondycję i zasięg roślinności, co ma zastosowanie m.in. w rolnictwie, leśnictwie i planowaniu przestrzennym.
