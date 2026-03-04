from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
from docx2pdf import convert
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def form():
    return render_template("form.html")

@app.route('/generate', methods=['POST'])
def generate():

    principal = request.form.get("principal")
    surveyor = request.form.get("surveyor")
    vessel = request.form.get("vessel").upper()
    port = request.form.get("port")
    job_scope = request.form.get("job_scope").upper()
    survey_date = request.form.get("survey_date")

    owner = request.form.get("owner").upper()
    charterer = request.form.get("charterer").upper()
    chief_engineer = request.form.get("chief_engineer").upper()
    master = request.form.get("master").upper()

    bunker1_supply = request.form.get("bunker1_supply")
    bunker2_supply = request.form.get("bunker2_supply")

    bunker1_sentence = ""
    bunker2_sentence = ""

    if bunker1_supply == "yes":
        bunker1_sentence = f"The bunker transferring of {request.form.get('bunker1_name')} commenced at {request.form.get('bunker1_commenced_hour')} on {request.form.get('bunker1_commenced_date')} and completed at {request.form.get('bunker1_completed_hour')} on {request.form.get('bunker1_completed_date')}."

    if bunker2_supply == "yes":
        bunker2_sentence = f"The bunker transferring of {request.form.get('bunker2_name')} commenced at {request.form.get('bunker2_commenced_hour')} on {request.form.get('bunker2_commenced_date')} and completed at {request.form.get('bunker2_completed_hour')} on {request.form.get('bunker2_completed_date')}."

    context = {
        "principal": principal,
        "surveyor": surveyor,
        "vessel": vessel,
        "port": port,
        "job_scope": job_scope,
        "survey_date": survey_date,
        "owner": owner,
        "charterer": charterer,
        "chief_engineer": chief_engineer,
        "master": master,
        "bunker1_sentence": bunker1_sentence,
        "bunker2_sentence": bunker2_sentence,
        "issue_date": datetime.today().strftime("%d/%m/%Y")
    }

    template = DocxTemplate("template.docx")
    template.render(context)

    output_docx = "report.docx"
    template.save(output_docx)

    export_type = request.form.get("export_type")

    if export_type == "word":
        return send_file(output_docx, as_attachment=True)

    output_pdf = "report.pdf"
    convert(output_docx, output_pdf)

    return send_file(output_pdf, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)