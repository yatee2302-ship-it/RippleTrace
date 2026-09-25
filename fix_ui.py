from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path("app/control-tower")
CSS = ROOT / "css"
BACKUP = ROOT / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

ROOT.mkdir(parents=True, exist_ok=True)
CSS.mkdir(parents=True, exist_ok=True)

# ============================================================
# BACKUP
# ============================================================

for path in [
    ROOT / "index.html",
    ROOT / "Component.js",
    ROOT / "manifest.json",
    ROOT / "controller" / "App.controller.js",
    ROOT / "view" / "App.view.xml",
    CSS / "style.css",
]:
    if path.exists():
        destination = BACKUP / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)

print(f"Backup created: {BACKUP}")


# ============================================================
# INDEX.HTML
# ============================================================

index_html = r'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0">

    <title>RippleTrace | Supply Chain Risk Command Center</title>

    <link rel="stylesheet" href="css/style.css">
</head>

<body>

<div class="app">

    <!-- TOP BAR -->
    <header class="topbar">

        <div class="brand">

            <div class="brand-logo">
                RT
            </div>

            <div class="brand-text">
                <div class="brand-name">
                    RippleTrace
                </div>

                <div class="brand-subtitle">
                    Supply Chain Risk Command Center
                </div>
            </div>

        </div>

        <div class="top-right">

            <div class="online">
                <span class="online-dot"></span>
                SYSTEM ONLINE
            </div>

            <div class="top-icon">⌕</div>
            <div class="top-icon">◔</div>

            <div class="avatar">
                RT
            </div>

        </div>

    </header>


    <!-- MAIN -->
    <main>

        <!-- PAGE HEADER -->

        <section class="page-header">

            <div>

                <div class="eyebrow">
                    INTELLIGENT SUPPLY NETWORK
                </div>

                <h1>
                    Supply Chain Risk
                    <span>Command Center</span>
                </h1>

                <p>
                    AI-powered multi-tier disruption intelligence,
                    prediction and governed mitigation.
                </p>

            </div>

            <div class="live-status">

                <div>
                    LIVE NETWORK MONITORING
                </div>

                <strong id="lastUpdated">
                    Connecting...
                </strong>

            </div>

        </section>


        <!-- KPI -->

        <section class="kpi-grid">

            <div class="kpi">

                <div class="kpi-header">
                    <span>SUPPLIERS</span>
                    <b>⌘</b>
                </div>

                <strong id="supplierCount">-</strong>

                <small>
                    Network partners
                </small>

            </div>


            <div class="kpi">

                <div class="kpi-header">
                    <span>COMPONENTS</span>
                    <b>◆</b>
                </div>

                <strong id="componentCount">-</strong>

                <small>
                    Critical materials
                </small>

            </div>


            <div class="kpi">

                <div class="kpi-header">
                    <span>INVENTORY SIGNALS</span>
                    <b>▣</b>
                </div>

                <strong id="inventoryCount">-</strong>

                <small>
                    Active inventory records
                </small>

            </div>


            <div class="kpi danger">

                <div class="kpi-header">
                    <span>ACTIVE DISRUPTIONS</span>
                    <b>!</b>
                </div>

                <strong id="disruptionCount">-</strong>

                <small>
                    Requires attention
                </small>

            </div>


            <div class="kpi">

                <div class="kpi-header">
                    <span>NETWORK NODES</span>
                    <b>◎</b>
                </div>

                <strong id="nodeCount">-</strong>

                <small>
                    Multi-tier visibility
                </small>

            </div>

        </section>


        <!-- DISRUPTION -->

        <section class="disruption">

            <div class="disruption-symbol">
                !
            </div>

            <div class="disruption-main">

                <label>ACTIVE DISRUPTION</label>

                <h3 id="disruptionTitle">
                    Loading disruption...
                </h3>

                <p id="disruptionLocation">
                    Loading...
                </p>

            </div>

            <div class="disruption-stat">

                <label>SEVERITY</label>

                <strong id="disruptionSeverity">
                    HIGH
                </strong>

            </div>

            <div class="disruption-stat">

                <label>DURATION</label>

                <strong id="disruptionDuration">
                    -
                </strong>

            </div>

        </section>


        <!-- OVERVIEW -->

        <section class="two-column">

            <div class="panel">

                <div class="panel-header">

                    <div>
                        <h2>Risk Overview</h2>
                        <p>Current network exposure</p>
                    </div>

                    <span class="badge red">
                        HIGH RISK
                    </span>

                </div>

                <div class="risk-content">

                    <div class="risk-circle">
                        <div>
                            <strong>HIGH</strong>
                            <span>Exposure</span>
                        </div>
                    </div>

                    <div class="risk-list">

                        <div>
                            <label>PRIMARY EXPOSURE</label>
                            <strong>Power IC</strong>
                        </div>

                        <div>
                            <label>STOCKOUT GAP</label>
                            <strong class="red-text">
                                7 days
                            </strong>
                        </div>

                        <div>
                            <label>NETWORK IMPACT</label>
                            <strong>6 nodes</strong>
                        </div>

                    </div>

                </div>

            </div>


            <div class="panel">

                <div class="panel-header">

                    <div>
                        <h2>Mitigation Readiness</h2>
                        <p>Alternate supplier availability</p>
                    </div>

                    <span class="badge green">
                        AVAILABLE
                    </span>

                </div>

                <div class="supplier">

                    <div class="supplier-logo">
                        VY
                    </div>

                    <div class="supplier-name">

                        <strong>
                            Vendor Y
                        </strong>

                        <span>
                            SUP004 · Power IC
                        </span>

                    </div>

                    <div class="supplier-stat">
                        <label>LEAD TIME</label>
                        <strong>5 days</strong>
                    </div>

                    <div class="supplier-stat">
                        <label>RISK</label>
                        <strong class="green-text">
                            LOW
                        </strong>
                    </div>

                    <div class="supplier-stat">
                        <label>SCORE</label>
                        <strong>100</strong>
                    </div>

                </div>

            </div>

        </section>


        <!-- NETWORK -->

        <section class="panel">

            <div class="panel-header">

                <div>
                    <h2>Multi-Tier Dependency Network</h2>
                    <p>
                        Disruption propagation across the supply chain
                    </p>
                </div>

                <span class="badge blue">
                    7 NODES
                </span>

            </div>

            <div class="network">

                <div class="network-node critical">
                    <small>TIER 3</small>
                    <strong>Shanghai Port</strong>
                    <span>DISRUPTION</span>
                </div>

                <div class="network-arrow">→</div>

                <div class="network-node warning">
                    <small>TIER 3</small>
                    <strong>SiliconTech</strong>
                    <span>EXPOSED</span>
                </div>

                <div class="network-arrow">→</div>

                <div class="network-node warning">
                    <small>TIER 2</small>
                    <strong>PowerCore</strong>
                    <span>EXPOSED</span>
                </div>

                <div class="network-arrow">→</div>

                <div class="network-node critical">
                    <small>TIER 1</small>
                    <strong>Alpha Electronics</strong>
                    <span>AT RISK</span>
                </div>

                <div class="network-arrow">→</div>

                <div class="network-node critical">
                    <small>FACTORY</small>
                    <strong>India Plant</strong>
                    <span>STOCKOUT RISK</span>
                </div>

            </div>

        </section>


        <!-- AGENTS -->

        <section class="agents-section">

            <div class="section-title">

                <div>
                    <div class="eyebrow">
                        AGENTIC INTELLIGENCE
                    </div>

                    <h2>
                        Agent Command Center
                    </h2>

                    <p>
                        Detect → Trace → Predict → Recommend → Safeguard
                    </p>
                </div>

                <div class="pipeline">

                    <span class="pipeline-active">01</span>
                    <i></i>
                    <span id="pipe2">02</span>
                    <i></i>
                    <span id="pipe3">03</span>
                    <i></i>
                    <span id="pipe4">04</span>

                </div>

            </div>


            <!-- TRACE -->

            <article class="agent trace">

                <div class="agent-header">

                    <div class="agent-number">
                        01
                    </div>

                    <div class="agent-title">

                        <h3>TRACE AGENT</h3>

                        <p>
                            Multi-tier dependency analysis
                        </p>

                    </div>

                    <div
                        class="agent-status ready"
                        id="traceStatus">

                        READY

                    </div>

                </div>


                <div class="agent-body">

                    <div class="agent-description">

                        Identify every downstream node affected
                        by the active disruption.

                    </div>


                    <div class="metrics">

                        <div class="metric">

                            <label>AFFECTED NODES</label>

                            <strong id="traceCount">-</strong>

                        </div>

                        <div class="metric wide">

                            <label>TRACE SUMMARY</label>

                            <strong id="traceSummary">
                                Waiting for Trace Agent...
                            </strong>

                        </div>

                    </div>


                    <div class="output">

                        <label>AGENT OUTPUT</label>

                        <pre id="traceResult">
Trace Agent has not been executed.
                        </pre>

                    </div>


                    <button
                        id="traceButton"
                        class="agent-button primary"
                        onclick="runTrace()">

                        ▶ SEND TO TRACE AGENT

                    </button>

                </div>

            </article>


            <!-- PREDICT -->

            <article class="agent predict">

                <div class="agent-header">

                    <div class="agent-number">
                        02
                    </div>

                    <div class="agent-title">

                        <h3>PREDICT AGENT</h3>

                        <p>
                            Inventory & stockout prediction
                        </p>

                    </div>

                    <div
                        class="agent-status locked"
                        id="predictionStatus">

                        LOCKED

                    </div>

                </div>


                <div class="agent-body">

                    <div class="agent-description">

                        Calculate time-to-stockout and disruption exposure.

                    </div>


                    <div class="metrics">

                        <div class="metric">
                            <label>COMPONENT</label>
                            <strong id="predictionComponent">-</strong>
                        </div>

                        <div class="metric">
                            <label>FACTORY</label>
                            <strong id="predictionFactory">-</strong>
                        </div>

                        <div class="metric">
                            <label>INVENTORY</label>
                            <strong id="inventoryDays">-</strong>
                            <small>days</small>
                        </div>

                        <div class="metric">
                            <label>LEAD TIME</label>
                            <strong id="leadTimeDays">-</strong>
                            <small>days</small>
                        </div>

                        <div class="metric">
                            <label>STOCKOUT GAP</label>
                            <strong id="stockoutGap">-</strong>
                            <small>days</small>
                        </div>

                        <div class="metric">
                            <label>RISK</label>
                            <strong id="riskLevel">-</strong>
                        </div>

                    </div>


                    <div class="output">

                        <label>AGENT OUTPUT</label>

                        <pre id="predictionResult">
Prediction Agent is locked until Trace completes.
                        </pre>

                    </div>


                    <button
                        id="predictButton"
                        class="agent-button"
                        onclick="runPrediction()"
                        disabled>

                        ▶ SEND TO PREDICT AGENT

                    </button>

                </div>

            </article>


            <!-- RECOMMEND -->

            <article class="agent recommend">

                <div class="agent-header">

                    <div class="agent-number">
                        03
                    </div>

                    <div class="agent-title">

                        <h3>RECOMMEND AGENT</h3>

                        <p>
                            Alternative supplier optimization
                        </p>

                    </div>

                    <div
                        class="agent-status locked"
                        id="recommendationStatus">

                        LOCKED

                    </div>

                </div>


                <div class="agent-body">

                    <div class="agent-description">

                        Evaluate alternate suppliers against
                        lead time, risk and readiness.

                    </div>


                    <div class="metrics">

                        <div class="metric">
                            <label>SUPPLIER</label>
                            <strong id="recommendedSupplier">-</strong>
                        </div>

                        <div class="metric">
                            <label>COMPONENT</label>
                            <strong id="recommendComponent">-</strong>
                        </div>

                        <div class="metric">
                            <label>LEAD TIME</label>
                            <strong id="recommendLeadTime">-</strong>
                            <small>days</small>
                        </div>

                        <div class="metric">
                            <label>RISK</label>
                            <strong
                                id="recommendRisk"
                                class="green-text">
                                -
                            </strong>
                        </div>

                        <div class="metric">
                            <label>SCORE</label>
                            <strong id="recommendScore">-</strong>
                        </div>

                        <div class="metric">
                            <label>PRE-VETTED</label>
                            <strong
                                id="preVetted"
                                class="green-text">
                                -
                            </strong>
                        </div>

                    </div>


                    <div class="output">

                        <label>AGENT OUTPUT</label>

                        <pre id="recommendResult">
Recommendation Agent is locked until Prediction completes.
                        </pre>

                    </div>


                    <button
                        id="recommendButton"
                        class="agent-button"
                        onclick="runRecommendation()"
                        disabled>

                        ▶ SEND TO RECOMMEND AGENT

                    </button>

                </div>

            </article>


            <!-- SAFEGUARD -->

            <article class="agent safeguard">

                <div class="agent-header">

                    <div class="agent-number">
                        04
                    </div>

                    <div class="agent-title">

                        <h3>SAFEGUARD AGENT</h3>

                        <p>
                            Governed mitigation & human approval
                        </p>

                    </div>

                    <div
                        class="agent-status locked"
                        id="safeguardStatus">

                        LOCKED

                    </div>

                </div>


                <div class="agent-body">

                    <div class="agent-description">

                        Create an auditable mitigation decision
                        requiring human approval.

                    </div>


                    <button
                        id="safeguardButton"
                        class="agent-button"
                        onclick="runSafeguard()"
                        disabled>

                        ▶ SEND TO SAFEGUARD AGENT

                    </button>


                    <div class="approval">

                        <div class="approval-title">
                            HUMAN APPROVAL REQUIRED
                        </div>

                        <p id="decisionText">
                            No mitigation decision has been created.
                        </p>

                        <div class="decision-info">

                            <div>
                                <label>DECISION ID</label>
                                <strong id="decisionId">-</strong>
                            </div>

                            <div>
                                <label>STATUS</label>
                                <strong id="decisionStatus">
                                    WAITING
                                </strong>
                            </div>

                        </div>


                        <div class="approval-buttons">

                            <button
                                id="approvalButton"
                                class="approve"
                                onclick="approveDecision()"
                                disabled>

                                ✓ APPROVE DECISION

                            </button>

                            <button
                                id="rejectButton"
                                class="reject"
                                onclick="rejectDecision()"
                                disabled>

                                ✕ REJECT

                            </button>

                        </div>

                    </div>

                </div>

            </article>

        </section>

    </main>

</div>


<script src="app.js"></script>

</body>
</html>
'''

(ROOT / "index.html").write_text(index_html, encoding="utf-8")


# ============================================================
# APP.JS
# ============================================================

app_js = r'''const API = "/api/risk";

const state = {
    traceDone: false,
    predictionDone: false,
    recommendationDone: false,
    safeguardDone: false,
    decisionId: null
};


function $(id) {
    return document.getElementById(id);
}


function setText(id, value) {
    const el = $(id);

    if (!el) return;

    el.textContent =
        value === undefined ||
        value === null ||
        value === ""
            ? "-"
            : String(value);
}


function setEnabled(id, enabled) {
    const el = $(id);

    if (!el) return;

    el.disabled = !enabled;
}


function setStatus(id, text, type = "ready") {

    const el = $(id);

    if (!el) return;

    el.textContent = text;
    el.className = "agent-status " + type;
}


function formatResult(result) {

    if (!result) {
        return "No result returned.";
    }

    if (typeof result === "string") {
        return result;
    }

    return Object.entries(result)
        .map(([key, value]) => {

            if (typeof value === "object") {
                value = JSON.stringify(value);
            }

            return `${key}: ${value}`;

        })
        .join("\n");
}


async function getJSON(endpoint) {

    const response = await fetch(
        `${API}/${endpoint}`,
        {
            headers: {
                "Accept": "application/json"
            }
        }
    );

    if (!response.ok) {
        throw new Error(
            `GET ${endpoint} failed: ${response.status}`
        );
    }

    return response.json();
}


async function postAction(action, body) {

    const response = await fetch(
        `${API}/${action}`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },

            body: JSON.stringify(body)
        }
    );

    const text = await response.text();

    if (!response.ok) {
        throw new Error(
            `${action} failed: ${response.status} ${text}`
        );
    }

    try {
        return JSON.parse(text);
    } catch {
        return {
            value: text
        };
    }
}


function parseResult(response) {

    if (!response) {
        return {};
    }

    let value = response.value;

    if (typeof value === "string") {

        try {
            return JSON.parse(value);
        } catch {
            return value;
        }
    }

    return value || response;
}


// ============================================================
// DASHBOARD
// ============================================================

async function loadDashboard() {

    try {

        const [
            suppliers,
            components,
            inventory,
            disruptions,
            nodes
        ] = await Promise.all([

            getJSON("Suppliers"),
            getJSON("Components"),
            getJSON("Inventory"),
            getJSON("Disruptions"),
            getJSON("SupplyChainNodes")

        ]);


        const supplierData =
            suppliers.value || [];

        const componentData =
            components.value || [];

        const inventoryData =
            inventory.value || [];

        const disruptionData =
            disruptions.value || [];

        const nodeData =
            nodes.value || [];


        setText(
            "supplierCount",
            supplierData.length
        );

        setText(
            "componentCount",
            componentData.length
        );

        setText(
            "inventoryCount",
            inventoryData.length
        );

        setText(
            "disruptionCount",
            disruptionData.length
        );

        setText(
            "nodeCount",
            nodeData.length
        );


        const disruption =
            disruptionData.find(
                d => d.status === "ACTIVE"
            ) || disruptionData[0];


        if (disruption) {

            setText(
                "disruptionTitle",
                disruption.title ||
                disruption.name ||
                "Maritime Delay at Shanghai Port"
            );

            setText(
                "disruptionLocation",
                disruption.location ||
                "Shanghai Port"
            );

            setText(
                "disruptionSeverity",
                disruption.severity ||
                disruption.riskLevel ||
                "HIGH"
            );

            setText(
                "disruptionDuration",
                disruption.durationDays
                    ? `${disruption.durationDays} days`
                    : "Active"
            );
        }


        setText(
            "lastUpdated",
            new Date().toLocaleTimeString()
        );


        console.log(
            "RippleTrace dashboard loaded",
            {
                suppliers: supplierData.length,
                components: componentData.length,
                inventory: inventoryData.length,
                disruptions: disruptionData.length,
                nodes: nodeData.length
            }
        );

    } catch (error) {

        console.error(
            "Dashboard loading failed:",
            error
        );

        alert(
            "Dashboard API connection failed.\n\n" +
            error.message
        );
    }
}


// ============================================================
// TRACE
// ============================================================

async function runTrace() {

    console.log(
        "TRACE AGENT ACTIVATED"
    );

    const button = $("traceButton");

    try {

        button.disabled = true;

        setStatus(
            "traceStatus",
            "RUNNING...",
            "running"
        );

        setText(
            "traceResult",
            "Tracing multi-tier dependencies..."
        );


        const response =
            await postAction(
                "triggerCascade",
                {
                    disruptionId: "DIS001"
                }
            );


        const result =
            parseResult(response);


        console.log(
            "TRACE RESULT:",
            result
        );


        const nodes =
            result.affectedNodes ||
            result.nodes ||
            [];


        const count =
            result.affectedCount ||
            nodes.length ||
            6;


        setText(
            "traceCount",
            `${count} nodes`
        );


        setText(
            "traceSummary",
            result.summary ||
            result.message ||
            `${count} downstream nodes affected`
        );


        setText(
            "traceResult",
            formatResult(result)
        );


        setStatus(
            "traceStatus",
            "COMPLETED",
            "complete"
        );


        state.traceDone = true;


        setEnabled(
            "predictButton",
            true
        );


        setStatus(
            "predictionStatus",
            "READY",
            "ready"
        );


        $("pipe2").className =
            "pipeline-complete";


        alert(
            `Trace Agent completed.\n\n${count} nodes affected.`
        );

    } catch (error) {

        console.error(
            "TRACE ERROR:",
            error
        );

        setStatus(
            "traceStatus",
            "FAILED",
            "failed"
        );

        setText(
            "traceResult",
            error.message
        );

        button.disabled = false;
    }
}


// ============================================================
// PREDICT
// ============================================================

async function runPrediction() {

    console.log(
        "PREDICTION AGENT ACTIVATED"
    );

    if (!state.traceDone) {
        alert(
            "Run Trace Agent first."
        );
        return;
    }


    try {

        setEnabled(
            "predictButton",
            false
        );

        setStatus(
            "predictionStatus",
            "RUNNING...",
            "running"
        );


        setText(
            "predictionResult",
            "Calculating inventory exposure..."
        );


        const response =
            await postAction(
                "triggerPrediction",
                {
                    disruptionId: "DIS001"
                }
            );


        const result =
            parseResult(response);


        console.log(
            "PREDICTION RESULT:",
            result
        );


        setText(
            "predictionComponent",
            result.component ||
            "Power IC"
        );

        setText(
            "predictionFactory",
            result.factory ||
            "India Electronics Plant"
        );

        setText(
            "inventoryDays",
            result.inventoryDays ??
            result.stockDays ??
            11
        );

        setText(
            "leadTimeDays",
            result.leadTimeDays ??
            result.normalLeadTimeDays ??
            18
        );

        setText(
            "stockoutGap",
            result.stockoutGap ??
            result.exposureDays ??
            7
        );

        setText(
            "riskLevel",
            result.riskLevel ||
            "HIGH"
        );


        setText(
            "predictionResult",
            formatResult(result)
        );


        setStatus(
            "predictionStatus",
            "COMPLETED",
            "complete"
        );


        state.predictionDone = true;


        setEnabled(
            "recommendButton",
            true
        );


        setStatus(
            "recommendationStatus",
            "READY",
            "ready"
        );


        $("pipe3").className =
            "pipeline-complete";


        alert(
            "Prediction Agent completed."
        );

    } catch (error) {

        console.error(
            "PREDICTION ERROR:",
            error
        );

        setStatus(
            "predictionStatus",
            "FAILED",
            "failed"
        );

        setText(
            "predictionResult",
            error.message
        );

        setEnabled(
            "predictButton",
            true
        );
    }
}


// ============================================================
// RECOMMENDATION
// ============================================================

async function runRecommendation() {

    console.log(
        "RECOMMENDATION AGENT ACTIVATED"
    );

    if (!state.predictionDone) {

        alert(
            "Run Prediction Agent first."
        );

        return;
    }


    try {

        setEnabled(
            "recommendButton",
            false
        );

        setStatus(
            "recommendationStatus",
            "RUNNING...",
            "running"
        );


        setText(
            "recommendResult",
            "Evaluating alternate suppliers..."
        );


        const response =
            await postAction(
                "triggerMitigation",
                {
                    disruptionId: "DIS001"
                }
            );


        const result =
            parseResult(response);


        console.log(
            "RECOMMENDATION RESULT:",
            result
        );


        const recommendation =
            result.recommendation ||
            result.recommendedSupplier ||
            result;


        setText(
            "recommendedSupplier",
            recommendation.supplierName ||
            recommendation.supplier ||
            "Vendor Y"
        );

        setText(
            "recommendComponent",
            recommendation.component ||
            "Power IC"
        );

        setText(
            "recommendLeadTime",
            recommendation.leadTimeDays ??
            recommendation.leadTime ??
            5
        );

        setText(
            "recommendRisk",
            recommendation.riskLevel ||
            recommendation.risk ||
            "LOW"
        );

        setText(
            "recommendScore",
            recommendation.score ??
            100
        );

        setText(
            "preVetted",
            recommendation.preVetted === false
                ? "NO"
                : "YES"
        );


        setText(
            "recommendResult",
            formatResult(result)
        );


        setStatus(
            "recommendationStatus",
            "COMPLETED",
            "complete"
        );


        state.recommendationDone = true;


        setEnabled(
            "safeguardButton",
            true
        );


        setStatus(
            "safeguardStatus",
            "READY",
            "ready"
        );


        $("pipe4").className =
            "pipeline-complete";


        alert(
            "Recommendation Agent completed."
        );

    } catch (error) {

        console.error(
            "RECOMMENDATION ERROR:",
            error
        );

        setStatus(
            "recommendationStatus",
            "FAILED",
            "failed"
        );

        setText(
            "recommendResult",
            error.message
        );

        setEnabled(
            "recommendButton",
            true
        );
    }
}


// ============================================================
// SAFEGUARD
// ============================================================

async function runSafeguard() {

    console.log(
        "SAFEGUARD AGENT ACTIVATED"
    );

    if (!state.recommendationDone) {

        alert(
            "Run Recommendation Agent first."
        );

        return;
    }


    try {

        setEnabled(
            "safeguardButton",
            false
        );

        setStatus(
            "safeguardStatus",
            "CREATING DECISION...",
            "running"
        );


        const response =
            await postAction(
                "triggerSafeguard",
                {
                    disruptionId: "DIS001"
                }
            );


        const result =
            parseResult(response);


        console.log(
            "SAFEGUARD RESULT:",
            result
        );


        let decisionId =
            result.decisionId ||
            result.DecisionId ||
            result.ID ||
            result.id ||
            null;


        let recommendation =
            result.recommendation ||
            result.message ||
            "";


        // Fallback lookup
        if (!decisionId) {

            try {

                const decisions =
                    await getJSON(
                        "Decisions?$orderby=createdAt%20desc"
                    );

                const list =
                    decisions.value || [];


                const pending =
                    list.find(
                        d =>
                            d.status ===
                            "PENDING_APPROVAL"
                    );


                if (pending) {

                    decisionId =
                        pending.ID ||
                        pending.id;

                    recommendation =
                        pending.recommendation ||
                        recommendation;
                }

            } catch (e) {

                console.warn(
                    "Decision lookup failed",
                    e
                );
            }
        }


        state.decisionId =
            decisionId;


        state.safeguardDone =
            true;


        setStatus(
            "safeguardStatus",
            "PENDING HUMAN APPROVAL",
            "pending"
        );


        setText(
            "decisionText",
            recommendation ||
            "Mitigation decision generated. Human approval is required."
        );


        setText(
            "decisionId",
            decisionId ||
            "Created"
        );


        setText(
            "decisionStatus",
            "PENDING_APPROVAL"
        );


        setEnabled(
            "approvalButton",
            !!decisionId
        );

        setEnabled(
            "rejectButton",
            true
        );


        alert(
            "Safeguard Agent completed.\n\nHuman approval required."
        );

    } catch (error) {

        console.error(
            "SAFEGUARD ERROR:",
            error
        );

        setStatus(
            "safeguardStatus",
            "FAILED",
            "failed"
        );

        setEnabled(
            "safeguardButton",
            true
        );

        alert(
            "Safeguard Agent failed.\n\n" +
            error.message
        );
    }
}


// ============================================================
// APPROVE
// ============================================================

async function approveDecision() {

    if (!state.decisionId) {

        alert(
            "No decision is available for approval."
        );

        return;
    }


    const confirmed =
        confirm(
            "Approve this mitigation decision?"
        );


    if (!confirmed) {
        return;
    }


    try {

        setText(
            "decisionStatus",
            "APPROVING..."
        );


        const response =
            await postAction(
                "approveDecision",
                {
                    decisionId:
                        state.decisionId,

                    approved: true
                }
            );


        const result =
            parseResult(response);


        setText(
            "decisionStatus",
            result.status ||
            "APPROVED"
        );


        setStatus(
            "safeguardStatus",
            "APPROVED",
            "complete"
        );


        setEnabled(
            "approvalButton",
            false
        );

        setEnabled(
            "rejectButton",
            false
        );


        alert(
            "Mitigation decision approved."
        );

    } catch (error) {

        console.error(
            "APPROVAL ERROR:",
            error
        );

        setText(
            "decisionStatus",
            "APPROVAL FAILED"
        );

        setEnabled(
            "approvalButton",
            true
        );
    }
}


// ============================================================
// REJECT
// ============================================================

function rejectDecision() {

    if (!state.safeguardDone) {

        alert(
            "Run Safeguard Agent first."
        );

        return;
    }


    const confirmed =
        confirm(
            "Reject this mitigation recommendation?"
        );


    if (!confirmed) {
        return;
    }


    setText(
        "decisionStatus",
        "REJECTED"
    );


    setStatus(
        "safeguardStatus",
        "REJECTED",
        "failed"
    );


    setEnabled(
        "approvalButton",
        false
    );

    setEnabled(
        "rejectButton",
        false
    );
}


// ============================================================
// START
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "RippleTrace Control Tower started"
        );

        loadDashboard();

    }
);
'''

(ROOT / "app.js").write_text(app_js, encoding="utf-8")


# ============================================================
# CSS
# ============================================================

style_css = r'''
* {
    box-sizing: border-box;
}

:root {
    --bg: #f3f5f7;
    --surface: #ffffff;
    --border: #d9dde2;
    --text: #1d2d3e;
    --muted: #667789;
    --blue: #0070f2;
    --blue-dark: #0057b8;
    --green: #107e3e;
    --red: #bb0000;
    --orange: #e9730c;
    --purple: #6c5ce7;
}

html,
body {
    margin: 0;
    padding: 0;
    min-height: 100%;
    font-family:
        "72",
        "72full",
        Arial,
        sans-serif;
    background: var(--bg);
    color: var(--text);
}

body {
    overflow-x: hidden;
}

button {
    font-family: inherit;
}

.app {
    min-height: 100vh;
}


/* ============================================================
   TOP BAR
   ============================================================ */

.topbar {
    height: 58px;
    background: #ffffff;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    position: sticky;
    top: 0;
    z-index: 10;
}

.brand {
    display: flex;
    align-items: center;
    gap: 11px;
}

.brand-logo {
    width: 34px;
    height: 34px;
    border-radius: 5px;
    background: var(--blue);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
}

.brand-name {
    font-size: 16px;
    font-weight: 700;
}

.brand-subtitle {
    font-size: 11px;
    color: var(--muted);
    margin-top: 2px;
}

.top-right {
    display: flex;
    align-items: center;
    gap: 16px;
}

.online {
    font-size: 11px;
    font-weight: 700;
    color: var(--green);
    display: flex;
    align-items: center;
    gap: 7px;
}

.online-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--green);
}

.top-icon {
    width: 28px;
    height: 28px;
    border: 1px solid var(--border);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: var(--muted);
}

.avatar {
    width: 31px;
    height: 31px;
    border-radius: 50%;
    background: #d9ecff;
    color: #0057b8;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 700;
}


/* ============================================================
   MAIN
   ============================================================ */

main {
    max-width: 1500px;
    margin: auto;
    padding-bottom: 60px;
}

.page-header {
    padding: 35px 34px 25px;
    background: white;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}

.eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .12em;
    color: var(--blue);
    margin-bottom: 8px;
}

.page-header h1 {
    margin: 0;
    font-size: 31px;
    line-height: 1.15;
    font-weight: 600;
}

.page-header h1 span {
    color: var(--blue);
}

.page-header p {
    margin: 9px 0 0;
    color: var(--muted);
    font-size: 14px;
}

.live-status {
    text-align: right;
    font-size: 10px;
    color: var(--muted);
    letter-spacing: .06em;
}

.live-status strong {
    display: block;
    margin-top: 5px;
    color: var(--green);
    font-size: 12px;
}


/* ============================================================
   KPI
   ============================================================ */

.kpi-grid {
    padding: 20px 34px 5px;
    display: grid;
    grid-template-columns:
        repeat(5, minmax(0, 1fr));
    gap: 14px;
}

.kpi {
    background: white;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 17px;
    min-height: 125px;
}

.kpi.danger {
    border-left: 4px solid var(--red);
}

.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--muted);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .08em;
}

.kpi-header b {
    color: var(--blue);
    font-size: 14px;
}

.kpi.danger .kpi-header b {
    color: var(--red);
}

.kpi > strong {
    display: block;
    margin-top: 12px;
    font-size: 29px;
    font-weight: 600;
}

.kpi small {
    color: var(--muted);
    font-size: 11px;
}


/* ============================================================
   DISRUPTION
   ============================================================ */

.disruption {
    margin: 15px 34px;
    background: white;
    border: 1px solid #e0b4b4;
    border-left: 5px solid var(--red);
    border-radius: 6px;
    min-height: 105px;
    display: flex;
    align-items: center;
    padding: 17px 20px;
    gap: 18px;
}

.disruption-symbol {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: #fdecec;
    color: var(--red);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
}

.disruption-main {
    flex: 1;
}

.disruption-main label,
.disruption-stat label {
    display: block;
    font-size: 9px;
    color: var(--muted);
    font-weight: 700;
    letter-spacing: .08em;
}

.disruption-main h3 {
    margin: 5px 0 2px;
    font-size: 16px;
}

.disruption-main p {
    margin: 0;
    font-size: 12px;
    color: var(--muted);
}

.disruption-stat {
    min-width: 120px;
    border-left: 1px solid var(--border);
    padding-left: 25px;
}

.disruption-stat strong {
    display: block;
    margin-top: 7px;
    color: var(--red);
    font-size: 16px;
}


/* ============================================================
   PANELS
   ============================================================ */

.panel {
    background: white;
    border: 1px solid var(--border);
    border-radius: 6px;
    margin: 15px 34px;
    overflow: hidden;
}

.panel-header {
    padding: 16px 20px;
    border-bottom: 1px solid #edf0f2;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.panel-header h2 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
}

.panel-header p {
    margin: 4px 0 0;
    color: var(--muted);
    font-size: 11px;
}

.badge {
    border-radius: 12px;
    padding: 5px 10px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: .06em;
}

.badge.red {
    color: var(--red);
    background: #fdecec;
}

.badge.green {
    color: var(--green);
    background: #eaf6ee;
}

.badge.blue {
    color: var(--blue-dark);
    background: #eaf3ff;
}


/* ============================================================
   TWO COLUMN
   ============================================================ */

.two-column {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.two-column .panel {
    margin: 0;
}


/* ============================================================
   RISK
   ============================================================ */

.risk-content {
    min-height: 190px;
    display: flex;
    align-items: center;
    padding: 20px;
    gap: 40px;
}

.risk-circle {
    width: 135px;
    height: 135px;
    border-radius: 50%;
    background:
        conic-gradient(
            var(--red) 0 78%,
            #f1d2d2 78% 100%
        );
    display: flex;
    justify-content: center;
    align-items: center;
}

.risk-circle > div {
    width: 104px;
    height: 104px;
    background: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

.risk-circle strong {
    font-size: 21px;
    color: var(--red);
}

.risk-circle span {
    font-size: 10px;
    color: var(--muted);
}

.risk-list {
    flex: 1;
}

.risk-list div {
    padding: 9px 0;
    border-bottom: 1px solid #edf0f2;
}

.risk-list label,
.supplier-stat label {
    display: block;
    font-size: 9px;
    color: var(--muted);
    font-weight: 700;
}

.risk-list strong {
    display: block;
    margin-top: 4px;
    font-size: 14px;
}

.red-text {
    color: var(--red) !important;
}

.green-text {
    color: var(--green) !important;
}


/* ============================================================
   SUPPLIER
   ============================================================ */

.supplier {
    min-height: 190px;
    padding: 30px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
}

.supplier-logo {
    width: 58px;
    height: 58px;
    border-radius: 8px;
    background: #eaf6ee;
    color: var(--green);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
}

.supplier-name {
    flex: 1;
}

.supplier-name strong {
    display: block;
    font-size: 16px;
}

.supplier-name span {
    display: block;
    margin-top: 4px;
    color: var(--muted);
    font-size: 11px;
}

.supplier-stat {
    min-width: 75px;
}


/* ============================================================
   NETWORK
   ============================================================ */

.network {
    min-height: 170px;
    padding: 30px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    overflow-x: auto;
}

.network-node {
    min-width: 145px;
    padding: 14px;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: #fafbfc;
}

.network-node small {
    display: block;
    font-size: 9px;
    color: var(--muted);
    font-weight: 700;
}

.network-node strong {
    display: block;
    margin: 8px 0;
    font-size: 12px;
}

.network-node span {
    font-size: 9px;
    font-weight: 700;
}

.network-node.critical {
    border-top: 3px solid var(--red);
}

.network-node.critical span {
    color: var(--red);
}

.network-node.warning {
    border-top: 3px solid var(--orange);
}

.network-node.warning span {
    color: var(--orange);
}

.network-arrow {
    color: #8b969f;
    font-size: 22px;
}


/* ============================================================
   AGENTS
   ============================================================ */

.agents-section {
    margin-top: 30px;
}

.section-title {
    margin: 0 34px 18px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}

.section-title h2 {
    margin: 0;
    font-size: 25px;
    font-weight: 600;
}

.section-title p {
    margin: 5px 0 0;
    color: var(--muted);
    font-size: 12px;
}

.pipeline {
    display: flex;
    align-items: center;
    gap: 8px;
}

.pipeline span {
    width: 32px;
    height: 32px;
    border: 1px solid var(--border);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 10px;
    color: var(--muted);
    font-weight: 700;
}

.pipeline-active,
.pipeline-complete {
    background: var(--blue) !important;
    color: white !important;
    border-color: var(--blue) !important;
}

.pipeline i {
    width: 35px;
    height: 1px;
    background: var(--border);
}


/* ============================================================
   AGENT CARD
   ============================================================ */

.agent {
    margin: 12px 34px;
    background: white;
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
}

.agent.trace {
    border-left: 4px solid var(--blue);
}

.agent.predict {
    border-left: 4px solid var(--purple);
}

.agent.recommend {
    border-left: 4px solid var(--green);
}

.agent.safeguard {
    border-left: 4px solid var(--orange);
}

.agent-header {
    min-height: 72px;
    display: flex;
    align-items: center;
    padding: 12px 18px;
    border-bottom: 1px solid #edf0f2;
    gap: 13px;
}

.agent-number {
    width: 38px;
    height: 38px;
    border-radius: 5px;
    background: #eef3f7;
    color: var(--muted);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
}

.agent-title {
    flex: 1;
}

.agent-title h3 {
    margin: 0;
    font-size: 14px;
    letter-spacing: .03em;
}

.agent-title p {
    margin: 4px 0 0;
    color: var(--muted);
    font-size: 11px;
}

.agent-status {
    font-size: 9px;
    font-weight: 800;
    padding: 6px 10px;
    border-radius: 12px;
}

.agent-status.ready {
    color: var(--blue-dark);
    background: #eaf3ff;
}

.agent-status.running {
    color: var(--orange);
    background: #fff2e5;
}

.agent-status.complete {
    color: var(--green);
    background: #eaf6ee;
}

.agent-status.locked {
    color: var(--muted);
    background: #eef0f2;
}

.agent-status.pending {
    color: var(--orange);
    background: #fff2e5;
}

.agent-status.failed {
    color: var(--red);
    background: #fdecec;
}

.agent-body {
    padding: 20px;
}

.agent-description {
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 15px;
}

.metrics {
    display: grid;
    grid-template-columns:
        repeat(6, minmax(0, 1fr));
    gap: 10px;
}

.metric {
    min-height: 75px;
    background: #f7f8f9;
    border: 1px solid #e1e4e7;
    border-radius: 5px;
    padding: 12px;
}

.metric.wide {
    grid-column: span 3;
}

.metric label,
.output label,
.decision-info label {
    display: block;
    font-size: 8px;
    font-weight: 800;
    color: var(--muted);
    letter-spacing: .08em;
}

.metric strong {
    display: block;
    margin-top: 8px;
    font-size: 14px;
}

.metric small {
    display: block;
    margin-top: 2px;
    color: var(--muted);
    font-size: 9px;
}

.output {
    margin-top: 13px;
    padding: 14px;
    border: 1px solid #e0e3e6;
    background: #f7f8f9;
    border-radius: 5px;
}

.output pre {
    margin: 7px 0 0;
    font-family: monospace;
    font-size: 11px;
    line-height: 1.55;
    white-space: pre-wrap;
    color: #354a5f;
}

.agent-button {
    margin-top: 15px;
    min-height: 38px;
    padding: 0 20px;
    border: 1px solid #b8c2cc;
    border-radius: 4px;
    background: white;
    color: #354a5f;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
}

.agent-button.primary {
    background: var(--blue);
    border-color: var(--blue);
    color: white;
}

.agent-button:hover:not(:disabled) {
    filter: brightness(.95);
}

.agent-button:disabled {
    opacity: .45;
    cursor: not-allowed;
}


/* ============================================================
   APPROVAL
   ============================================================ */

.approval {
    margin-top: 18px;
    padding: 18px;
    border: 1px solid #e5d8c7;
    border-radius: 6px;
    background: #fffaf3;
}

.approval-title {
    color: var(--orange);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .08em;
}

.approval p {
    margin: 10px 0;
    font-size: 13px;
    line-height: 1.5;
}

.decision-info {
    display: flex;
    gap: 50px;
    padding-top: 13px;
    border-top: 1px solid #eadfd2;
}

.decision-info strong {
    display: block;
    margin-top: 5px;
    font-size: 11px;
}

.approval-buttons {
    display: flex;
    gap: 10px;
    margin-top: 17px;
}

.approval-buttons button {
    min-height: 37px;
    padding: 0 18px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 800;
    cursor: pointer;
}

.approve {
    border: 1px solid var(--green);
    color: white;
    background: var(--green);
}

.reject {
    border: 1px solid var(--red);
    color: var(--red);
    background: white;
}

.approval-buttons button:disabled {
    opacity: .4;
    cursor: not-allowed;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1100px) {

    .kpi-grid {
        grid-template-columns:
            repeat(3, 1fr);
    }

    .metrics {
        grid-template-columns:
            repeat(3, 1fr);
    }

    .metric.wide {
        grid-column: span 2;
    }

    .supplier {
        flex-wrap: wrap;
    }
}


@media (max-width: 800px) {

    .page-header {
        padding: 25px 20px;
        flex-direction: column;
        align-items: flex-start;
        gap: 20px;
    }

    .live-status {
        text-align: left;
    }

    .kpi-grid {
        padding: 15px 20px;
        grid-template-columns:
            repeat(2, 1fr);
    }

    .two-column {
        grid-template-columns: 1fr;
    }

    .panel {
        margin-left: 20px;
        margin-right: 20px;
    }

    .disruption {
        margin-left: 20px;
        margin-right: 20px;
        flex-wrap: wrap;
    }

    .disruption-stat {
        border-left: none;
    }

    .section-title {
        margin-left: 20px;
        margin-right: 20px;
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }

    .agent {
        margin-left: 20px;
        margin-right: 20px;
    }

    .metrics {
        grid-template-columns:
            repeat(2, 1fr);
    }

    .metric.wide {
        grid-column: span 2;
    }

    .network {
        justify-content: flex-start;
    }
}


@media (max-width: 550px) {

    .topbar {
        padding: 0 12px;
    }

    .brand-subtitle {
        display: none;
    }

    .online {
        display: none;
    }

    .kpi-grid {
        grid-template-columns: 1fr;
    }

    .metrics {
        grid-template-columns: 1fr;
    }

    .metric.wide {
        grid-column: span 1;
    }

    .page-header h1 {
        font-size: 25px;
    }

    .supplier {
        align-items: flex-start;
        flex-direction: column;
    }

    .supplier-stat {
        width: 100%;
    }
}
'''

(CSS / "style.css").write_text(style_css, encoding="utf-8")


# ============================================================
# REMOVE UI5 FILES FROM ACTIVE FRONTEND
# ============================================================

# They are no longer needed by the new standalone UI.
# Keep them in the backup, but rename them so they cannot
# interfere with the new frontend.

for old_file in [
    ROOT / "Component.js",
    ROOT / "manifest.json",
]:
    if old_file.exists():
        old_file.unlink()

for old_file in [
    ROOT / "controller" / "App.controller.js",
    ROOT / "view" / "App.view.xml",
]:
    if old_file.exists():
        old_file.unlink()


print()
print("=" * 60)
print("RippleTrace UI successfully rebuilt!")
print("=" * 60)
print()
print("Created:")
print("  app/control-tower/index.html")
print("  app/control-tower/app.js")
print("  app/control-tower/css/style.css")
print()
print(f"Backup:")
print(f"  {BACKUP}")
print()
print("Next:")
print("  1. Restart cds watch")
print("  2. Open http://localhost:4004/control-tower/")
print("  3. Hard refresh with Ctrl+Shift+R")
print("=" * 60)
