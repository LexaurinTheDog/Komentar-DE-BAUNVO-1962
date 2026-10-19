# Quellen und Nachweise

Alle tatsächlichen Abrufe und Lektüren dieser Edition erfolgten am **19. Oktober 2026**. ISO-Zeitstempel, HTTP-Ergebnisse, Dateipfade und SHA-256 stehen im [Verifikationsprotokoll](sources/verification.json). Das [Dateiverzeichnis mit Hashes](sources/source-manifest.json) erfasst die gesicherten Quellen. Original-Intake und aktuelle Quelle bleiben getrennt erhalten.

## Verordnung und Fassung

- [Amtliches Portal](https://www.gesetze-im-internet.de/baunvo/) und [gesicherte Inhaltsseite](sources/index.html).
- [Amtliche Gesamtausgabe](https://www.gesetze-im-internet.de/baunvo/BJNR004290962.html) und [gesicherte HTML-Antwort](sources/baunvo.html).
- [Amtliches XML-ZIP](https://www.gesetze-im-internet.de/baunvo/xml.zip), [ZIP-Beleg](sources/baunvo.zip), [entpackte XML](sources/BJNR004290962.xml), [kanonische Lesefassung](sources/canonical.md).
- [Bundesgesetzblatt 2023 I Nr. 176](https://www.recht.bund.de/bgbl/1/2023/176/VO.html): [PDF-Antwort](sources/bgbl-2023-176.pdf) und [extrahierter Text](sources/bgbl-2023-176.txt). Artikel 2 enthält die letzte im konsolidierten Text ausgewiesene Änderung. Ausgabe vom 6. Juli 2023, Artikel 6 Absatz 1: Inkrafttreten am Folgetag, damit 7. Juli 2023. Die für einzelne BauGB-Änderungen vorgesehenen Sonderzeitpunkte betreffen Artikel 2 nicht.
- [Unveränderter Intake vom 1.10.2026](sources/intake-2026-10-01.md) und [paragraphenweiser Änderungsabgleich](sources/change-map.json). Alle 40 nummerierten Stellen stimmen materiell überein; bei § 25 ist die dort angehängte Erläuterung jetzt als Fußnote getrennt. Der ursprüngliche Textnachweis „Geltung ab 1.10.1977“ ist eine Quellenangabe zum Nachweiszeitraum und kein Beleg für das Inkrafttreten aller heutigen Regeln. Die allgemeine Quellenfußnote verweist außerdem auf § 26a.

Der Rechtsstand wurde anhand der am Stichtag angebotenen amtlichen HTML- und XML-Fassung und der dortigen letzten Änderungsangabe geprüft; deren Inkrafttreten wurde zusätzlich im Verkündungsblatt festgestellt. Das technische XML-Builddatum 6. Mai 2026 und das Abrufdatum werden nicht als Inkrafttretensbelege verwendet. Die ergänzende Suche nach späteren Änderungen ist im Suchprotokoll enthalten; eine vollständige Durchsicht sämtlicher Bundesgesetzblätter wird nicht behauptet.

## Ergänzende Vorschriften und Rechtsprechung

Die [gesicherte BauGB-Regelung zu Wasserstoff](sources/baugb-249a.html) belegt die in § 14 erläuterte Verweisung. [§ 31 BauGB](sources/baugb-31.html) und [§ 34 BauGB](sources/baugb-34.html) wurden als ergänzender Kontext gesichert; daraus wird keine Vollkommentierung oder Prüfung aller baugesetzlichen Sonderzulassungen abgeleitet. Die HTML-Antworten von Gesetze im Internet verwenden teilweise ISO-8859-1, die XML und eigenen Markdown-Dateien UTF-8.

Die [drei Fallkarten](cases/README.md) verlinken die amtlichen Entscheidungen, vollständige Rohantworten und Lesefassungen. Für 4 C 5.16 und 4 C 3.21 sind zusätzlich unveränderte lokale amtliche Korpustexte vorhanden. Deren ursprüngliche Herkunft und Abrufdaten stehen im jeweiligen Frontmatter. Direkte Abrufe bei bverwg.de lieferten 403; der erfolgreiche Firecrawl-Zugriff lieferte HTML mit Status 200 laut Anbieter-Metadaten. Diese beiden Zugriffsarten werden im Verifikationsprotokoll unterschieden.

Nicht amtliche Suchtreffer dienten allenfalls der Auffindung. Die Erläuterungen stützen sich auf die genannten Primärtexte. In den Gerichtsgründen zitierte weitere Entscheidungen und Literatur sind nicht automatisch als eigens verifizierte Quellen dieses Kommentars übernommen.

## Reproduktion und Grenzen

[_parse.py](_parse.py) erzeugt `units.jsonl`, `meta.json` und die kanonische Lesefassung. [_completeness.py](_completeness.py) ermittelt die erwarteten Kennungen unabhängig aus der amtlichen Inhaltsübersicht und prüft sie gegen sämtliche Paragraphenknoten und extrahierten Einheiten. [Vollständigkeitsbericht](completeness-report.json): 40 Paragraphen, drei leere Stellen, fünf Strukturüberschriften, keine Anlagen. Tabelle und Fußnote sind Teil des Erhaltungsnachweises. [_compare_intake.py](_compare_intake.py) reproduziert den Intake-Abgleich. [_quality.py](_quality.py) kontrolliert Kommentierungsabdeckung, Wiederholungen und eigene lokale Verweise.

Die technische Prüfung ersetzt keine unabhängige juristische Durchsicht. Die Auswahl der Rechtsprechung ist begrenzt. Historische Fassungen werden nicht vollständig ediert; konkrete Altplanfälle erfordern die zusätzliche Beschaffung des jeweils maßgebenden historischen Primärtexts. [Redaktioneller Prüfvermerk](REVIEW.md).
