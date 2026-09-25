const cds = require('@sap/cds');

const runCascadeAgent = require('./cascade-agent');

module.exports = async function runPredictionAgent(disruptionId) {

    const db = await cds.connect.to('db');

    const {
        Inventory,
        Components,
        Factories
    } = cds.entities('rippletrace');

    // Run Cascade Agent first
    const cascade = await runCascadeAgent(disruptionId);

    // Find affected component
    const componentNode = cascade.affectedNodes.find(
        node => node.nodeType === 'COMPONENT'
    );

    // Find affected factory
    const factoryNode = cascade.affectedNodes.find(
        node => node.nodeType === 'FACTORY'
    );

    if (!componentNode || !factoryNode) {
        throw new Error(
            'Could not identify affected component or factory'
        );
    }

    // Find component in database
    const component = await db.run(
        SELECT.one.from(Components).where({
            name: componentNode.name
        })
    );

    // Find factory in database
    const factory = await db.run(
        SELECT.one.from(Factories).where({
            name: factoryNode.name
        })
    );

    if (!component || !factory) {
        throw new Error(
            'Component or factory not found in database'
        );
    }

    // Find inventory record
    const inventory = await db.run(
        SELECT.one.from(Inventory).where({
            component_ID: component.ID,
            factory_ID: factory.ID
        })
    );

    if (!inventory) {
        throw new Error(
            'Inventory record not found'
        );
    }

    const stockDays = Number(inventory.stockDays);
    const leadTimeDays = Number(inventory.normalLeadTimeDays);

    // Calculate stockout exposure
    const stockoutGapDays = Math.max(
        0,
        leadTimeDays - stockDays
    );

    // Determine risk level
    let riskLevel = 'LOW';

    if (stockoutGapDays >= 7) {
        riskLevel = 'HIGH';
    } else if (stockoutGapDays > 0) {
        riskLevel = 'MEDIUM';
    }

    return {
        disruption: cascade.disruption,

        impact: {
            component: component.name,
            factory: factory.name,
            inventoryDays: stockDays,
            normalLeadTimeDays: leadTimeDays,
            stockoutGapDays: stockoutGapDays,
            riskLevel: riskLevel
        },

        affectedNodes: cascade.affectedNodes
    };
};
