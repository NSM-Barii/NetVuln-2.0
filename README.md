# NetVuln 2.0 🔥  
**The Next-Gen Recon & Vulnerability Analysis Engine**  
_📡 Successor to NetVuln 1.0 — now with full AI integration_

---

## 🧠 Overview

**NetVuln 2.0** is an advanced offensive security tool designed to automate reconnaissance and vulnerability analysis for bug bounty hunters, red teamers, and cybersecurity researchers.

Unlike its predecessor, NetVuln 2.0 offers **multi-layered scanning, API enrichment, and AI-powered insights** — all in a unified Python-based framework.

---

## 🚀 Features

### 🔍 Scanning Capabilities:
- ✅ **Port Scanning** via Python `socket` and `nmap`
- ✅ **Subdomain Enumeration**
- ✅ **Directory Brute-forcing** on all discovered subdomains
- ✅ **Nmap Vulnerability Scripting Engine (NSE)** integration

### 🧠 AI + Vulnerability Detection:
- 🤖 Uses **OpenAI's GPT-4** to analyze and summarize scan results
- 🔎 Prioritizes exploitable bugs like:
  - XSS
  - SQLi
  - IDOR
  - Path Traversal
  - Authentication/Access Control Bypass

### 🌐 External API Integration: 
NetVuln 2.0 queries external threat intelligence APIs to enrich its findings:

| API | Purpose |
|-----|---------|
| `ipinfo.io` | IP Geolocation & ASN Lookup |
| `Shodan` | Open Port & Device Fingerprinting |
| `NVD` / `vulners.com` | CVE + Exploit Enrichment |  ( COMING SOON )
| `cve.circl.lu` | Cross-source vulnerability feed | ( COMING SOON )
| `wpscan` | WordPress-specific enumeration |        ( COMING SOON )

---

## 🗂️ Data Handling

- All recon and scan data is **saved locally** in structured formats (TXT / JSON)  ( COMING SOON )
- Scan results are passed to **OpenAI for summarization and vuln suggestions**
- AI output is optionally formatted for terminal or Discord notifications       ( COMING SOON )

---

## 📦 Planned Additions
- 🛡️ AI-assisted proof-of-concept generation
- 🧰 CVE patch suggestions
- 🧪 Live testing modules (XSS payloads, IDOR iterators)
- 📊 Rich GUI or TUI reporting

---

## 📸 Screenshots & Demos  
Coming soon — full demo videos + walkthroughs will be available on [YouTube.com/@nsm_barii](https://youtube.com/@nsm_barii)

---

## 👨‍💻 Author

**Jabari "Bari" Lucien**  
Cybersecurity Developer | Network Automation Specialist  
GitHub: [@NSM-Barii](https://github.com/NSM-Barii)  
LinkedIn: [Jabari Lucien](https://www.linkedin.com/in/jabari-lucien)

---

## 🛑 Disclaimer

This tool is for **educational and authorized penetration testing purposes only**.  
Do **not** use it on networks you do not own or have permission to test.

---
