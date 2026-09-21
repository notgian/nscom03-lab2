import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import os


C_THZ_NM = 299_792.458

# Create directory for generated plots
os.makedirs('rainbow_plots', exist_ok=True)


# Base color definitions
COLOR_DATA = {
    "Red": {"hex": "#FF0000", "range": (620, 750)},
    "Orange": {"hex": "#FF7F00", "range": (590, 620)},
    "Yellow": {"hex": "#FFFF00", "range": (570, 590)},
    "Green": {"hex": "#00FF00", "range": (495, 570)},
    "Blue": {"hex": "#0000FF", "range": (450, 495)},
    "Indigo": {"hex": "#4B0082", "range": (425, 450)},
    "Violet": {"hex": "#9400D3", "range": (380, 425)},
}

# Define rainbow colors with frequencies (THz), wavelengths (nm), and RGB hex
colors_info = []
for name, data in COLOR_DATA.items():
    avg_wavelength = sum(data["range"]) / 2
    
    colors_info.append({
        "name": name,
        "hex": data["hex"],
        "wavelength_nm": avg_wavelength,
        "freq_thz": round(C_THZ_NM / avg_wavelength, 2),  # Frequency in THz
    })

# 1. Generate Individual Color Plots with Annotated Waveform Parameters
for c in colors_info:
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=250)
    freq_thz = c["freq_thz"]
    amplitude = 1.0
    phase_shift = 0
    
    # thz -> 10^12 -> femto (1/THz in fs = 1000 / THz)
    T_fs = 1000.0 / freq_thz

    t_fs = np.linspace(0, T_fs, 1000)

    y = amplitude * np.sin(2 * np.pi * freq_thz * (t_fs / 1000.0) + phase_shift)

    color_code = c.get("hex")
    ax.plot(t_fs, y, color=color_code, linewidth=2, label=f'{c["name"]} Light Signal ({c["freq_thz"]} THz)')
    
    # --- AMPLITUDE ANNOTATION ---
    peak_idx = np.argmax(y)
    t_peak = t_fs[peak_idx]
    y_peak = y[peak_idx]

    ax.vlines(
        x=t_peak,
        ymin=0,
        ymax=y_peak,
        colors="black",
        linestyles="--",
        linewidth=1.2,
        alpha=0.8,
    )

    ax.plot(t_peak, y_peak, marker="o", markersize=5, color="black")

    # Add text next to the vertical line
    ax.text(
        x=t_peak + (T_fs * 0.03),  
        y=amplitude / 2,
        s="Peak Amplitude (A = 1.0)",
        fontsize=8,
        fontweight="bold",
        verticalalignment="center",
        bbox=dict(
            boxstyle="round,pad=0.3", fc="#FFFFE0", ec="gray", lw=0.5
        ),
    )
    
    # --- PERIOD ANNOTATION ---

    y_period = -1.2

    # Double-headed arrow spanning from t=0 to t=T_fs
    ax.annotate(
        "",
        xy=(0, y_period),
        xytext=(T_fs, y_period),
        arrowprops=dict(
            arrowstyle="<->",
            linewidth=1.5,
            color="black",
        ),
    )

    # Centered label text over the arrow line
    ax.text(
        x=T_fs / 2.0,
        y=y_period,
        s=f"Period = {T_fs:.2f} fs",
        fontsize=8,
        fontweight="bold",
        horizontalalignment="center",
        verticalalignment="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.8),
    )

    ax.set_title(f'Sinusoidal Waveform - {c["name"]} Light Signal\n(Frequency: {freq_thz} THz | Wavelength: {c["wavelength_nm"]} nm)', fontsize=10, fontweight='bold', pad=10)
    ax.set_xlabel('Time (fs)', fontsize=8.5)
    ax.set_ylabel('Amplitude (V)', fontsize=8.5)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlim(0, T_fs)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', fontsize=8)

    plt.tight_layout()
    plt.savefig(f'rainbow_plots/{c["name"].lower()}.png', dpi=300)
    plt.close(fig)

exit(0)

# 2. Generate Composite Signals Plots (Section 8)
t_fs = np.linspace(0, 5, 1000)

fig, axs = plt.subplots(3, 1, figsize=(7, 7.5), dpi=250)

# Frequencies in THz
f_red_thz = 437.65  # ~438 THz
f_blue_thz = 634.48 # ~634 THz

# Convert THz frequency for fs time array: (f_thz * t_fs) / 1000
y_red = 1.0 * np.sin(2 * np.pi * (f_red_thz / 1000.0) * t_fs + 0)
y_blue = 1.0 * np.sin(2 * np.pi * (f_blue_thz / 1000.0) * t_fs + np.pi/2)
y_comp1 = y_red + y_blue

axs[0].plot(t_fs, y_comp1, color='#8E44AD', linewidth=1.8, label=f'Composite: Red ({f_red_thz:.0f} THz) + Blue ({f_blue_thz:.0f} THz)')
axs[0].set_title('Composite Signal 1: Combination of 2 Waveforms (Red + Blue)', fontsize=9.5, fontweight='bold')
axs[0].set_xlabel('Time (fs)', fontsize=8)
axs[0].set_ylabel('Amplitude (V)', fontsize=8)
axs[0].set_xlim(0, 5)
axs[0].grid(True, linestyle=':', alpha=0.6)
axs[0].legend(loc='upper right', fontsize=8)

# Combination 2: Red + Green + Blue (RGB - 3 Signals)
f_green_thz = 562.99  # ~563 THz

y_green = 1.0 * np.sin(2 * np.pi * (f_green_thz / 1000.0) * t_fs + np.pi/3)
y_comp2 = y_red + y_green + y_blue

axs[1].plot(t_fs, y_comp2, color='#2C3E50', linewidth=1.8, label='Composite: Red + Green + Blue (RGB Primary Light)')
axs[1].set_title('Composite Signal 2: Combination of 3 Waveforms (Red + Green + Blue)', fontsize=9.5, fontweight='bold')
axs[1].set_xlabel('Time (fs)', fontsize=8)
axs[1].set_ylabel('Amplitude (V)', fontsize=8)
axs[1].set_xlim(0, 5)
axs[1].grid(True, linestyle=':', alpha=0.6)
axs[1].legend(loc='upper right', fontsize=8)

# Combination 3: All 7 Rainbow Colors Combined (Full Spectrum)
y_all = np.zeros_like(t_fs)
for c in colors_info:
    f_thz = c["freq_thz"]
    phi = c.get("phase", 0)  # Default to 0 if phase key isn't present
    y_all += np.sin(2 * np.pi * (f_thz / 1000.0) * t_fs + phi)

axs[2].plot(t_fs, y_all, color='#117A65', linewidth=1.5, label='Composite: All 7 ROYGBIV Spectral Signals')
axs[2].set_title('Composite Signal 3: Full ROYGBIV Spectrum Waveform Superposition', fontsize=9.5, fontweight='bold')
axs[2].set_xlabel('Time (fs)', fontsize=8.5)
axs[2].set_ylabel('Amplitude (V)', fontsize=8)
axs[2].set_xlim(0, 5)
axs[2].grid(True, linestyle=':', alpha=0.6)
axs[2].legend(loc='upper right', fontsize=8)

plt.tight_layout()
plt.show()
plt.savefig('rainbow_plots/composite_signals.png', dpi=300)
plt.close()

# 3. Generate Frequency-Domain Light Spectrum Plot (Section 9)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), dpi=300)

# Spectrum plot (Discrete Lines)
freqs = [c["freq_thz"] for c in colors_info]
amps = [c["amplitude"] for c in colors_info]
bar_colors = [c.get("hex") for c in colors_info]

for c in colors_info:
    ax1.text(c["freq_thz"], 1.08, f'{c["name"]}\n{c["freq_thz"]} THz', ha='center', va='bottom', fontsize=8, fontweight='bold', color=c.get("hex"))

ax1.set_title('Frequency-Domain Representation: Discrete Spectral Lines (ROYGBIV)', fontsize=10, fontweight='bold')
ax1.set_xlabel('Frequency (THz)', fontsize=8.5)
ax1.set_ylabel('Peak Amplitude (V)', fontsize=8.5)
ax1.set_xlim(380, 800)
ax1.set_ylim(0, 1.3)
ax1.grid(True, linestyle=':', alpha=0.6)

# Continuous Light Spectrum Band
wavelengths = np.linspace(380, 750, 500)
freq_domain = (3e8 / (wavelengths * 1e-9)) / 1e12 # THz

# Display color bar gradient
spectrum_img = np.zeros((50, 500, 3))
for i, wl in enumerate(wavelengths):
    # Map wavelength to approximate RGB for visual spectrum banner
    if 380 <= wl < 440:
        r, g, b = -(wl - 440) / (440 - 380), 0.0, 1.0
    elif 440 <= wl < 490:
        r, g, b = 0.0, (wl - 440) / (490 - 440), 1.0
    elif 490 <= wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / (510 - 490)
    elif 510 <= wl < 580:
        r, g, b = (wl - 510) / (580 - 510), 1.0, 0.0
    elif 580 <= wl < 645:
        r, g, b = 1.0, -(wl - 645) / (645 - 580), 0.0
    elif 645 <= wl <= 750:
        r, g, b = 1.0, 0.0, 0.0
    else:
        r, g, b = 0.0, 0.0, 0.0
    spectrum_img[:, i] = [r, g, b]

ax2.imshow(spectrum_img, extent=[380, 780, 0, 1], aspect='auto')
ax2.set_yticks([])
ax2.set_xlabel('Frequency (THz) / Visible Spectrum Band', fontsize=8.5)
ax2.set_title('Visible Light Spectrum Map in Frequency Domain', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('rainbow_plots/light_spectrum.png', dpi=300)
plt.close()
