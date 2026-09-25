const cds = require('@sap/cds');

module.exports = async function runCascadeAgent(disruptionId) {

    const db = await cds.connect.to('db');

    const {
        Disruptions,
        SupplyChainNodes,
        SupplyChainEdges
    } = cds.entities('rippletrace');

    // 1. Find the disruption
    const disruption = await db.run(
        SELECT.one.from(Disruptions).where({
            ID: disruptionId
        })
    );

    if (!disruption) {
        throw new Error(`Disruption ${disruptionId} not found`);
    }

    // 2. Find the node where disruption occurred
    const portNode = await db.run(
        SELECT.one.from(SupplyChainNodes).where({
            name: disruption.location
        })
    );

    if (!portNode) {
        throw new Error(
            `No supply-chain node found for ${disruption.location}`
        );
    }

    // 3. Traverse the graph
    const affected = [];
    const visited = new Set();

    async function traverse(nodeId) {

        if (visited.has(nodeId)) {
            return;
        }

        visited.add(nodeId);

        const node = await db.run(
            SELECT.one.from(SupplyChainNodes).where({
                ID: nodeId
            })
        );

        if (node) {
            affected.push({
                id: node.ID,
                name: node.name,
                nodeType: node.nodeType,
                tier: node.tier,
                confidence: Number(node.confidence),
                status: node.status
            });
        }

        // Find outgoing relationships
        const edges = await db.run(
            SELECT.from(SupplyChainEdges).where({
                sourceNode_ID: nodeId
            })
        );

        for (const edge of edges) {
            await traverse(edge.targetNode_ID);
        }
    }

    await traverse(portNode.ID);

    return {
        disruption: {
            id: disruption.ID,
            type: disruption.type,
            location: disruption.location,
            severity: disruption.severity,
            delayDays: Number(disruption.delayDays)
        },

        affectedCount: affected.length,

        affectedNodes: affected
    };
};
