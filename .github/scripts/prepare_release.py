import os
import glob
import datetime

def get_env_var(filepath, key, default=""):
    """قراءة متغير معين من ملفات بيئة البناء المخزنة"""
    if not os.path.exists(filepath):
        return default
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(f"{key}="):
                return line.strip().split("=", 1)[1]
    return default

def main():
    # البحث عن ملفات بيئة البناء المستخرجة من الـ Matrix
    env_files = glob.glob("downloaded-artifacts/build-env-*.txt") or glob.glob("build-env-*.txt")
    latest_env = env_files[0] if env_files else ""

    # استخراج البيانات الديناميكية للبناء
    linux_ver = get_env_var(latest_env, "LINUX_VERSION", "6.1-LTS")
    susfs_ver = get_env_var(latest_env, "SUSFS_VERSION", "v1.5.5")
    compiler = get_env_var(latest_env, "COMPILER_STRING", "Clang/LLVM (Android GKI Toolchain)")
    run_num = os.environ.get("GITHUB_RUN_NUMBER", "1")
    commit_sha = os.environ.get("GITHUB_SHA", "unknown")[:7]
    build_date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    lto_type = os.environ.get("LTO_INPUT", "fullLTO")
    tag_name = f"v6.1-r{run_num}"
    release_name = f"⚡ GKID Kernel v6.1-r{run_num} | Tab S10 Ultra (Dimensity 9300+)"

    # قراءة البصمات (Checksums) لإدراجها تلقائياً
    checksums_content = ""
    for c_path in ["release-artifacts/checksums.txt", "checksums.txt"]:
        if os.path.exists(c_path):
            with open(c_path, "r", encoding="utf-8") as cf:
                checksums_content = cf.read().strip()
            break

    # بناء نص صفحة الإصدار بالبادجات المدمجة الأنيقة (flat-square)
    release_body = f"""# ⚡ GKID Kernel (Tab S10 Ultra Edition) — Build r{run_num}

<p align="center">
  <img src="https://raw.githubusercontent.com/ifoknr/GKID-Kernels/dev/docs/banner.png" alt="GKID Kernels Banner" width="100%">
</p>

<p align="center">
  <a href="#-device-specifications"><img src="https://img.shields.io/badge/Device-Tab%20S10%20Ultra-007ec6?style=flat-square&logo=samsung&logoColor=white" alt="Device"></a>
  <a href="#-device-specifications"><img src="https://img.shields.io/badge/GKI-Kernel%206.1-success?style=flat-square&logo=linux&logoColor=white" alt="GKI"></a>
  <a href="#-device-specifications"><img src="https://img.shields.io/badge/SoC-Dimensity%209300+-orange?style=flat-square&logo=mediatek&logoColor=white" alt="SoC"></a>
  <a href="#-performance--gaming"><img src="https://img.shields.io/badge/LTO-{lto_type}-red?style=flat-square&logo=llvm&logoColor=white" alt="LTO"></a>
  <a href="#-security--root-hiding"><img src="https://img.shields.io/badge/SuSFS-{susfs_ver}-7c3aed?style=flat-square&logo=gitlab&logoColor=white" alt="SuSFS"></a>
  <a href="https://t.me/FADELEES"><img src="https://img.shields.io/badge/Telegram-@FADELEES-2CA5E0?style=flat-square&logo=telegram&logoColor=white" alt="Telegram"></a>
</p>

**⚡ Automated CI/CD Release Build** tailored specifically for the **Samsung Galaxy Tab S10 Ultra (Dimensity 9300+)**. Integrated with KernelSU-Next, ReSukiSU, SuSFS {susfs_ver}, FullLTO compilation, and dedicated hardware schedulers.

---

## 📋 Build Metadata

| Property | Value |
| :--- | :--- |
| **Release Tag** | `{tag_name}` |
| **Commit** | `{commit_sha}` |
| **Build Date** | `{build_date}` |
| **Linux Kernel Base** | `Linux {linux_ver}` |
| **Toolchain** | `{compiler}` |
| **Pipeline Mode** | `{lto_type} Compilation` |

---

## 📱 Device Specifications

| Property | Details |
| :--- | :--- |
| **Target Device** | Samsung Galaxy Tab S10 Ultra (Wi-Fi & 5G variants) |
| **Kernel & OS** | Linux GKI 6.1 (Android 14) |
| **SoC** | MediaTek Dimensity 9300+ (4× Cortex-X4 + 4× Cortex-A720) |
| **Storage Subsystem** | UFS 4.0 (`none` direct I/O scheduler) |

---

## ⚡ Performance & Gaming

| Feature | Description |
| :--- | :--- |
| **Aggressive EAS Tuning** | Tuned `sugov_ext` rate limits (500µs ramp) for instant CPU frequency scaling during frame spikes. |
| **All-Big-Core Thread Affinity** | Prioritizes game render threads (`UnityMain`, `GameThread`) directly onto Cortex-X4 cores. |
| **Zero-Overhead UFS 4.0 I/O** | `none` scheduler completely bypasses I/O queue latency on ultra-fast UFS 4.0 storage. |
| **F2FS GC Suppression** | Silences aggressive garbage collection during screen-on time to eliminate micro-stutters. |
| **Optimized zRAM Overhead** | High-throughput LZ4 compression with 8 concurrent streams to prevent CPU decompression stalls. |
| **Stripped Debug Overhead** | Completely disabled `CONFIG_FTRACE`, `debugfs`, and tracing bloat for maximum raw game performance. |
| **FullLTO Pipeline** | Whole-program Link-Time Optimization compiled with Clang for optimal execution cache. |

---

## 🔋 Battery Life & Deep Sleep

| Feature | Description |
| :--- | :--- |
| **Wakelock Ceiling** | Enforced 500ms limit on runaway background services to curb idle drain. |
| **Freeze Timeout** | Reduced task freeze timeout (20s → 1s) for near-instant suspend entry. |
| **F2FS Sleep Tuning** | Postpones background filesystem maintenance to deep-sleep idle intervals. |
| **Suspend Engine** | Optimized platform-level suspend/resume routines to maintain zero overnight drops. |

---

## 🌐 Low-Latency Networking

| Feature | Description |
| :--- | :--- |
| **TCP BBRv3** | Google's congestion control engine backported for ultra-low latency and consistent ping. |
| **FQ-CoDel** | Fair Queuing with Controlled Delay as default packet discipline to combat bufferbloat. |
| **IPv4/IPv6 WireGuard** | WireGuard VPN protocol compiled directly in-kernel for line-rate secure tunneling. |
| **IP Set & Netfilter** | Granular hardware-accelerated packet filtering and firewall match rules. |

---

## 🛡️ Security & Root Hiding

| Feature | Description |
| :--- | :--- |
| **KernelSU-Next & ReSukiSU** | Kernel-space root engine supporting modern manager interfaces. |
| **SuSFS Integration** | Advanced filesystem mount insulation preventing detection by banking and integrity systems. |
| **AVC Log Spoofing** | Silently redirects root SELinux denials to standard `priv_app` domains in audit logs. |
| **Multi-Manager Support** | In-kernel verification supporting official KernelSU-Next, ReSukiSU, and WKSU APK signatures. |

---

## 📦 Verified Artifacts & Checksums

"""

    if checksums_content:
        release_body += f"""```text
{checksums_content}
```\n"""
    else:
        release_body += "*Checksums will be updated directly upon artifact generation.*\n"

    release_body += """
---

## 🛠️ Quick Installation Guide

> [!CAUTION]
> **Always backup your current boot image before flashing!**

1. **Kernel Flasher (Recommended):**
   - Open **Kernel Flasher**, grant Superuser permissions, and create a backup of your stock boot.
   - Go to **Flash**, select the downloaded `*.zip` archive, and confirm.
   - Reboot your tablet.
2. **Fastboot / Recovery (Alternative):**
   - Flash the injected `boot-*.img` directly:
     ```bash
     fastboot flash boot boot-*.img
     fastboot reboot
     ```

---

## 💬 Community & Support

- **Telegram:** [@FADELEES](https://t.me/FADELEES)
- **Issues & Tracking:** [GitHub Issues](https://github.com/ifoknr/GKID-Kernels/issues)
"""

    # كتابة نص الإصدار إلى الملف الذي يقرأه الأكشن
    with open("release_body.md", "w", encoding="utf-8") as f:
        f.write(release_body)

    # تصدير اسم الإصدار والـ Tag لـ GitHub Actions
    github_env = os.environ.get("GITHUB_ENV")
    if github_env and os.path.exists(github_env):
        with open(github_env, "a", encoding="utf-8") as env_file:
            env_file.write(f"RELEASE_NAME={release_name}\n")
            env_file.write(f"RELEASE={tag_name}\n")

    print(f"✅ Generated release_body.md successfully for {tag_name}")

if __name__ == "__main__":
    main()
