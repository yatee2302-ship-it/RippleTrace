# 🌐 RippleTrace

### Agentic Multi-Tier Supply Chain Risk Intelligence

> **SAP Hackfest 2026 — Grand Finale | Chandigarh University**

RippleTrace is an **agentic supply-chain risk intelligence platform** designed to identify, trace, and analyze the propagation of disruptions across multi-tier supply networks.

The platform combines **AI agents, supply-chain intelligence, scenario analysis, and SAP technologies** to help organizations understand how a disruption at one point in the supply chain can impact downstream suppliers, logistics, inventory, and operations.

---

## 🏆 SAP Hackfest 2026

RippleTrace was developed as a **team project for SAP Hackfest 2026** and presented at the **Grand Finale at Chandigarh University, Chandigarh**.

The project focuses on moving from reactive supply-chain monitoring toward **proactive disruption intelligence and scenario-based decision making**.

---

## 🎯 Problem

Modern supply chains are highly interconnected. A disruption affecting one supplier, logistics route, or geographic region can propagate across multiple tiers and create cascading operational risks.

Traditional monitoring approaches may identify individual disruptions but can struggle to answer:

* Which downstream suppliers will be affected?
* How will the disruption propagate across multiple tiers?
* What inventory or logistics dependencies are exposed?
* Which risks require immediate attention?
* What could happen under different disruption scenarios?

---

## 💡 Our Solution

**RippleTrace** creates an intelligent view of supply-chain dependencies and uses agentic workflows to analyze disruption scenarios.

### Core capabilities

* 🔗 **Multi-Tier Risk Mapping**

  * Maps relationships across Tier 1, Tier 2, and Tier 3 suppliers.
  * Identifies dependencies and potential propagation paths.

* 🌊 **Disruption Contagion Analysis**

  * Tracks how a disruption can move through interconnected supply-chain nodes.
  * Helps visualize cascading effects.

* 🤖 **Agentic Intelligence**

  * Uses specialized agents for sensing, scenario analysis, logistics, inventory, and safeguards.
  * Agents work together to analyze disruption situations.

* 📦 **Logistics & Inventory Intelligence**

  * Evaluates potential effects on logistics and inventory.
  * Helps identify operational exposure.

* 🧪 **Scenario Analysis**

  * Allows users to provide disruption information and analyze possible consequences.
  * Supports what-if decision making.

* 👤 **Human-in-the-Loop Safeguards**

  * Keeps critical decisions under human oversight.
  * Provides decision-support rather than fully autonomous business decisions.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │   Disruption Input   │
                    │  User / Scenario     │
                    └──────────┬───────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │ Sensing & Scenario Agent │
                 └────────────┬─────────────┘
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
      ┌─────────────┐ ┌──────────────┐ ┌───────────────┐
      │ Contagion   │ │ Logistics &  │ │ Compliance &  │
      │ Mapper      │ │ Inventory    │ │ Human-in-Loop │
      │             │ │ Agent        │ │ Safeguards    │
      └──────┬──────┘ └──────┬───────┘ └───────┬───────┘
             │               │                 │
             └───────────────┼─────────────────┘
                             ▼
                 ┌─────────────────────────┐
                 │ Supply Chain Risk View  │
                 │ & Scenario Insights     │
                 └─────────────────────────┘
```

---

## 🤖 Agentic Workflow

### 1. Sensing & Scenario Agent

Receives disruption information and establishes the scenario that needs to be analyzed.

### 2. Contagion Mapper

Analyzes the supply-chain dependency graph and identifies how disruption can propagate across multiple tiers.

### 3. Logistics & Inventory Agent

Evaluates potential operational consequences involving logistics routes, inventory, and supply availability.

### 4. Compliance & Human-in-the-Loop Safeguards

Adds governance and human oversight to ensure that critical recommendations remain reviewable before action.

---

## 🌍 Example Scenario

RippleTrace can analyze scenarios involving events such as:

* 🌊 Geopolitical disruptions
* 🚢 Shipping-route disruptions
* 📡 GPS spoofing
* 🌐 Regional supply interruptions
* 🏭 Supplier-level failures

For example:

```text
Disruption
    ↓
Tier 1 Supplier
    ↓
Tier 2 Supplier
    ↓
Tier 3 Supplier
    ↓
Logistics / Inventory Impact
    ↓
Business Risk
```

The objective is to make the **ripple effect of a disruption visible before it becomes a larger operational problem**.

---

## ☁️ SAP Ecosystem

The solution was designed around SAP's enterprise ecosystem and supply-chain capabilities.

Key concepts explored in the project include:

* **SAP BTP**
* **SAP Ariba**
* **SAP Integrated Business Planning (IBP)**
* **SAP Joule**
* **Knowledge / Dependency Graphs**
* **AI Agents**

These components support the overall vision of connecting supply-chain data, intelligence, and decision support.

---

## ✨ Key Features

| Feature                       | Purpose                                        |
| ----------------------------- | ---------------------------------------------- |
| Multi-tier dependency mapping | Understand supplier relationships              |
| Contagion analysis            | Trace disruption propagation                   |
| AI agents                     | Automate scenario analysis                     |
| Logistics intelligence        | Identify operational exposure                  |
| Inventory analysis            | Understand supply impact                       |
| Scenario simulation           | Explore possible outcomes                      |
| Human-in-the-loop             | Maintain decision oversight                    |
| Risk visualization            | Make complex dependencies easier to understand |

---

## 🛠️ Technology & Concepts

**AI / Intelligence**

* Agentic AI
* Scenario Analysis
* Risk Intelligence
* Knowledge / Dependency Graphs

**SAP**

* SAP Business Technology Platform (BTP)
* SAP Ariba
* SAP IBP
* SAP Joule

**Development**

* Python
* JavaScript
* Web-based dashboard / prototype

> The exact technologies used by the prototype may vary from the broader SAP architecture explored during the hackathon.

---

## 👩‍💻 My Contribution

**Yatee Soni — Team Member**

Contributed to the development and presentation of RippleTrace as part of the **SAP Hackfest 2026 team**.

My work involved contributing to the project's:

* Product and solution development
* Supply-chain risk intelligence workflow
* Prototype implementation
* User-facing presentation and demonstration
* SAP Hackfest 2026 Grand Finale presentation

> Individual contribution can be updated here with specific modules as the project evolves.

---

## 🎥 Hackathon Presentation

**Event:** SAP Hackfest 2026
**Stage:** Grand Finale
**Venue:** Chandigarh University, Chandigarh
**Project:** RippleTrace — Agentic Multi-Tier Supply Chain Risk Intelligence

---

## 👥 Team

RippleTrace was developed collaboratively as part of our **SAP Hackfest 2026 team**.

The project involved collective work across:

* Product ideation
* Supply-chain analysis
* AI / agentic workflows
* Prototype development
* SAP ecosystem integration
* Presentation and demonstration

---

## 🚀 Future Scope

Potential future extensions include:

* Real-time supply-chain data integration
* Automated external event monitoring
* More advanced disruption propagation models
* Predictive inventory impact analysis
* Supplier risk scoring
* Real-time alerts
* Integration with enterprise SAP systems
* Advanced graph-based analytics
* Explainable AI recommendations

---

## 📌 Project Status

**Hackathon Prototype — SAP Hackfest 2026**

RippleTrace was developed and demonstrated as a functional hackathon prototype at the SAP Hackfest 2026 Grand Finale.

---

## 🔗 Links

**Original Team Repository:**
https://github.com/devansh-spec/RippleTrace

**My Fork:**
https://github.com/yateesoni/RippleTrace

---

## 📄 License

This repository is a fork of the original RippleTrace team repository. Please refer to the original repository for the applicable project license and ownership information.
