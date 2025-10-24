# SysWatch - Systemövervakningsapplikation

## Systemutveckling i Python – Individuell slutuppgift

**Studentinformation**  
Namn: Dennis  
Klass: DOE25  
Datum: 2025-10-19
GitHub-länk till projektet: https://github.com/DennisNilssonn/SysWatch

## 1. Inledning

I denna uppgift har jag utvecklat en övervakningsapplikation i Python som samlar in systeminformation och visar den i terminalen. Programmet kan starta övervakning, visa status, skapa och visa larm, samt hantera övervakningsläge.

Syftet är att visa hur man kan använda Python för systemutveckling inom DevOps, med fokus på struktur, funktioner och objektorientering.

## 2. Planering och design

Jag började med att läsa igenom kravspecifikationen och dela upp den i fem huvuddelar: starta övervakning, visa status, skapa larm, visa larm och starta övervakningsläge. Jag ritade sedan ett enkelt flöde över hur användaren navigerar i menyn och vilka funktioner som behövs.

Jag planerade att dela upp koden i separata moduler för bättre organisation - en för användargränssnitt, en för systemövervakning, en för alarmhantering och en för hjälpfunktioner. Detta gjorde koden mer läsbar och lättare att underhålla.

## 3. Programstruktur

Programmet är uppdelat i flera filer. Filen `main.py` innehåller huvudmenyn och startpunkten. Filen `monitor.py` ansvarar för att läsa systeminformation med hjälp av biblioteket psutil och hantera övervakningsläget. Filen `alarms.py` hanterar skapade larm och CRUD-operationer, medan `ui.py` och `utils.py` innehåller hjälpfunktioner för användargränssnittet. Filen `logger.py` hanterar all loggning av användaråtgärder och systemhändelser.

Filer kommunicerar med varandra genom imports och funktionsanrop. `main.py` importerar funktioner från de andra modulerna och koordinerar hela programflödet. Alla användaråtgärder och systemhändelser loggas automatiskt till separata loggfiler.

## 4. Viktiga funktioner eller klasser

**JsonFile-klassen i alarms.py** har metoder för att läsa och spara alarm till JSON-fil. Jag valde att använda en klass för att kunna återanvända samma kod både för att läsa och spara alarm, och för att hålla filhanteringen organiserad.

**monitor_system()-funktionen** använder threading för att köra övervakning i bakgrunden medan användaren kan trycka Enter för att gå tillbaka. Jag valde denna approach för att skapa en smidig användarupplevelse där övervakningen inte blockerar menyn.

**check_alarms()-funktionen** kontrollerar om några alarm ska gå av baserat på aktuell systemanvändning. Jag implementerade denna som en separat funktion för att hålla alarmlogiken åtskild från visningslogiken.

**SysWatchLogger-klassen i logger.py** hanterar all loggning av programmet. Den skapar en unik loggfil för varje programstart med tidsstämpel i filnamnet. Alla användaråtgärder, menyval, alarm-operationer och systemhändelser loggas automatiskt med omedelbar skrivning till disk för att säkerställa att inget går förlorat.

## 5. Bibliotek och verktyg

- **psutil** – för att läsa systemresurser (CPU, minne, disk)
- **os** – för filhantering och operativsystemsdata
- **json** – för att spara och läsa in larm
- **time** – för att skapa loopar i övervakningsläget
- **threading** – för att köra övervakning i bakgrunden
- **datetime** – för tidsstämplar på alarm och loggfilnamn
- **logger** – för att logga alla användaråtgärder och systemhändelser

Jag versionshanterade projektet med Git genom att skapa commits för varje större funktion och använda beskrivande commit-meddelanden. Alla filer är spårade förutom `alarms.json` som innehåller användardata och `logs/` mappen som innehåller loggfiler.

## 6. Testning och felsökning

Jag testade alla menyval manuellt genom att köra programmet i terminalen. För att undvika krascher använde jag try/except vid inmatning av siffror och JSON-hantering. Jag lade även till print()-utskrifter i början för att förstå flödet innan jag implementerade den slutgiltiga funktionaliteten.

En viktig bugg jag fick hantera var när JSON-filen blev korrupt - jag lade till felhantering som skapar en ny fil om den befintliga är trasig. Jag implementerade också ett robust loggningssystem som skriver direkt till disk för att säkerställa att alla användaråtgärder loggas korrekt.

## 7. Resultat

Jag är nöjd med hur programmet hanterar flera larm samtidigt och visar både aktiva och utlösta alarm tydligt. Övervakningsläget med progress bars fungerar smidigt och ger en bra överblick över systemets status.

Alarmhanteringen med CRUD-operationer fungerar som tänkt och användargränssnittet är intuitivt med tydliga menyer. Loggningssystemet fungerar perfekt och skapar en detaljerad historik över alla användaråtgärder och systemhändelser.

## 8. Reflektion och lärdomar

Jag har lärt mig mycket om hur moduler gör program mer strukturerade och lättare att underhålla. Jag har även förstått vikten av att planera innan man börjar koda och att använda Git ofta.

Threading var nytt för mig och jag lärde mig hur man kan använda det för att skapa bättre användarupplevelser. Jag förstod också vikten av felhantering, särskilt när man arbetar med filer och användarinmatning. Genom att implementera loggning lärde jag mig om filhantering, buffring och hur man skapar robusta system som inte förlorar data.

## 9. Möjliga förbättringar och vidareutveckling

Jag skulle vilja lägga till e-postnotifiering vid aktiverat larm och ett enkelt GUI med tkinter. Jag skulle också vilja skriva enhetstester för vissa funktioner och lägga till möjlighet att exportera övervakningsdata till CSV-format.

En annan förbättring skulle vara att lägga till fler systemmätningar som nätverksanvändning och temperatur. Jag skulle också vilja utveckla loggningssystemet med möjlighet att filtrera och söka i loggfiler, samt lägga till loggningsnivåer som DEBUG, INFO, WARNING och ERROR.

## 10. Sammanfattning

Projektet visar hur man kan använda Python för att skapa en enkel men effektiv övervakningsapplikation. Jag har tillämpat modulär programmering, filhantering, felhantering, loggning och versionshantering i praktiken. Programmet demonstrerar viktiga koncept inom systemutveckling och ger en bra grund för vidareutveckling.
