#  Datora Komponentu Cenu Salīdzinātājs

Darba autors: Kristers Balcers 241RDC013

##  Projekta mērķis

Šī Python skripta mērķis ir atvieglot datora komponentu cenu pārbaudi internetā, automātiski salīdzinot cenas divos populāros Latvijas interneta veikalos: 1a.lv un aio.lv.

Plānojot būvēt jaunu datoru, skripts ļauj izvairīties no ikdienas manuālas cenu pārbaudes — palaid kodu, un dažās sekundēs redzi, kurš  komponents šobrīd ir izdevīgākais!

---

##  Kā tas strādā

- Katram produktam (`Mātesplate`, `Procesors`, `Videokarte`, `RAM`, `Barošanas bloks`) ir definētas saites uz `1a.lv` un `aio.lv`.
- Skripts izmanto Selenium WebDriver, lai ielādētu šīs lapas.
- HTML saturs tiek nolasīts un pārmeklēts ar regulāro izteiksmi (regex), lai atrastu cenu formātā `123,45 €`.
- Iegūtās cenas tiek salīdzinātas.
- Konsolē tiek izvadīta tabula ar:
  - 1a.lv cenu
  - aio.lv cenu
  - Kurš veikals konkrētajam produktam ir lētāks

---

##  Prasības

- Python 3.7+
- Google Chrome pārlūks
- [ChromeDriver](https://chromedriver.chromium.org/downloads) atbilstošai pārlūka versijai
- Python bibliotēka: `selenium`

###  Instalācija

```bash
pip install selenium


------------------------

 Iespējamie uzlabojumi
CSV/Excel rezultātu eksports

Automātiskas e-pasta paziņojumu integrācija

Vairāku veikalu paplašināšana (RD Electronics, Dateks u.c.)
