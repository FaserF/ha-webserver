# Webserver App (for Home Assistant)

[![GitHub Release](https://img.shields.io/github/release/FaserF/ha-webserver.svg?style=flat-square)](https://github.com/FaserF/ha-webserver/releases)
[![Downloads (Current release)](https://img.shields.io/github/downloads/FaserF/ha-webserver/latest/webserver_app.zip?label=Downloads%20(Current%20release)&style=flat-square)](https://github.com/FaserF/ha-webserver/releases)
[![License](https://img.shields.io/github/license/FaserF/ha-webserver.svg?style=flat-square)](LICENSE)
[![hacs](https://img.shields.io/badge/HACS-custom-orange.svg?style=flat-square)](https://hacs.xyz)
[![Add to Home Assistant](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=webserver_app)
[![CI Orchestrator](https://github.com/FaserF/ha-webserver/actions/workflows/ci-orchestrator.yml/badge.svg)](https://github.com/FaserF/ha-webserver/actions/workflows/ci-orchestrator.yml)

A native, lightweight Home Assistant integration designed to monitor and manage Apache2 and Nginx webserver add-ons. Automatically track operational metrics, monitor SSL certificate expiration, parse error logs, and restart add-ons directly from your Home Assistant dashboard.

> [!IMPORTANT]
> **Repository Migration Notice**  
> This integration originally resided within the [FaserF/hassio-addons](https://github.com/FaserF/hassio-addons) repository. It has been migrated to this dedicated repository (`ha-webserver`) to facilitate cleaner release versioning, HACS updates via release zips, and independent development.

---

---

## ❤️ Support This Project

> I maintain this integration in my **free time alongside my regular job** — bug hunting, new features, and testing on real hardware. Test devices cost money, and every donation helps me stay independent and free up more time for open-source work.
>
> Donations are completely voluntary — but the more support I receive, the less I depend on other income sources and the more time I can realistically invest into these GitHub projects. 💪

<div align="center">

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor%20on-GitHub-%23EA4AAA?style=for-the-badge&logo=github-sponsors&logoColor=white)](https://github.com/sponsors/FaserF)&nbsp;&nbsp;
[![PayPal](https://img.shields.io/badge/Donate%20via-PayPal-%2300457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/FaserF)

</div>

---
## 🧭 Quick Links

| | | |
| :--- | :--- | :--- |
| [✨ Features](#-features) | [📦 Installation](#-installation) | [⚙️ Configuration](#️-configuration) |
| [🧱 Supported Add-ons](#-supported-add-ons) | [🧑‍💻 Development](#-development) | [📄 License](#-license) |

---

## ✨ Features

- **Automated Supervisor Discovery**:
  - Dynamically detects supported local add-ons via the Home Assistant Supervisor internal API.
  - Zero manual YAML configuration needed.
- **Comprehensive Telemetry Sensors**:
  - **Status**: Live operational tracker (`started`, `stopped`) with instant update notifications.
  - **Version**: Tracks currently installed add-on version vs. newly available releases.
  - **Performance Stats**: Real-time extraction of active network connections, server load, total accesses, and handled HTTP requests.
  - **Log Diagnostics**: Proactively scans and aggregates critical add-on logs for `ERROR` and `WARNING` patterns.
- **SSL Lifecycle Management**:
  - Automatically loads and analyzes active local certificates (e.g. via `/ssl/`).
  - Dedicated sensors expose absolute **SSL Expiration Date** alongside a countdown of **Remaining Valid Days**.
- **Control & Recovery**:
  - **Reload Button**: Native button entity allowing immediate restarts of add-on containers straight from the entity detail view.
- **Advanced Observability**:
  - Fully supports downloading JSON state maps directly inside Home Assistant via native **Diagnostics** integration.

---

## 🧱 Supported Add-ons

| Add-on Variant | Supported Internal Slugs |
| :--- | :--- |
| **[Apache2](https://github.com/FaserF/hassio-addons/tree/master/apache2)** | `apache2`, `apache2-edge` |
| **[Apache2 Minimal](https://github.com/FaserF/hassio-addons/tree/master/apache2-minimal)** | `apache2-minimal`, `apache2-minimal-edge` |
| **[Apache2 Minimal with MariaDB](https://github.com/FaserF/hassio-addons/tree/master/apache2-minimal-mariadb)** | `apache2-minimal-mariadb`, `apache2-minimal-mariadb-edge` |
| **[Nginx](https://github.com/FaserF/hassio-addons/tree/master/nginx)** | `nginx`, `nginx-edge` |

---

## 📦 Installation

### HACS (Recommended)

1. Open **HACS** inside Home Assistant.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Add `FaserF/ha-webserver` as an **Integration** repository.
4. Search for **Webserver App** and click **Download**.
5. Restart Home Assistant.

---

## ⚙️ Configuration

Click the button below to start configuring the integration instantly:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=webserver_app)

Alternatively, go to **Settings > Devices & Services**, click **Add Integration**, search for **Webserver App**, and select your add-on variant.

---

## 🧑‍💻 Development

### Setup Environment
This integration is developed using standard Home Assistant custom component testing tooling.

```bash
# Clone the repository
git clone https://github.com/FaserF/ha-webserver.git
cd ha-webserver
```

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.