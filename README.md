# Tkinter Desktop Information Tool

A desktop information utility built with **Python + Tkinter**, integrating weather queries, moon phase display, and a daily To-Do feature.  
It supports automatic refresh and exception fallback handling, with a focus on engineering completeness and practical usability.

---

## ✨ Features Overview

* 🌦 **Weather Information Display**  
  Retrieves weather data based on the Open-Meteo API and supports scheduled automatic refresh.

* 🌙 **Moon Phase Calculation & Display**  
  Calculates the current moon phase using a local algorithm, without relying on third-party services.

* 📝 **Daily To-Do**  
  Supports simple task recording with local data persistence.

* ⏱ **Automatic Refresh Mechanism**  
  Uses Tkinter’s `after()` method to implement scheduled updates, avoiding blocking the main UI thread.

* 🛡 **Exception Fallback Handling**  
  Captures API and network exceptions to ensure stable program operation.

---

## 🧠 Technical Highlights

* Tkinter GUI layout and widget state management  
* API requests and response data parsing  
* Multi-threading for handling time-consuming tasks, with safe UI updates on the main thread  
* `after()` scheduling mechanism  
* Local file-based data persistence design  
* Exception handling and degraded display logic  

---

## 🚀 Current Status

* ✅ Core functionality completed  
* ✅ Program runs stably  
* 🟡 UI color scheme and visual details are not yet optimized  

> The current version of this project focuses on functional completeness and engineering structure.  
> UI visual optimization will be gradually improved in future versions.

---

## 🔮 Future Plans (Not Current Focus)

* UI color scheme and layout refinement  
* Configuration extraction (themes / refresh frequency)  
* More comprehensive information summary display  

---

## Demo

<img width="800" height="450" alt="Screenshot 2025-12-31 154730" src="https://github.com/user-attachments/assets/0f196589-4415-419f-a94b-ffa71224bcfd" />

---

## 🚀 Quick Start / Usage

### Environment Requirements
- Python 3.13+
- Virtual environment recommended (optional):
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
---

## 📌 说明

这是一个个人练习与探索性质的桌面小项目，重点在于将 Python 基础、API 使用与 GUI 结合，逐步形成完整的小型应用，而非单一功能示例。
