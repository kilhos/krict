from rdkit.Chem.Crippen import MolLogP
from rdkit.Chem.Descriptors import qed
from rdkit.Chem.Descriptors import ExactMolWt
import json
import rdkit
from rdkit import Chem


def prediction(smiles):
    mol = Chem.MolFromSmiles(smiles)
    qed_score = qed(mol)
    logp_score = MolLogP(mol)
    weight = ExactMolWt(mol)
    num_h_acceptors = Chem.Lipinski.NumHAcceptors(mol)
    num_h_donors = Chem.Lipinski.NumHDonors(mol)
    num_rotatable_bonds = Chem.Lipinski.NumRotatableBonds(mol)
    
    property_info = {}
    property_info['weight'] = weight
    property_info['logp'] = logp_score
    property_info['numH'] = num_h_acceptors
    property_info['numHD'] = num_h_donors
    property_info['numR'] = num_rotatable_bonds
    property_info['qed'] = qed_score
    return property_info

#smiles = 'Cc1cn2c(n1)CCC(NC(=O)Cc1c(C)noc1Cl)C2'
#property_info = prediction(smiles)
#print (property_info)