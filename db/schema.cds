namespace rippletrace;

using { cuid, managed } from '@sap/cds/common';

entity Suppliers : cuid, managed {
    name        : String(100);
    tier        : Integer;
    location    : String(100);
    country     : String(100);
    status      : String(30);
    confidence  : Decimal(5,2);
}

entity Components : cuid, managed {
    name        : String(100);
    criticality : String(30);
}

entity Factories : cuid, managed {
    name        : String(100);
    location    : String(100);
    country     : String(100);
}

entity Dependencies : cuid, managed {
    source      : Association to Suppliers;
    target      : Association to Suppliers;
    component   : Association to Components;
    relation    : String(50);
    evidence    : String(100);
    status      : String(30);
    confidence  : Decimal(5,2);
}

entity Inventory : cuid, managed {
    factory             : Association to Factories;
    component           : Association to Components;
    stockDays           : Decimal(10,2);
    dailyDemand         : Decimal(10,2);
    normalLeadTimeDays  : Decimal(10,2);
}

entity Disruptions : cuid, managed {
    type        : String(50);
    location    : String(100);
    severity    : String(30);
    delayDays   : Decimal(10,2);
    description : String(500);
    active      : Boolean default true;
}

entity AlternateSuppliers : cuid, managed {
    supplier    : Association to Suppliers;
    component   : Association to Components;
    leadTimeDays: Decimal(10,2);
    costIndex   : Decimal(10,2);
    riskLevel   : String(30);
    preVetted   : Boolean default false;
}

entity RiskAssessments : cuid, managed {
    disruption      : Association to Disruptions;
    component       : Association to Components;
    factory         : Association to Factories;
    riskScore       : Decimal(5,2);
    stockoutGapDays : Decimal(10,2);
    confidence      : Decimal(5,2);
    status          : String(30);
}

entity Decisions : cuid, managed {
    risk            : Association to RiskAssessments;
    recommendation  : String(500);
    alternate       : Association to AlternateSuppliers;
    status          : String(30);
    humanApproved   : Boolean default false;
}
entity SupplyChainNodes : cuid, managed {
    nodeType    : String(30);
    name        : String(100);
    tier        : Integer;
    location    : String(100);
    status      : String(30);
    confidence  : Decimal(5,2);
}

entity SupplyChainEdges : cuid, managed {
    sourceNode      : Association to SupplyChainNodes;
    targetNode      : Association to SupplyChainNodes;
    relationship    : String(50);
    evidence        : String(100);
    status          : String(30);
    confidence      : Decimal(5,2);
}
