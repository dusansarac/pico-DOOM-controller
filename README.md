# Raspberry Pi Pico DOOM HID Controller & UAC Telemetry Terminal

Custom hardverski kontroler za retro FPS igre (DOOM) zasnovan na Raspberry Pi Pico mikrokontroleru (CircuitPython), uparen sa desktop telemetrijskom aplikacijom pisanoj u Python / Tkinter okruženju.

## Sistem u radu

1. **RP2040 (CircuitPython Firmware)**:
   - Emulira USB HID miša i tastaturu bez potrebe za dodatnim drajverima.
   - Očitava tastere za kretanje (`W`/`S`), taster za paljbu (Left Click) i analogni potenciometar za rotaciju (X-osa miša).
   - Detektuje "combo" tastere za reset statistike u slučaju pogibije.
   - Šalje periodične CSV telemetrijske podatke putem USB Serial veze (`shots, elapsed_seconds, deaths`).

2. **UAC Telemetry GUI (Python / Tkinter)**:
   - Automatski skenira i detektuje COM port povezanog Pico uređaja.
   - Višenitno (`threading`) očitava serijski tok podataka radi fluidnog rada korisničkog interfejsa.
   - Prikazuje ispaljenu municiju, vreme preživljavanja i broj pogibija u autentičnom DOOM UAC stilu.

## Pinout Konekcije

| Komponenta | Pico Pin (GP) | Funkcija |
| :--- | :--- | :--- |
| **BTN_FORWARD** | GP26 | Kretanje napred (`W` taster) |
| **BTN_BACK** | GP22 | Kretanje nazad (`S` taster) |
| **BTN_FIRE** | GP27 | Pucanje (Lijevi klik miša) |
| **POTENTIOMETER** | GP28 (ADC) | Horizontalno ciljanje (X osa miša) |

## Pokretanje Desktop Aplikacije

```bash
pip install -r requirements.txt
python doom_gui.py