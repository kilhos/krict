from django.http import FileResponse
from reportlab.pdfbase.ttfonts import TTFont

from job_user.calculate_property import prediction
from job_user.models import *
import io, datetime
from reportlab.pdfgen import canvas


def fn_chemtrans_report(pk):
    job_res_list = JobResult.objects.get(pk=pk)
    job_list = job_res_list.job
    user_list = job_list.user
    module_list = job_list.module_api.module
    module_api_list = job_list.module_api
    buffer = io.BytesIO()
    canvas.pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    canvas.pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    canvas.pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    canvas.pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    p = canvas.Canvas(buffer)
    pdf_name = job_list.job_name
    if pdf_name == '':
        pdf_name = 'no_name'
    p.setLineWidth(.1)
    p.setFont('Helvetica', 22)
    p.drawString(20, 750, pdf_name)

    p.setFont('Helvetica-Bold', 12)
    p.drawString(440, 759, 'Writer : ' + user_list.name)
    p.drawString(440, 739, 'Report Date : ' + str(datetime.datetime.now().strftime('%Y-%m-%d')))
    p.line(425, 729, 600, 729)

    p.setFont('Helvetica', 14)
    p.drawString(20, 700, 'Job Description')

    p.setFont('Helvetica', 8)
    p.drawString(20, 680, 'Module used : ' + module_list.module_name)
    p.drawString(20, 670, 'Usage module API : ' + str(module_api_list.module_api_name))
    p.drawString(20, 660, 'Job Explanation : ' + job_list.job_explanation)

    p.setFont('Helvetica', 14)
    p.drawString(20, 640, 'Job Data')

    p.setFont('Helvetica', 8)
    p.drawString(20, 620, 'Job Smiles : ' + job_list.smiles)

    img_path = settings.BASE_DIR + '/static/smiles/userpk' + str(job_list.user_id) + '/jobpk' + str(
        job_list.pk) + '.png'
    mask = [0, 0, 0, 0, 0, 0]
    p.drawImage(img_path, x=400, y=560, width=100, height=100, mask=mask)
    smiles_detail = prediction(job_list.smiles)
    p.drawString(20, 610, 'Molecular weight : ' + str(smiles_detail['weight']))
    p.drawString(20, 600, 'LogP : ' + str(smiles_detail['logp']))
    p.drawString(20, 590, 'H-Bond Acceptor : ' + str(smiles_detail['numH']))
    p.drawString(20, 580, 'H-Bond Dornor : ' + str(smiles_detail['numHD']))
    p.drawString(20, 570, 'Rotatable Bond : ' + str(smiles_detail['numR']))
    p.drawString(20, 560, 'QED (drug likeness) : ' + str(round(smiles_detail['qed'], 3)))

    p.setFont('Helvetica', 14)
    p.drawString(20, 530, 'Job Result')

    p.setFont('Helvetica', 7)
    p.drawString(20, 509, 'Elapsed Time : ' + str(round(float(job_res_list.result_json['time']), 1)))

    if 'CID1' in job_res_list.result_json:
        p.drawString(20, 500, 'CID1 : ' + str(job_res_list.result_json['CID1']))
    if 'CID2' in job_res_list.result_json:
        p.drawString(310, 500, 'CID2 : ' + str(job_res_list.result_json['CID2']))
    if 'CID3' in job_res_list.result_json:
        p.drawString(20, 491, 'CID3 : ' + str(job_res_list.result_json['CID3']))
    if 'CID4' in job_res_list.result_json:
        p.drawString(310, 491, 'CID4 : ' + str(job_res_list.result_json['CID4']))
    if 'CID5' in job_res_list.result_json:
        p.drawString(20, 482, 'CID5 : ' + str(job_res_list.result_json['CID5']))
    if 'CID6' in job_res_list.result_json:
        p.drawString(310, 482, 'CID6 : ' + str(job_res_list.result_json['CID6']))
    if 'CID7' in job_res_list.result_json:
        p.drawString(20, 473, 'CID7 : ' + str(job_res_list.result_json['CID7']))
    if 'CID8' in job_res_list.result_json:
        p.drawString(310, 473, 'CID8 : ' + str(job_res_list.result_json['CID8']))
    if 'CID9' in job_res_list.result_json:
        p.drawString(20, 464, 'CID9 : ' + str(job_res_list.result_json['CID9']))
    if 'CID10' in job_res_list.result_json:
        p.drawString(310, 464, 'CID10 : ' + str(job_res_list.result_json['CID10']))
    if 'CID11' in job_res_list.result_json:
        p.drawString(20, 455, 'CID11 : ' + str(job_res_list.result_json['CID11']))
    if 'CID12' in job_res_list.result_json:
        p.drawString(310, 455, 'CID12 : ' + str(job_res_list.result_json['CID12']))
    if 'CID13' in job_res_list.result_json:
        p.drawString(20, 446, 'CID13 : ' + str(job_res_list.result_json['CID13']))
    if 'CID14' in job_res_list.result_json:
        p.drawString(310, 446, 'CID14 : ' + str(job_res_list.result_json['CID14']))
    if 'CID15' in job_res_list.result_json:
        p.drawString(20, 437, 'CID15 : ' + str(job_res_list.result_json['CID15']))
    if 'CID16' in job_res_list.result_json:
        p.drawString(310, 437, 'CID16 : ' + str(job_res_list.result_json['CID16']))
    if 'CID17' in job_res_list.result_json:
        p.drawString(20, 428, 'CID17 : ' + str(job_res_list.result_json['CID17']))
    if 'CID18' in job_res_list.result_json:
        p.drawString(310, 428, 'CID18 : ' + str(job_res_list.result_json['CID18']))
    if 'CID19' in job_res_list.result_json:
        p.drawString(20, 419, 'CID19 : ' + str(job_res_list.result_json['CID19']))
    if 'CID20' in job_res_list.result_json:
        p.drawString(310, 419, 'CID20 : ' + str(job_res_list.result_json['CID20']))
    if 'CID21' in job_res_list.result_json:
        p.drawString(20, 410, 'CID21 : ' + str(job_res_list.result_json['CID21']))
    if 'CID22' in job_res_list.result_json:
        p.drawString(310, 410, 'CID22 : ' + str(job_res_list.result_json['CID22']))
    if 'CID23' in job_res_list.result_json:
        p.drawString(20, 401, 'CID23 : ' + str(job_res_list.result_json['CID23']))
    if 'CID24' in job_res_list.result_json:
        p.drawString(310, 401, 'CID24 : ' + str(job_res_list.result_json['CID24']))
    if 'CID25' in job_res_list.result_json:
        p.drawString(20, 392, 'CID25 : ' + str(job_res_list.result_json['CID25']))
    if 'CID26' in job_res_list.result_json:
        p.drawString(310, 392, 'CID26 : ' + str(job_res_list.result_json['CID26']))
    if 'CID27' in job_res_list.result_json:
        p.drawString(20, 383, 'CID27 : ' + str(job_res_list.result_json['CID27']))
    if 'CID28' in job_res_list.result_json:
        p.drawString(310, 383, 'CID28 : ' + str(job_res_list.result_json['CID28']))
    if 'CID29' in job_res_list.result_json:
        p.drawString(20, 374, 'CID29 : ' + str(job_res_list.result_json['CID29']))
    if 'CID30' in job_res_list.result_json:
        p.drawString(310, 374, 'CID30 : ' + str(job_res_list.result_json['CID30']))
    if 'CID31' in job_res_list.result_json:
        p.drawString(20, 365, 'CID31 : ' + str(job_res_list.result_json['CID31']))
    if 'CID32' in job_res_list.result_json:
        p.drawString(310, 365, 'CID32 : ' + str(job_res_list.result_json['CID32']))
    if 'CID33' in job_res_list.result_json:
        p.drawString(20, 356, 'CID33 : ' + str(job_res_list.result_json['CID33']))
    if 'CID34' in job_res_list.result_json:
        p.drawString(310, 356, 'CID34 : ' + str(job_res_list.result_json['CID34']))
    if 'CID35' in job_res_list.result_json:
        p.drawString(20, 347, 'CID35 : ' + str(job_res_list.result_json['CID35']))
    if 'CID36' in job_res_list.result_json:
        p.drawString(310, 347, 'CID36 : ' + str(job_res_list.result_json['CID36']))
    if 'CID37' in job_res_list.result_json:
        p.drawString(20, 338, 'CID37 : ' + str(job_res_list.result_json['CID37']))
    if 'CID38' in job_res_list.result_json:
        p.drawString(310, 338, 'CID38 : ' + str(job_res_list.result_json['CID38']))
    if 'CID39' in job_res_list.result_json:
        p.drawString(20, 329, 'CID39 : ' + str(job_res_list.result_json['CID39']))
    if 'CID40' in job_res_list.result_json:
        p.drawString(310, 329, 'CID40 : ' + str(job_res_list.result_json['CID40']))
    if 'CID41' in job_res_list.result_json:
        p.drawString(20, 320, 'CID41 : ' + str(job_res_list.result_json['CID41']))
    if 'CID42' in job_res_list.result_json:
        p.drawString(310, 320, 'CID42 : ' + str(job_res_list.result_json['CID42']))
    if 'CID43' in job_res_list.result_json:
        p.drawString(20, 311, 'CID43 : ' + str(job_res_list.result_json['CID43']))
    if 'CID44' in job_res_list.result_json:
        p.drawString(310, 311, 'CID44 : ' + str(job_res_list.result_json['CID44']))
    if 'CID45' in job_res_list.result_json:
        p.drawString(20, 302, 'CID45 : ' + str(job_res_list.result_json['CID45']))
    if 'CID46' in job_res_list.result_json:
        p.drawString(310, 302, 'CID46 : ' + str(job_res_list.result_json['CID46']))
    if 'CID47' in job_res_list.result_json:
        p.drawString(20, 293, 'CID47 : ' + str(job_res_list.result_json['CID47']))
    if 'CID48' in job_res_list.result_json:
        p.drawString(310, 293, 'CID48 : ' + str(job_res_list.result_json['CID48']))
    if 'CID49' in job_res_list.result_json:
        p.drawString(20, 284, 'CID49 : ' + str(job_res_list.result_json['CID49']))
    if 'CID50' in job_res_list.result_json:
        p.drawString(310, 284, 'CID50 : ' + str(job_res_list.result_json['CID50']))
    if 'CID51' in job_res_list.result_json:
        p.drawString(20, 275, 'CID51 : ' + str(job_res_list.result_json['CID51']))
    if 'CID52' in job_res_list.result_json:
        p.drawString(310, 275, 'CID52 : ' + str(job_res_list.result_json['CID52']))
    if 'CID53' in job_res_list.result_json:
        p.drawString(20, 266, 'CID53 : ' + str(job_res_list.result_json['CID53']))
    if 'CID54' in job_res_list.result_json:
        p.drawString(310, 266, 'CID54 : ' + str(job_res_list.result_json['CID54']))
    if 'CID55' in job_res_list.result_json:
        p.drawString(20, 257, 'CID55 : ' + str(job_res_list.result_json['CID55']))
    if 'CID56' in job_res_list.result_json:
        p.drawString(310, 257, 'CID56 : ' + str(job_res_list.result_json['CID56']))
    if 'CID57' in job_res_list.result_json:
        p.drawString(20, 248, 'CID57 : ' + str(job_res_list.result_json['CID57']))
    if 'CID58' in job_res_list.result_json:
        p.drawString(310, 248, 'CID58 : ' + str(job_res_list.result_json['CID58']))
    if 'CID59' in job_res_list.result_json:
        p.drawString(20, 239, 'CID59 : ' + str(job_res_list.result_json['CID59']))
    if 'CID60' in job_res_list.result_json:
        p.drawString(310, 239, 'CID60 : ' + str(job_res_list.result_json['CID60']))
    if 'CID61' in job_res_list.result_json:
        p.drawString(20, 230, 'CID61 : ' + str(job_res_list.result_json['CID61']))
    if 'CID62' in job_res_list.result_json:
        p.drawString(310, 230, 'CID62 : ' + str(job_res_list.result_json['CID62']))
    if 'CID63' in job_res_list.result_json:
        p.drawString(20, 221, 'CID63 : ' + str(job_res_list.result_json['CID63']))
    if 'CID64' in job_res_list.result_json:
        p.drawString(310, 221, 'CID64 : ' + str(job_res_list.result_json['CID64']))
    if 'CID65' in job_res_list.result_json:
        p.drawString(20, 212, 'CID65 : ' + str(job_res_list.result_json['CID65']))
    if 'CID66' in job_res_list.result_json:
        p.drawString(310, 212, 'CID66 : ' + str(job_res_list.result_json['CID66']))
    if 'CID67' in job_res_list.result_json:
        p.drawString(20, 203, 'CID67 : ' + str(job_res_list.result_json['CID67']))
    if 'CID68' in job_res_list.result_json:
        p.drawString(310, 203, 'CID68 : ' + str(job_res_list.result_json['CID68']))
    if 'CID69' in job_res_list.result_json:
        p.drawString(20, 194, 'CID69 : ' + str(job_res_list.result_json['CID69']))
    if 'CID70' in job_res_list.result_json:
        p.drawString(310, 194, 'CID70 : ' + str(job_res_list.result_json['CID70']))
    if 'CID71' in job_res_list.result_json:
        p.drawString(20, 185, 'CID71 : ' + str(job_res_list.result_json['CID71']))
    if 'CID72' in job_res_list.result_json:
        p.drawString(310, 185, 'CID72 : ' + str(job_res_list.result_json['CID72']))
    if 'CID73' in job_res_list.result_json:
        p.drawString(20, 176, 'CID73 : ' + str(job_res_list.result_json['CID73']))
    if 'CID74' in job_res_list.result_json:
        p.drawString(310, 176, 'CID74 : ' + str(job_res_list.result_json['CID74']))
    if 'CID75' in job_res_list.result_json:
        p.drawString(20, 167, 'CID75 : ' + str(job_res_list.result_json['CID75']))
    if 'CID76' in job_res_list.result_json:
        p.drawString(310, 167, 'CID76 : ' + str(job_res_list.result_json['CID76']))
    if 'CID77' in job_res_list.result_json:
        p.drawString(20, 158, 'CID77 : ' + str(job_res_list.result_json['CID77']))
    if 'CID78' in job_res_list.result_json:
        p.drawString(310, 158, 'CID78 : ' + str(job_res_list.result_json['CID78']))
    if 'CID79' in job_res_list.result_json:
        p.drawString(20, 149, 'CID79 : ' + str(job_res_list.result_json['CID79']))
    if 'CID80' in job_res_list.result_json:
        p.drawString(310, 149, 'CID80 : ' + str(job_res_list.result_json['CID80']))
    if 'CID81' in job_res_list.result_json:
        p.drawString(20, 140, 'CID81 : ' + str(job_res_list.result_json['CID81']))
    if 'CID82' in job_res_list.result_json:
        p.drawString(310, 140, 'CID82 : ' + str(job_res_list.result_json['CID82']))
    if 'CID83' in job_res_list.result_json:
        p.drawString(20, 131, 'CID83 : ' + str(job_res_list.result_json['CID83']))
    if 'CID84' in job_res_list.result_json:
        p.drawString(310, 131, 'CID84 : ' + str(job_res_list.result_json['CID84']))
    if 'CID85' in job_res_list.result_json:
        p.drawString(20, 122, 'CID85 : ' + str(job_res_list.result_json['CID85']))
    if 'CID86' in job_res_list.result_json:
        p.drawString(310, 122, 'CID86 : ' + str(job_res_list.result_json['CID86']))
    if 'CID87' in job_res_list.result_json:
        p.drawString(20, 113, 'CID87 : ' + str(job_res_list.result_json['CID87']))
    if 'CID88' in job_res_list.result_json:
        p.drawString(310, 113, 'CID88 : ' + str(job_res_list.result_json['CID88']))
    if 'CID89' in job_res_list.result_json:
        p.drawString(20, 104, 'CID89 : ' + str(job_res_list.result_json['CID89']))
    if 'CID90' in job_res_list.result_json:
        p.drawString(310, 104, 'CID90 : ' + str(job_res_list.result_json['CID90']))
    if 'CID91' in job_res_list.result_json:
        p.drawString(20, 95, 'CID91 : ' + str(job_res_list.result_json['CID91']))
    if 'CID92' in job_res_list.result_json:
        p.drawString(310, 95, 'CID92 : ' + str(job_res_list.result_json['CID92']))
    if 'CID93' in job_res_list.result_json:
        p.drawString(20, 86, 'CID93 : ' + str(job_res_list.result_json['CID93']))
    if 'CID94' in job_res_list.result_json:
        p.drawString(310, 86, 'CID94 : ' + str(job_res_list.result_json['CID94']))
    if 'CID95' in job_res_list.result_json:
        p.drawString(20, 77, 'CID95 : ' + str(job_res_list.result_json['CID95']))
    if 'CID96' in job_res_list.result_json:
        p.drawString(310, 77, 'CID96 : ' + str(job_res_list.result_json['CID96']))
    if 'CID97' in job_res_list.result_json:
        p.drawString(20, 68, 'CID97 : ' + str(job_res_list.result_json['CID97']))
    if 'CID98' in job_res_list.result_json:
        p.drawString(310, 68, 'CID98 : ' + str(job_res_list.result_json['CID98']))
    if 'CID99' in job_res_list.result_json:
        p.drawString(20, 59, 'CID99 : ' + str(job_res_list.result_json['CID99']))
    if 'CID100' in job_res_list.result_json:
        p.drawString(310, 59, 'CID100 : ' + str(job_res_list.result_json['CID100']))

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='' + pdf_name + '.pdf')
