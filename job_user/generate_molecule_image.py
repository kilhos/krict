from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import DrawingOptions
from job_user.models import *
from accounts.models import *
import os

DrawingOptions.atomLabelFontSize = 55
DrawingOptions.dotsPerAngstrom = 100
DrawingOptions.bondLineWidth = 3.0


def make_smile_image(job_pk):
    job_data = Job.objects.get(pk=job_pk)
    os.makedirs(f'static/smiles/userpk{job_data.user_id}', exist_ok=True)
    Draw.MolToFile(Chem.MolFromSmiles(job_data.smiles), f'static/smiles/userpk{job_data.user_id}/jobpk{job_data.pk}.png')
