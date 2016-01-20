# BartaCrop

### Crop the slides of your favorite MFF teacher today

Skript splituje PDF soubory, které mají 4 slajdy na stránku, na pdf s jedním slajdem na stránce. 

Argumenty:

- **-m --margin** - například 18 nebo 13; 18 funguje na slajdy z AI a snad i na ostatní od Bartáka, 13 na slajdy ze statistického zpracování jazyků
- **-r --reverse** - mění virtuální origin pdf, místo vlevo dole tak vlevo nahoře, fungovalo na ty slajdy ze statistického zpracování jazyků
- **-fa --filename_append** - default je \_cropped
- **-o --order** - explicitně vypsané 1, 2, 3, 4 v pořadí, ve kterém má skript řadit stránky - 1 je levá horní část, 3 je levá dolní část 