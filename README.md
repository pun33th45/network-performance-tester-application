# 🚀 iPerf GUI Performance Tool

A **desktop-based graphical extension** of the **iPerf Web Performance Tool**, developed as part of my **Network Engineering Internship**.  
This application provides a **real-time GUI wrapper over iPerf3** to perform practical TCP/UDP network performance testing with live visualization.

---

## 📌 Project Overview

The iPerf GUI Performance Tool abstracts complex CLI-based network testing into a **simple, interactive desktop interface**.  
It enables engineers to configure tests, execute real backend commands, and analyze performance metrics visually.

> ⚠️ This is **not a demo or simulated project**.  
> All metrics are generated from **actual iPerf3 backend execution**.

---

## 🧑‍💻 Internship Context

- **Domain:** Network Engineering  
- **Base Tool:** iPerf3  
- **Project Type:** Internship / Industry-oriented project  
- **Purpose:** Practical network performance analysis using a GUI-based approach  

---

## 🖥️ Application UI Dashboard

![Application UI Dashboard](./screenshots/Application%20UI%20dashboard.png)

*Central dashboard providing real-time visibility into network performance, including throughput trends, key metrics, and live backend system output.*

---

## ⚙️ Parameter Dashboard

![Parameter Dashboard](./screenshots/Parameter%20dashboard.png)

*Configuration panel allowing users to define test parameters such as target server IP, protocol selection (TCP/UDP), test duration, parallel streams, and ping execution.*

---

## 🔁 TCP Testing

![TCP Testing](./screenshots/TCP%20testing.png)

*TCP throughput testing with real-time bandwidth visualization, enabling accurate analysis of stable and high-throughput network links.*

---

## 📡 UDP Testing

![UDP Testing](./screenshots/UDP%20testing.png)

*UDP performance testing showcasing throughput variation, jitter, and packet loss, supporting reliability analysis for wireless and latency-sensitive networks.*

---

## ⚙️ How It Works

GUI Application
↓
Test Parameter Configuration
↓
iPerf3 Backend Execution
↓
Output Parsing
↓
Graphs, Metrics & System Logs


---

## 🧩 Key Features

- TCP and UDP network performance testing  
- Real-time throughput visualization  
- Jitter and packet loss measurement (UDP)  
- Ping-based latency testing  
- Parallel stream configuration  
- Live backend system output display  
- Export test results to CSV  
- Clean, professional dark-themed UI  

---

## 📦 Repository Structure

iperf-gui/
├── src/
├── assets/
├── extra_bin/ # iPerf binaries (tracked using Git LFS)
├── screenshots/
│ ├── Application UI dashboard.png
│ ├── Parameter dashboard.png
│ ├── TCP testing.png
│ └── UDP testing.png
├── README.md
├── .gitattributes
├── .gitignore


> ⚠️ This repository uses **Git LFS** for large binaries.  
> Run `git lfs install` before cloning the repository.

---

## 🎯 Learning Outcomes

- Practical understanding of network performance testing  
- GUI abstraction over CLI-based engineering tools  
- Backend command execution and output parsing  
- Real-time data visualization for network metrics  
- Industry-standard project structuring and documentation  

---

## 📌 Acknowledgment

This project was developed as part of my **Network Engineering Internship**, with a focus on building **practical, production-relevant tools** for real-world network performance analysis.

---
