Tenhle dokument reflektuje aktuální stav projektu a plán na jeho modernizaci.
Projekt AW sloužil v době mého studia jako praktická use case studie asynchronního zpracování a minimalizaci rizika race condition.
Pro praktické účely není projekt vhodně navržený a zaslouží změny i featury, které jej vylepší. Níže uvedu seznam bodů: co, proč a jak vylepšit.

## 1) Načítání kódu pomocí importlib:
Scrapery mají fungovat jako zásuvné modely, já jako uživatel si vytvořím scraper, nahraju ho a projekt ho dynamicky načte.
Nepovažuju takové načtení za bezpečné bez dalších akcí, jako např. sken kód pro podezřelé funkce (exec, eval, ...).
Řešení: každý scraper izolovat v Dockeru, zajistit mu minimální možné prostředí.

## 2) Refaktoring zachytávání výjimek a logování:
Aktuální strategie je trochu marná, zbytečně ukončuje celý thread pro jeden špatný výsledek, i když částečný report je zde lepší než žádný report.
Řešení: lepší sémantika Exceptions a robustnější rozhodovací logika, užitečnější logging.

## 3) threading vs. asyncio:
Projekt má dva cíle možné paralelizace: HTTP requesty a zpracování HTML dokumentu. Pro potřeby vhodné optimalizace je na místě zvážit přechod na asyncio,
pokud se parsing HTML neukáže jako bottleneck.

## 4) uchovávání výsledků z minulého scrapingu:
Fancy featura s nízkou prioritou, tj. poskytnout v mail reportu informaci o nabídce, která je nová, a výsledky, které zmizely.
SQLite se na to zdá vhodná, výsledků budou stovky nebo tisíce. Naopak třeba Redis se mi nezdá jako dobré řešení, protože AW nepoběží jako nekonečný proces.

## 5) Nahrazení scheduleru cronem a odstranění balastu
Čistá ergonomie údržby, custom scheduler byl skvělý studijně, ale vytváří zbytečnou plochu pro nové bugy. Považuju za rozumné se ho zbavit.
Stejným způsobem naložit se smyčkou čekající na příkazy a editory napsanými v Tkinteru.
S tím souvisí zamyšlení nad způsobem, jakým projektu předávat konfiguraci a queries ke zpracování.

## 6) Webové rozhraní
Mít malý webový server, který umožňuje spuštění on demand, editaci queries a konfigurace, a navíc ho nasadit ven (s robustním systémem autorizace a zabezpečení), je finální plán a konečný stav projektu.
Cokoliv dalšího přibude před bod 6 a mělo by být dokončeno, než dojde k budování serveru, protože jeho podoba závisí na tom, jaké rozhraní si projekt vyžádá.
