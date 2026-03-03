from flask import Flask, render_template, request, send_file
from weasyprint import HTML
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():

    # General Info
    vessel = request.form.get('vessel')
    principal = request.form.get('principal')
    port = request.form.get('port')
    job_scope = request.form.get('job_scope')
    surveyor = request.form.get('surveyor')
    date = request.form.get('date')
    owner = request.form.get('owner')
    charterer = request.form.get('charterer')
    chief_engineer = request.form.get('chief_engineer')
    master = request.form.get('master')
    comments = request.form.get('comments')

    # Bunker 1 Quantities
    bdr1 = float(request.form.get('bdr1') or 0)
    barge1 = float(request.form.get('barge1') or 0)
    received1 = float(request.form.get('received1') or 0)
    nominated1 = float(request.form.get('nominated1') or 0)

    # Auto differences
    diff21_1 = round(barge1 - bdr1, 3)
    diff31_1 = round(received1 - bdr1, 3)
    diff41_1 = round(nominated1 - bdr1, 3)

    # Determine more/less
    def more_less(value):
        return "more" if value > 0 else "less"

    html = render_template(
        "report_template.html",
        vessel=vessel,
        principal=principal,
        port=port,
        job_scope=job_scope,
        surveyor=surveyor,
        date=date,
        owner=owner,
        charterer=charterer,
        chief_engineer=chief_engineer,
        master=master,
        comments=comments,
        bdr1=bdr1,
        barge1=barge1,
        received1=received1,
        nominated1=nominated1,
        diff21_1=abs(diff21_1),
        diff31_1=abs(diff31_1),
        diff41_1=abs(diff41_1),
        diff21_type=more_less(diff21_1),
        diff31_type=more_less(diff31_1),
        diff41_type=more_less(diff41_1),
        issue_date=datetime.today().strftime('%d/%m/%Y')
    )

    pdf_path = f"Summary_Report_{vessel}.pdf"
    HTML(string=html, base_url=request.host_url).write_pdf(pdf_path)

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)