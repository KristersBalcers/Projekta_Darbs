from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
#regex_pattern: Regulārā izteiksme, kas nosaka, kā izskatās cena.

def iegut_cenu_ar_regex(url, regex_pattern, nosaukums):
    service = Service('./chromedriver')
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'€')]")))
    except:
        pass

# Iegūst visu HTML (lapas saturu kā tekstu).

    html = driver.page_source
    driver.quit()

    match = re.search(regex_pattern, html)
    if match:
        cena_raw = match.group(1).replace(',', '.').replace(' ', '')
        try:
            cena = float(cena_raw)
        except ValueError:
            raise Exception(f"Nepareizs cenas formāts lapā ({nosaukums}): '{cena_raw}'")

# Pārbauda vai cena nav 0.0 (bieži kļūda, nevis reāla cena)
        if cena == 0.0:
            raise Exception(f"Nederīga cena (0.0) lapā ({nosaukums})")

        return cena
    else:
        raise Exception(f"Cena nav atrasta lapā ({nosaukums})")

if __name__ == '__main__':
    start_time = time.time()

    # Uzlabots regex, kas uzticami atrod cenas ar € simbolu
    regex = r'>(\d{1,4}(?:[\s.,]\d{2})) *€<'

    produkti = [
        ("Mātesplate", 
         "https://www.1a.lv/p/matesplate-gigabyte-b650m-s2h/mkuk",
         "https://aio.lv/en/product--gigabyte-b650m-s2h--10620327"),

        ("Procesors", 
         "https://www.1a.lv/p/procesors-amd-ryzen-5-7600x-4-7ghz-am5-32mb/h336",
         "https://aio.lv/en/product--amd-100-000000593--5065742"),

        ("Videokarte", 
         "https://www.1a.lv/p/videokarte-gigabyte-geforce-rtx-4060-8-gb-gddr6/ob37",
         "https://aio.lv/en/product--gigabyte-gv-n4060eagleoc-ice-8gd--10825902"),

        ("Barošanas bloks", 
         "https://www.1a.lv/p/barosanas-bloks-corsair-rmx-series-rm850x-atx-850-w-13-5-cm-1-35-db/car0",
         "https://aio.lv/en/product--corsair-cp-9020270-eu--11082561"),

        ("RAM",
         "https://www.1a.lv/p/operativa-atmina-ram-team-group-t-force-delta-rgb-black-ddr5-32-gb-6000-mhz/gma7?cat=2vj&index=21",
         "https://aio.lv/en/product--team-group-ff3d532g5600hc36bdc0--5092340"),
    ]

    rezultati = []

    for nosaukums, url1a, urlaio in produkti:
        try:
            cena_1a = iegut_cenu_ar_regex(url1a, regex, "1a.lv " + nosaukums)
        except Exception as e:
            print(f"Kļūda ar 1a.lv {nosaukums}: {e}")
            cena_1a = "Nav atrasts"

        try:
            cena_aio = iegut_cenu_ar_regex(urlaio, regex, "aio.lv " + nosaukums)
        except Exception as e:
            print(f"Kļūda ar aio.lv {nosaukums}: {e}")
            cena_aio = "Nav atrasts"

# isinstance pārbauda, vai kāds objekts pieder pie noteikta datu tipa

        if isinstance(cena_1a, float) and isinstance(cena_aio, float):
            if cena_1a < cena_aio:
                labakais = "1a"
            elif cena_aio < cena_1a:
                labakais = "aio"
            else:
                labakais = "Vienādas cenas"
        elif isinstance(cena_1a, float):
            labakais = "1a"
        elif isinstance(cena_aio, float):
            labakais = "aio"
        else:
            labakais = "Nav cenas"

        rezultati.append((nosaukums, cena_1a, cena_aio, labakais))

    print(f"{'Produkts':<18} {'Cena 1a':<12} {'Cena aio':<12} {'Izdevīgākais variants'}")
    print("-" * 60)
    for r in rezultati:
        print(f"{r[0]:<18} {str(r[1]):<12} {str(r[2]):<12} {r[3]}")

    end_time = time.time()
    print(f"\nIzpildes laiks: {end_time - start_time:.2f} sekundes")

# A Regex is a sequence of characters that specifies a match pattern in text. -geegsforgeeks
