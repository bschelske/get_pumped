# 💪 get_pumped
Automated control of syringe pumps for microfluidic device workflows

> **get_pumped!** is a Python-based tool that communicates with syringe pumps via serial connections, enabling reproducible and programmable flow control for microfluidic experiments. It was developed as part of a graduate research project to automate machine learning data collection.

---

## 📘 Overview

Microfluidic devices require precise and programmable fluid flow, often achieved through a combination of syringe pumps and handheld pipeting. Manual pipeting solution into microfluidic devices is time-consuming, error-prone, and not easily reproducible.

**get_pumped** allows us to:
- Define flow profiles and sequences using Python scripts
- Communicate with pumps via serial ports (USB)
- Automate start/stop/timing/volume logic for multi-pump setups
- Integrate pump control into broader experimental workflows

This tool is especially useful for coordinating fluid control within microfluidic devices or for facilitating data collection (e.g. imaging).

---

## 🔧 Features

- 📡 **Serial communication** with supported syringe pump models
- 🔁 **Flow scripting**: Define flow rates, volumes, delays, and sequences
- 🧠 **Multi-pump coordination**: Synchronize multiple pumps for complex flows
- 🧪 **Looped protocols** for time-dependent delivery patterns
- 🖥️ **Responisve User Interface** Update parameters on the fly
- 🧩 Class methods for syringe pump control and in-house field generator
