#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "RippleTrace"
APP = ROOT / "app" / "control-tower"

INDEX = APP / "index.html"
CSS = APP / "css" / "style.css"
REALTIME = APP / "realtime-monitor.js"

if not INDEX.exists():
    raise SystemExit(f"ERROR: {INDEX} not found")

if not CSS.exists():
    raise SystemExit(f"ERROR: {CSS} not found")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ------------------------------------------------------------
# BACKUPS
# ------------------------------------------------------------

index_backup = APP / f"index.html.backup_{timestamp}"
css_backup = APP / f"style.css.backup_{timestamp}"

shutil.copy2(INDEX, index_backup)
shutil.copy2(CSS, css_backup)

# ------------------------------------------------------------
# REAL-TIME MONITOR JS
# ------------------------------------------------------------

realtime_js = r'''
(function () {
    "use strict";

    const API = "/api/risk/";

    let previousNodes = {};
    let lastUpdate = null;

    async function get(endpoint) {
        const response = await fetch(API + endpoint, {
            cache: "no-store"
        });

        if (!response.ok) {
            throw new Error(endpoint + " failed: " + response.status);
        }

        const data = await response.json();
        return data.value || data;
    }

    function createMonitor() {
        if (document.getElementById("rtMonitor")) {
            return;
        }

        const monitor = document.createElement("section");

        monitor.id = "rtMonitor";
        monitor.className = "rt-monitor";

        monitor.innerHTML = `
            <div class="rt-header">
                <div>
                    <div class="rt-eyebrow">
                        LIVE NETWORK INTELLIGENCE
                    </div>

                    <h2>Multi-Tier Dependency Network</h2>

                    <p>
                        Real-time supply chain topology and disruption propagation
                    </p>
                </div>

                <div class="rt-live-status">
                    <span class="rt-live-dot"></span>
                    <span>LIVE</span>
                    <small id="rtUpdated">Connecting...</small>
                </div>
            </div>

            <div class="rt-stats">

                <div class="rt-stat">
                    <span>NETWORK NODES</span>
                    <strong id="rtNodeCount">—</strong>
                </div>

                <div class="rt-stat">
                    <span>CONNECTIONS</span>
                    <strong id="rtEdgeCount">—</strong>
                </div>

                <div class="rt-stat danger">
                    <span>IMPACTED</span>
                    <strong id="rtImpacted">—</strong>
                </div>

                <div class="rt-stat warning">
                    <span>INVENTORY COVER</span>
                    <strong id="rtInventory">—</strong>
                </div>

            </div>

            <div class="rt-network">

                <div class="rt-tier-labels">
                    <span>TIER 3</span>
                    <span>TIER 2</span>
                    <span>TIER 1</span>
                    <span>PLANT</span>
                </div>

                <svg id="rtGraph"
                     viewBox="0 0 1200 430"
                     preserveAspectRatio="xMidYMid meet">
                </svg>

            </div>

            <div class="rt-footer">

                <div class="rt-legend">
                    <span>
                        <i class="healthy"></i>
                        Healthy
                    </span>

                    <span>
                        <i class="risk"></i>
                        At Risk
                    </span>

                    <span>
                        <i class="impacted"></i>
                        Impacted
                    </span>
                </div>

                <div class="rt-refresh">
                    Auto-refreshing every 3 seconds
                </div>

            </div>
        `;

        const anchor =
            document.querySelector(".agent-panel") ||
            document.querySelector("#agents") ||
            document.querySelector("main") ||
            document.body;

        if (anchor === document.body) {
            document.body.prepend(monitor);
        } else {
            anchor.parentNode.insertBefore(monitor, anchor);
        }
    }

    function nodeStatus(node) {

        const status =
            String(node.status || "").toUpperCase();

        if (
            status.includes("IMPACT") ||
            status.includes("CRITICAL") ||
            status.includes("DISRUPT")
        ) {
            return "impacted";
        }

        if (
            status.includes("RISK") ||
            status.includes("WARN") ||
            status.includes("HIGH")
        ) {
            return "risk";
        }

        return "healthy";
    }

    function escapeHtml(value) {
        return String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;");
    }

    function buildGraph(nodes, edges) {

        const svg = document.getElementById("rtGraph");

        if (!svg) return;

        const width = 1200;
        const height = 430;

        svg.innerHTML = `
            <defs>

                <filter id="rtGlow">
                    <feGaussianBlur stdDeviation="4"
                                    result="blur"/>
                    <feMerge>
                        <feMergeNode in="blur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>

                <marker id="rtArrow"
                        markerWidth="8"
                        markerHeight="8"
                        refX="7"
                        refY="3"
                        orient="auto">
                    <path d="M0,0 L0,6 L7,3 z"/>
                </marker>

            </defs>
        `;

        const groups = {};

        nodes.forEach(node => {

            const tier =
                Number(node.tier || 1);

            if (!groups[tier]) {
                groups[tier] = [];
            }

            groups[tier].push(node);
        });

        const positions = {};

        const tierX = {
            3: 130,
            2: 410,
            1: 700,
            0: 1010
        };

        Object.keys(groups).forEach(tierKey => {

            const group = groups[tierKey];

            group.forEach((node, index) => {

                const x =
                    tierX[tierKey] ||
                    (130 + Number(tierKey) * 280);

                const gap =
                    height / (group.length + 1);

                const y =
                    gap * (index + 1);

                positions[node.ID || node.id] = {
                    x,
                    y
                };

            });

        });

        // Connections
        edges.forEach(edge => {

            const source =
                positions[
                    edge.sourceNode_ID ||
                    edge.sourceNode ||
                    edge.source
                ];

            const target =
                positions[
                    edge.targetNode_ID ||
                    edge.targetNode ||
                    edge.target
                ];

            if (!source || !target) return;

            const line =
                document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "line"
                );

            line.setAttribute("x1", source.x);
            line.setAttribute("y1", source.y);
            line.setAttribute("x2", target.x);
            line.setAttribute("y2", target.y);

            line.setAttribute("class", "rt-edge");

            svg.appendChild(line);
        });

        // Nodes
        nodes.forEach(node => {

            const id =
                node.ID || node.id;

            const pos = positions[id];

            if (!pos) return;

            const status =
                nodeStatus(node);

            const group =
                document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "g"
                );

            group.setAttribute(
                "class",
                "rt-node-group " + status
            );

            group.setAttribute(
                "transform",
                `translate(${pos.x},${pos.y})`
            );

            const pulse =
                document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "circle"
                );

            pulse.setAttribute("r", "23");
            pulse.setAttribute(
                "class",
                "rt-node-pulse"
            );

            const circle =
                document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "circle"
                );

            circle.setAttribute("r", "15");
            circle.setAttribute(
                "class",
                "rt-node"
            );

            const title =
                document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "text"
                );

            title.setAttribute("y", "42");
            title.setAttribute(
                "class",
                "rt-node-title"
            );

            title.textContent =
                node.name || node.nodeType || "Node";

            const type =
                document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "text"
                );

            type.setAttribute("y", "-28");
            type.setAttribute(
                "class",
                "rt-node-type"
            );

            type.textContent =
                node.nodeType ||
                "NETWORK";

            group.appendChild(pulse);
            group.appendChild(circle);
            group.appendChild(type);
            group.appendChild(title);

            svg.appendChild(group);
        });
    }

    async function refresh() {

        try {

            const [
                nodes,
                edges,
                disruptions,
                inventory
            ] = await Promise.all([
                get("SupplyChainNodes"),
                get("SupplyChainEdges"),
                get("Disruptions"),
                get("Inventory")
            ]);

            createMonitor();

            const impacted =
                nodes.filter(
                    node => nodeStatus(node) === "impacted"
                ).length;

            const risk =
                nodes.filter(
                    node => nodeStatus(node) === "risk"
                ).length;

            document.getElementById("rtNodeCount")
                .textContent = nodes.length;

            document.getElementById("rtEdgeCount")
                .textContent = edges.length;

            document.getElementById("rtImpacted")
                .textContent =
                impacted + risk;

            const stockDays =
                inventory.length
                    ? inventory[0].stockDays
                    : null;

            document.getElementById("rtInventory")
                .textContent =
                stockDays !== null
                    ? Number(stockDays).toFixed(0) + " days"
                    : "—";

            buildGraph(nodes, edges);

            lastUpdate = new Date();

            document.getElementById("rtUpdated")
                .textContent =
                "Updated " +
                lastUpdate.toLocaleTimeString();

            document
                .querySelector(".rt-live-status")
                ?.classList.remove("offline");

            console.log(
                "[RippleTrace] Network refreshed:",
                {
                    nodes: nodes.length,
                    edges: edges.length,
                    impacted,
                    risk
                }
            );

        } catch (error) {

            console.error(
                "[RippleTrace] Live monitor error:",
                error
            );

            const status =
                document.querySelector(
                    ".rt-live-status"
                );

            if (status) {
                status.classList.add("offline");

                const label =
                    status.querySelector("span:nth-child(2)");

                if (label) {
                    label.textContent = "RECONNECTING";
                }
            }
        }
    }

    function start() {

        createMonitor();

        refresh();

        setInterval(
            refresh,
            3000
        );
    }

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            start
        );
    } else {
        start();
    }

})();
'''

REALTIME.write_text(realtime_js)

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------

css = r'''

/* ============================================================
   RIPPLETRACE LIVE NETWORK MONITOR
   UI ONLY — NO BACKEND DEPENDENCIES
   ============================================================ */

.rt-monitor {
    margin: 22px 34px;
    padding: 0;
    overflow: hidden;
    border: 1px solid rgba(120, 140, 160, .24);
    border-radius: 14px;
    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(0, 112, 242, .09),
            transparent 30%
        ),
        linear-gradient(
            145deg,
            #101820,
            #0b1117 70%
        );
    color: #f4f7fa;
    box-shadow:
        0 14px 45px rgba(0,0,0,.16);
}

.rt-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 24px;
    padding: 25px 28px 18px;
}

.rt-eyebrow {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .14em;
    color: #70b7ff;
    margin-bottom: 7px;
}

.rt-header h2 {
    margin: 0;
    font-size: 22px;
    font-weight: 650;
    letter-spacing: -.02em;
}

.rt-header p {
    margin: 7px 0 0;
    color: #91a0ad;
    font-size: 13px;
}

.rt-live-status {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 9px 13px;
    border: 1px solid rgba(45, 220, 130, .25);
    border-radius: 999px;
    background: rgba(30, 180, 100, .08);
    color: #62e6a0;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .08em;
    white-space: nowrap;
}

.rt-live-status small {
    color: #83919d;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0;
}

.rt-live-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #35dc8a;
    box-shadow: 0 0 0 4px rgba(53,220,138,.12);
    animation: rtPulse 1.5s infinite;
}

.rt-live-status.offline {
    color: #ffb15c;
    border-color: rgba(255,177,92,.25);
    background: rgba(255,177,92,.08);
}

.rt-live-status.offline .rt-live-dot {
    background: #ff9f43;
}

.rt-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    margin: 0 20px 18px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 9px;
    background: rgba(255,255,255,.06);
}

.rt-stat {
    padding: 15px 17px;
    background: rgba(255,255,255,.025);
}

.rt-stat span {
    display: block;
    color: #7e8c98;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: .1em;
}

.rt-stat strong {
    display: block;
    margin-top: 6px;
    font-size: 22px;
    font-weight: 650;
}

.rt-stat.danger strong {
    color: #ff7676;
}

.rt-stat.warning strong {
    color: #ffbf69;
}

.rt-network {
    position: relative;
    margin: 0 20px;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 10px;
    background:
        linear-gradient(
            rgba(255,255,255,.025) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(255,255,255,.025) 1px,
            transparent 1px
        );
    background-size: 32px 32px;
    overflow: hidden;
}

.rt-network svg {
    display: block;
    width: 100%;
    min-height: 390px;
}

.rt-tier-labels {
    position: absolute;
    top: 14px;
    left: 0;
    right: 0;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    pointer-events: none;
    z-index: 2;
}

.rt-tier-labels span {
    text-align: center;
    color: #53616d;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: .12em;
}

.rt-edge {
    stroke: #536575;
    stroke-width: 1.5;
    stroke-dasharray: 5 6;
    opacity: .55;
    animation: rtFlow 1.8s linear infinite;
}

.rt-node {
    stroke-width: 2;
    filter: url(#rtGlow);
}

.rt-node-pulse {
    fill: none;
    stroke-width: 1;
    opacity: .25;
    animation: rtNodePulse 2.2s infinite;
}

.rt-node-group.healthy .rt-node {
    fill: #1d9c65;
    stroke: #66e3aa;
}

.rt-node-group.healthy .rt-node-pulse {
    stroke: #44d993;
}

.rt-node-group.risk .rt-node {
    fill: #b86d17;
    stroke: #ffc064;
}

.rt-node-group.risk .rt-node-pulse {
    stroke: #ffb54d;
}

.rt-node-group.impacted .rt-node {
    fill: #b72d35;
    stroke: #ff7777;
}

.rt-node-group.impacted .rt-node-pulse {
    stroke: #ff5c66;
}

.rt-node-title {
    fill: #dbe4eb;
    text-anchor: middle;
    font-size: 12px;
    font-weight: 650;
}

.rt-node-type {
    fill: #647582;
    text-anchor: middle;
    font-size: 8px;
    font-weight: 800;
    letter-spacing: 1px;
}

.rt-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 22px 19px;
}

.rt-legend {
    display: flex;
    gap: 18px;
    color: #8b99a5;
    font-size: 10px;
}

.rt-legend span {
    display: flex;
    align-items: center;
    gap: 6px;
}

.rt-legend i {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
}

.rt-legend i.healthy {
    background: #45d995;
}

.rt-legend i.risk {
    background: #ffb24e;
}

.rt-legend i.impacted {
    background: #ff666f;
}

.rt-refresh {
    color: #5e6c78;
    font-size: 10px;
}

@keyframes rtPulse {
    0%, 100% {
        opacity: 1;
    }

    50% {
        opacity: .35;
    }
}

@keyframes rtFlow {
    to {
        stroke-dashoffset: -22;
    }
}

@keyframes rtNodePulse {
    0% {
        transform: scale(.65);
        opacity: .4;
    }

    70%, 100% {
        transform: scale(1.4);
        opacity: 0;
    }
}

@media (max-width: 900px) {

    .rt-monitor {
        margin: 15px;
    }

    .rt-header {
        align-items: flex-start;
        flex-direction: column;
    }

    .rt-stats {
        grid-template-columns: repeat(2, 1fr);
    }

    .rt-network svg {
        min-height: 320px;
    }
}

@media (max-width: 600px) {

    .rt-stats {
        grid-template-columns: 1fr;
    }

    .rt-footer {
        align-items: flex-start;
        flex-direction: column;
        gap: 12px;
    }

}
'''

with CSS.open("a") as f:
    f.write(css)

# ------------------------------------------------------------
# INDEX — ONLY ADD SCRIPT REFERENCE
# ------------------------------------------------------------

index = INDEX.read_text()

script_tag = '<script src="realtime-monitor.js"></script>'

if "realtime-monitor.js" not in index:

    if "</body>" in index:
        index = index.replace(
            "</body>",
            f"    {script_tag}\n</body>"
        )

    else:
        index += "\n" + script_tag + "\n"

    INDEX.write_text(index)

print()
print("=" * 64)
print("        RippleTrace UI Polish Complete")
print("=" * 64)
print()
print("UI changes:")
print("  ✓ Live multi-tier network monitor")
print("  ✓ Auto-refresh every 3 seconds")
print("  ✓ Animated dependency connections")
print("  ✓ Live node health states")
print("  ✓ Impacted / risk counters")
print("  ✓ Inventory coverage indicator")
print("  ✓ Last-updated timestamp")
print("  ✓ Enterprise command-center styling")
print()
print("Backend:")
print("  ✓ NOT MODIFIED")
print("  ✓ CDS schema NOT MODIFIED")
print("  ✓ Agents NOT MODIFIED")
print("  ✓ Database NOT MODIFIED")
print("  ✓ API actions NOT MODIFIED")
print("  ✓ Approval logic NOT MODIFIED")
print()
print("Frontend files changed:")
print("  • index.html")
print("  • css/style.css")
print("  • realtime-monitor.js")
print()
print("Backups:")
print(f"  • {index_backup.name}")
print(f"  • {css_backup.name}")
print()
print("Restart cds watch and hard-refresh the browser.")
print("=" * 64)
