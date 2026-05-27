# 🌡️ HDIOS — Heat Diffusion with Interactive Object Simulation

A Python-based interactive simulation that visualizes **2D heat diffusion** across a conductive plate, with support for configurable insulating holes of different shapes and placements. Built using NumPy and Matplotlib with real-time animation.

---

## 📸 What It Does

The simulation models heat spreading across a 60×60 grid plate where:
- The **left edge** is maintained at **100°C** (heat source)
- The **right edge** is maintained at **20°C** (ambient temperature)
- The **top and bottom edges** use **Neumann (zero-flux) boundary conditions**

You can configure **4 subplots simultaneously**, each with different hole configurations (shapes + placements) to compare how insulating holes affect heat flow.

---

## ✨ Features

- 🔲 **Interactive CLI** — configure each subplot before the simulation starts
- 🔵 **3 hole shapes** — circle, square, triangle
- 📍 **5 placements** — center, up, down, left, right
- 📊 **4 simultaneous comparisons** — run different configurations side-by-side
- 🎨 **Jet colormap** with real-time animation
- ⚡ **Finite difference method** for heat diffusion (explicit scheme)

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install numpy matplotlib
```

### Run

```bash
python ipw_project.py
```

You'll be prompted to configure each of the 4 graphs interactively:

```
--- Configuration for Graph 1 ---
Enter number of holes (0, 1, or 2): 1
Enter shape (square/circle/triangle): circle
Enter placement (center/up/down/left/right): center
```

---

## 🧮 How It Works

Heat diffusion is modeled using the **2D explicit finite difference method**:

$$T_{i,j}^{n+1} = T_{i,j}^{n} + \alpha \left( T_{i+1,j} + T_{i-1,j} + T_{i,j+1} + T_{i,j-1} - 4T_{i,j}^{n} \right)$$

Where:
- `α = 0.24` — thermal diffusivity constant
- Each hole region is reset to ambient temperature (20°C) after every diffusion step, acting as a **cold insulating body**

---

## ⚙️ Configuration Options

| Parameter | Options |
|-----------|---------|
| Number of holes | `0`, `1`, `2` |
| Shape | `circle`, `square`, `triangle` |
| Placement | `center`, `up`, `down`, `left`, `right` |

---

## 📁 Project Structure

```
ipw_project.py   # Main simulation script (single file)
README.md
```

---

## 🛠️ Built With

- [NumPy](https://numpy.org/) — grid operations and diffusion math
- [Matplotlib](https://matplotlib.org/) — visualization and animation

---

## 📌 Notes

- The simulation runs for **1000 time steps**, with **3 diffusion sub-steps per frame**
- A shared colorbar (15°C – 105°C) is shown across all 4 subplots
- Hole boundaries are outlined in white dashed lines on the plots

---

## 👨‍💻 Author

Made as part of an engineering coursework project (IPW).
