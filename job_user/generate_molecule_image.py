from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import DrawingOptions
from job_user.models import *
from accounts.models import *
import os

DrawingOptions.atomLabelFontSize = 55
DrawingOptions.dotsPerAngstrom = 100
DrawingOptions.bondLineWidth = 3.0


def fn_generate_mocule_image(job_pk):
    job_data = Job.objects.get(pk=job_pk)
    os.makedirs('static/smiles/userpk'+str(job_data.user_id), exist_ok=True)
    fname ='static/smiles/userpk'+str(job_data.user_id)+'/jobpk'+str(job_data.pk)+'.png'
    print(fname)
    mol = Chem.MolFromSmiles( job_data.smiles )
    Draw.MolToFile( mol, fname)
