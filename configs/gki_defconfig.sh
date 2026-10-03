#!/usr/bin/env bash

# Define target defconfig location
DEFCONFIG="arch/arm64/configs/gki_defconfig"

function apply_config(){
  cat "$1" >> "$2"
}

if [ "$KSU" != "no" ] && [ "$KSU" != "vnlto" ]; then
  # Base KSU Config & Dependencies
  echo "⚙️ Added KSU configuration"
  echo "CONFIG_KSU=y" >> "$DEFCONFIG"
fi

# KPM is a SukiSU-Ultra feature; other KSU forks ignore it
if [ "$KSU" = "SKSU" ]; then
  echo "CONFIG_KPM=y" >> "$DEFCONFIG"
fi

echo "🧩 Adding Built-in Features"
apply_config "$WORKDIR/configs/features.config" "$DEFCONFIG"

if [ "$NM" = "true" ]; then
  echo "📁 NoMount enabled"
  echo "CONFIG_NOMOUNT=y" >> "$DEFCONFIG"
fi

if [ "$KSU_SUSFS" = "true" ]; then
  echo "🔧 Mode: SuSFS Hook Enabled"
  apply_config "$WORKDIR/configs/susfs.config" "$DEFCONFIG"
fi

if ! { kernel_version_eq "$KERNEL_VERSION" "5.10" || kernel_version_eq "$KERNEL_VERSION" "6.12"; }; then
  echo "⚙️ Adding Compatibility GKI Networking and Filesystem configs"
  apply_config "$WORKDIR/configs/compat.config" "$DEFCONFIG"
fi

if kernel_version_eq "$KERNEL_VERSION" "6.1" && [ "${CUSTOM_CONFIG:-true}" = "true" ]; then
  echo "📱 Adding Tab S10 Ultra custom configs"
  apply_config "$WORKDIR/configs/custom.config" "$DEFCONFIG"
fi

if [ "$C_LTO" != "true" ]; then
  if [ "$KSU_COMPAT" = "true" ] || [ "$KSU" = "vnlto" ]; then
    LTO="noneLTO"
  fi
fi

case "$LTO" in
  thinLTO)
    echo "🔥 ThinLTO optimizations enabled"
    cat >> "$DEFCONFIG" <<EOF
CONFIG_LTO_NONE=n
CONFIG_LTO_CLANG_THIN=y
EOF
    ;;
  fullLTO)
    echo "🔥 Full LTO optimizations enabled"
    cat >> "$DEFCONFIG" <<EOF
CONFIG_LTO_NONE=n
CONFIG_LTO_CLANG_FULL=y
EOF
    ;;
  *)
    echo "ℹ️ LTO disabled or not specified"
    ;;
esac

if [ "$No_DS" = "true" ]; then
  export DROIDSPACES="false"
  export NH="false"
fi

if [ "$DROIDSPACES" = "true" ]; then
  echo "🐳 DroidSpaces support enabled"
  apply_config "$WORKDIR/configs/droidspaces.config" "$DEFCONFIG"
fi

if [ "$NH" = "true" ]; then
  echo "🐉 NetHunter support enabled"
  apply_config "$WORKDIR/configs/nethunter.config" "$DEFCONFIG"
fi

if [ "$KSU_COMPAT" != "true" ]; then
  echo "🔧 Disable useless debugging configs for performance and resources"
  cat >> "$DEFCONFIG" <<EOF
# Disable useless debugging configs for performance and resources
CONFIG_RCU_TRACE=n
EOF
fi
