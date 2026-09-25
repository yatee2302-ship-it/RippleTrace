
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
