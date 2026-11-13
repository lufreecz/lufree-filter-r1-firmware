# lufree filter R1 – firmware

Firmware releases for the smart variant of the **lufree filter R1** (hoseless air filter for the Bambu Lab R1 laser, ESP32-C3).

## Updating

The filter checks for new versions by itself once a day. Open the filter's web app → **Settings → Firmware update**:

- **Check for updates** – asks for the newest version now
- **Install** – downloads, verifies and installs it; the filter restarts (about 1 minute)
- **Install untested versions (beta)** – also offers pre-releases

Every image is signed. The filter installs only images signed with the lufree release key – also when a `.bin` file is uploaded by hand.

## Files

- [Releases](../../releases) – signed images `lufree-filter-r1-X.Y.Z.bin` and `manifest.json`
- `channels/stable.json` – newest tested release
- `channels/beta.json` – newest release including betas

These files are maintained automatically; please do not edit them by hand.
