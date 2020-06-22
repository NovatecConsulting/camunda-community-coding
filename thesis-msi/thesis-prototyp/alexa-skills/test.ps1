"*******************"
"**Prozess starten**"
"*******************"
"LaunchRequest - starte meine bestellung"
$test = (ask simulate -t "starte meine bestellung" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1 --force-new-session)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"HelpIntent - hilfe"
$test = (ask simulate -t "hilfe" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"BestellungIntent - ich möchte schnitzel mit pommes und cola für zimmer zwei bestellen"
$test = (ask simulate -t "ich möchte schnitzel mit pommes und cola für zimmer zwei bestellen" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"BestellungIntentBestätigen - ja"
$test = (ask simulate -t "ja" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"CancelIntent - stopp"
$test = (ask simulate -t "stopp" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1)
$test | Select-String -Pattern "caption" -CaseSensitive
""
""
"****************************"
"**Interaktion mit Aufgaben**"
"****************************"
"LaunchRequest: starte aufgaben felix"
$test = (ask simulate -t "starte aufgaben felix" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b --force-new-session)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"HelpIntent - hilfe"
$test = (ask simulate -t "hilfe" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"DetailsIntent: was ist meine aufgabe (felix)"
$test = (ask simulate -t "was ist meine aufgabe" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"WagenVorbereitenIntent: ich habe den wagen vorbereitet (felix)"
$test = (ask simulate -t "ich habe den wagen vorbereitet" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"CancelIntent - stopp"
$test = (ask simulate -t "stopp" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"LaunchRequest: starte aufgaben julian"
$test = (ask simulate -t "starte aufgaben julian" -l de-DE -s amzn1.ask.skill.56384de5-319d-4da7-b8fd-079b3ffa2015 --force-new-session)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"DetailsIntent: was ist meine aufgabe (julian)"
$test = (ask simulate -t "was ist meine aufgabe" -l de-DE -s amzn1.ask.skill.56384de5-319d-4da7-b8fd-079b3ffa2015)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"AbschlussIntent: die bestellung ist zubereitet (julian)"
$test = (ask simulate -t "die bestellung ist zubereitet" -l de-DE -s amzn1.ask.skill.56384de5-319d-4da7-b8fd-079b3ffa2015)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"CancelIntent - stopp"
$test = (ask simulate -t "stopp" -l de-DE -s amzn1.ask.skill.56384de5-319d-4da7-b8fd-079b3ffa2015)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"LaunchRequest: starte aufgaben felix"
$test = (ask simulate -t "starte aufgaben felix" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b --force-new-session)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"DetailsIntent: was ist meine aufgabe (felix)"
$test = (ask simulate -t "was ist meine aufgabe" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"AbschlussIntent: fertig (felix)"
$test = (ask simulate -t "fertig" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"AbschlussIntent: ja (felix)"
$test = (ask simulate -t "ja" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"************"
"**Weiteres**"
"************"
"LaunchRequest - starte meine bestellung"
$test = (ask simulate -t "starte meine bestellung" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1 --force-new-session)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"BestellungIntent - ich möchte schnitzel mit pommes und cola für zimmer zwei bestellen"
$test = (ask simulate -t "ich möchte schnitzel mit pommes und cola für zimmer zwei bestellen" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"BestellungIntentBestätigen - ja"
$test = (ask simulate -t "ja" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"BestellungIntent - ich möchte maultaschen mit kartoffelsalat und cola für zimmer zwei bestellen"
$test = (ask simulate -t "ich möchte schnitzel mit pommes und cola für zimmer zwei bestellen" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"BestellungIntentBestätigen - ja"
$test = (ask simulate -t "ja" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"CancelIntent - stopp"
$test = (ask simulate -t "stopp" -l de-DE -s amzn1.ask.skill.765398d3-91e8-4fa4-85f1-06a928d9e5f1)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"LaunchRequest: starte aufgaben felix"
$test = (ask simulate -t "starte aufgaben felix" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b --force-new-session)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"DetailsIntent: was ist meine aufgabe (felix)"
$test = (ask simulate -t "was ist meine aufgabe" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"VorIntent: vor (felix)"
$test = (ask simulate -t "vor" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"ZurückIntent: vorherige (felix)"
$test = (ask simulate -t "vorherige" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"AufgabeUebergabeIntent: an anna abgeben (felix)"
$test = (ask simulate -t "an anna abgeben" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"AufgabeFreigebenIntent: freigeben (felix)"
$test = (ask simulate -t "freigeben" -l de-DE -s amzn1.ask.skill.e5787d19-28ed-4ae3-8ef0-c12dabe2ac4b)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"**************"
"**Kennzahlen**"
"**************"
"LaunchRequest: starte mein dashboard"
$test = (ask simulate -t "starte mein dashboard" -l de-DE -s amzn1.ask.skill.b6f14732-b1c1-4fa5-b55b-b3af3aa4efc7 --force-new-session)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"HilfeIntent: hilfe"
$test = (ask simulate -t "hilfe" -l de-DE -s amzn1.ask.skill.b6f14732-b1c1-4fa5-b55b-b3af3aa4efc7)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"UebersichtIntent: uebersicht"
$test = (ask simulate -t "uebersicht" -l de-DE -s amzn1.ask.skill.b6f14732-b1c1-4fa5-b55b-b3af3aa4efc7)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"OffeneTasksGruppeIntent: wie viele offene aufgaben hat service"
$test = (ask simulate -t "wie viele offene aufgaben hat service" -l de-DE -s amzn1.ask.skill.b6f14732-b1c1-4fa5-b55b-b3af3aa4efc7)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"AnzahlInstanzenHeuteIntent: wie oft wurde heute der zimmerservice gestartet"
$test = (ask simulate -t "wie oft wurde heute der zimmerservice gestartet" -l de-DE -s amzn1.ask.skill.b6f14732-b1c1-4fa5-b55b-b3af3aa4efc7)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"OffeneTasksProzessIntent: aufgaben bei zimmerservice"
$test = (ask simulate -t "aufgaben bei zimmerservice" -l de-DE -s amzn1.ask.skill.b6f14732-b1c1-4fa5-b55b-b3af3aa4efc7)
$test | Select-String -Pattern "caption" -CaseSensitive
""
"StoppIntent: stopp"
$test = (ask simulate -t "stopp" -l de-DE -s amzn1.ask.skill.b6f14732-b1c1-4fa5-b55b-b3af3aa4efc7)
$test | Select-String -Pattern "caption" -CaseSensitive
""