from flask import Flask, render_template, request, send_file
from weasyprint import HTML
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():

    data = {
        "job_scope": request.form.get("job_scope", ""),
        "vessel": request.form.get("vessel", ""),
        "principal": request.form.get("principal", ""),
        "surveyor": request.form.get("surveyor", ""),
        "port": request.form.get("port", ""),
        "survey_date": request.form.get("survey_date", ""),
        "owner": request.form.get("owner", ""),
        "charterer": request.form.get("charterer", ""),
        "chief_engineer": request.form.get("chief_engineer", ""),
        "master": request.form.get("master", ""),
        "bunker1_supply": request.form.get("bunker1_supply") or "",
        "bunker1_name": request.form.get("bunker1_name", ""),
        "bunker1_commenced_hour": request.form.get("bunker1_commenced_hour", ""),
        "bunker1_commenced_date": request.form.get("bunker1_commenced_date", ""),
        "bunker1_completed_hour": request.form.get("bunker1_completed_hour", ""),
        "bunker1_completed_date": request.form.get("bunker1_completed_date", ""),
        "bunker2_supply": request.form.get("bunker2_supply") or "",
        "bunker2_name": request.form.get("bunker2_name", ""),
        "bunker2_commenced_hour": request.form.get("bunker2_commenced_hour", ""),
        "bunker2_commenced_date": request.form.get("bunker2_commenced_date", ""),
        "bunker2_completed_hour": request.form.get("bunker2_completed_hour", ""),
        "bunker2_completed_date": request.form.get("bunker2_completed_date", ""),
        "issue_date": datetime.today().strftime('%d/%m/%Y')
    }

    html = render_template("report_template.html", **data)

    pdf_file = f"Summary_Report_{data['vessel']}.pdf"

    HTML(string=html, base_url=request.host_url).write_pdf(pdf_file)

    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)