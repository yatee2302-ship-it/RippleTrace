using rippletrace as db from '../db/schema';

@path: '/api/risk'
service RiskService {

    entity Suppliers          as projection on db.Suppliers;
    entity Components         as projection on db.Components;
    entity Factories          as projection on db.Factories;
    entity Dependencies       as projection on db.Dependencies;
    entity Inventory          as projection on db.Inventory;
    entity Disruptions        as projection on db.Disruptions;
    entity AlternateSuppliers as projection on db.AlternateSuppliers;
    entity RiskAssessments    as projection on db.RiskAssessments;
    entity Decisions          as projection on db.Decisions;

    entity SupplyChainNodes   as projection on db.SupplyChainNodes;
    entity SupplyChainEdges   as projection on db.SupplyChainEdges;

    action triggerCascade(disruptionId: String) returns String;
    action triggerPrediction(disruptionId: String) returns String;
    action triggerMitigation(disruptionId: String) returns String;
    action triggerSafeguard(disruptionId: String) returns String;
    action approveDecision(decisionId: String, approved: Boolean) returns String;
}
