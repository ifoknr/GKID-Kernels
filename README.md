# ⚡ GKID Kernel (Tab S10 Ultra Edition)

<p align="center">
  <img src="docs/banner.png" alt="GKID Kernels Banner">
</p>

[![Fork](https://img.shields.io/badge/Project-Downstream%20Fork-blueviolet?style=for-the-badge&logo=git&logoColor=white)](#-about-this-fork)
[![Device](https://img.shields.io/badge/Tested%20On-Galaxy%20Tab%20S10%20Ultra-007ec6?style=for-the-badge&logo=samsung&logoColor=white)](#-target-device--specifications)
[![GKI Version](https://img.shields.io/badge/GKI-Kernel%206.1%20%7C%20Android%2014-success?style=for-the-badge&logo=linux&logoColor=white)](#-target-device--specifications)
[![Processor](https://img.shields.io/badge/SoC-Dimensity%209300-orange?style=for-the-badge&logo=mediatek&logoColor=white)](#-target-device--specifications)
[![KernelSU](https://img.shields.io/badge/KernelSU-Official-10b981?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/tiann/KernelSU)
[![ReSukiSU](https://img.shields.io/badge/ReSukiSU-Supported-E91E63?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ReSukiSU/ReSukiSU)
[![SuSFS](https://img.shields.io/badge/SuSFS-gki--android14--6.1-7c3aed?style=for-the-badge&logo=gitlab&logoColor=white)](#-integrated-patches--versions)
[![Telegram](https://img.shields.io/badge/Telegram-@FADELEES-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/FADELEES)

**⚡ High-performance, low-latency downstream GKI kernel fork** tailored specifically for the **Samsung Galaxy Tab S10 Ultra (MediaTek Dimensity 9300)**. Packed with KernelSU (official) or ReSukiSU, SuSFS, BBRv3, FullLTO and device-specific config tuning.

---

## 📌 About This Fork

> [!NOTE]
> This repository is an independent **downstream fork** of the original [GKID-Kernels by ahmed-alnassif](https://github.com/ahmed-alnassif/GKID-Kernels). 
> - While upstream targets generic multi-version GKI devices, **this fork is specifically refactored, stripped of obsolete patches, and finely tuned for the MediaTek Dimensity 9300 All-Big-Core architecture and UFS 4.0 storage on the Galaxy Tab S10 Ultra.**
> - Full credit goes to **Ahmed Al-Nassif** and the upstream Android Common Kernel (ACK) contributors.

---

## ⚡ Quick Start

1. **Check** your kernel version in Settings → About Tablet / Phone
2. **Download** matching variant package from [Releases](https://github.com/ifoknr/GKID-Kernels/releases)
3. **Flash** using [Kernel Flasher](#-installation-guide-kernel-flasher) *(Always back up your stock boot image first!)*
4. **Manage** SuSFS with [ReSuSFS](https://github.com/ahmed-alnassif/ReSuSFS) or [BERNE - SUSFS](https://github.com/rrr333nnn333/BRENE)

---

## 📱 Target Device & Specifications

| Property | Details |
| :--- | :--- |
| **Tested Device** | Samsung Galaxy Tab S10 Ultra (Wi-Fi & 5G variants) |
| **Kernel & OS** | Linux GKI 6.1 (Android 14) |
| **SoC** | MediaTek Dimensity 9300 (4× Cortex-X4 + 4× Cortex-A720) |
| **GPU** | ARM Immortalis-G720 MC12 |
| **Storage Type** | UFS 4.0 (F2FS `/data` partition) |
| **Kernel Base** | Android Generic Kernel Image (GKI) |

---

## 🧩 Integrated Patches & Versions

| Kernel Patch | Version | Purpose & Integration Details |
| :--- | :--- | :--- |
| **KernelSU (Kernel Patch)** | `tiann/KernelSU` `main` | Official kernel-space su implementation (`KSU+SUSFS` builds). |
| **ReSukiSU (Kernel Patch)** | `ReSukiSU/ReSukiSU` `main` | KernelSU fork with multi-manager support (`RSKSU+SUSFS` builds). |
| **SuSFS (Kernel Patch)** | `gki-android14-6.1` branch tip | Kernel-level VFS hiding and mount isolation. The exact version is printed in each release's notes. |
| **TCP BBRv3** | `v3 (Upstream backport)` | Google's congestion control algorithm for minimal jitter and stable gaming ping. |

---

## 🔑 Root Management

| Manager / Tool | Version | Purpose & Direct Links |
| :--- | :--- | :--- |
| [**KernelSU Manager**](https://github.com/tiann/KernelSU/releases) | `Latest Release` | Official manager for `KSU+SUSFS` builds. Builds also accept the WKSU, 5ec1cff, rsuntk and KOWX712 manager signatures. |
| [**ReSukiSU Manager**](https://github.com/ReSukiSU/ReSukiSU/releases) | `Latest Release` | Enhanced manager supporting multi-manager setups and advanced root control. |
| [**ReSuSFS WebUI**](https://github.com/ahmed-alnassif/ReSuSFS/releases) | `Latest Release` | WebUI and module interface for configuring SuSFS hiding scripts and toggles. |
| [**BERNE - SUSFS**](https://github.com/rrr333nnn333/BRENE) | `Latest Release` | Dedicated companion script and profile manager for automated SuSFS setup. |

---

## ⚡ Performance & Battery

What this repository adds on top of the GKI 6.1 source:

| Feature | Description |
| :--- | :--- |
| **FullLTO Compilation** | Built with Full Link-Time Optimization via Clang/LLVM (ThinLTO / no LTO selectable in CI). |
| **I/O Schedulers** | `mq-deadline` built in, alongside the default `none` scheduler used on UFS. |
| **F2FS** | Built-in F2FS with xattr, POSIX ACL and compression support. |
| **MGLRU** | Multi-Gen LRU enabled by default for better memory reclaim under pressure. |
| **CPU Governors** | `schedutil` (default) plus `ondemand` available. |

> [!NOTE]
> Scheduler, wakelock, freezer and F2FS GC tunings come from the kernel source
> branch ([GKI-Duchamp-6.1](https://github.com/ahmed-alnassif/GKI-Duchamp-6.1)),
> not from this repository. Debug options (`FTRACE`, `debugfs`, `SLUB_DEBUG`) and
> `CONFIG_HZ` are deliberately left at their GKI values, because changing them
> breaks the KMI and stops vendor modules from loading.

---

## 🌐 Networking

| Feature | Description |
| :--- | :--- |
| **TCP BBRv3** | Default congestion control algorithm for low-latency network performance. |
| **FQ CoDel** | Default queueing discipline (fair queuing with controlled delay) to combat bufferbloat. |
| **IP Set & Netfilter** | Advanced firewall and packet filtering capabilities, including IPv6 NAT. |
| **WireGuard** | In-kernel VPN tunneling, as shipped by GKI 6.1. |

---

## 🛡️ Security & Root Hiding

| Feature | Description |
| :--- | :--- |
| **KernelSU & ReSukiSU** | Kernel-based root, one build per engine. |
| **SuSFS Integration** | Advanced filesystem and mount hiding against app-level integrity checks. |
| **SUS MAP/PATH/MOUNT** | Kernel-level isolation preventing path detection by banking and integrity apps. |

---

## 📥 Downloads & Artifacts

All releases are available on the [**GitHub Releases**](https://github.com/ifoknr/GKID-Kernels/releases) page:

* 📦 **`GKID-Kernel-*.zip`**: Flashable archive configured for direct app deployment (Recommended).
* 🖼️ **`boot-*.img`**: The kernel repacked into a *generic* AOSP GKI boot image (not Samsung's stock boot). For the Tab S10 Ultra, prefer the AnyKernel `.zip`.

---

## 🛠️ Installation Guide (Kernel Flasher)

> [!CAUTION]
> **MANDATORY BACKUP REQUIRED BEFORE FLASHING:**  
> Modifying your kernel involves risks. **You MUST back up your stock `boot` (and `init_boot` if present) partition before flashing.** If you encounter a bootloop, restoring your backup via Kernel Flasher or fastboot is your safe return path.

### Requirements & Compatibility:
* **Tested Device:** **Samsung Galaxy Tab S10 Ultra** on **Linux Kernel 6.1 (Android 14)**.
* **Other GKI 6.1 devices:** Should work on Android 14 devices running a 6.1 GKI kernel, but vendor modules depend on the KMI of your stock kernel. Always keep your stock boot backup ready.
* **Root Access:** Root privileges via KernelSU, ReSukiSU, or Magisk.
* **Flashing Tool:** **Kernel Flasher** app by *fatalcoder524*: [Download Kernel Flasher v1.6.0+](https://github.com/fatalcoder524/KernelFlasher/releases).

### Flashing Steps:

1. **Take a Backup First:**
   - Open **Kernel Flasher** and grant it Superuser (Root) permissions.
   - Navigate to the **Backup** tab.
   - Tap **Create Backup** to dump your stock boot image to your internal storage. Keep this safe!
2. **Flash the Kernel Zip:**
   - Download the latest **`GKID-Kernel-*.zip`** from [Releases](https://github.com/ifoknr/GKID-Kernels/releases).
   - In **Kernel Flasher**, go to the **Flash** section and select the downloaded `.zip` file.
   - Review the flashing log and ensure the script finishes with success (`Done!`).
3. **Reboot:**
   - Tap **Reboot** to restart your device.
   - Verify kernel installation in **Settings → About Tablet → Software Information → Kernel Version**.

---

## 💬 Community & Support

- **Telegram Support:** [@FADELEES](https://t.me/FADELEES)
- **Issue Tracker:** [GitHub Issues](https://github.com/ifoknr/GKID-Kernels/issues)
- **Original Upstream Project:** [ahmed-alnassif/GKID-Kernels](https://github.com/ahmed-alnassif/GKID-Kernels)

---

## 📄 License

Distributed under the GNU General Public License v2 (GPL-2.0). See [LICENSE](LICENSE) for more details.
