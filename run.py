import pathlib
import shutil
from datetime import time
from flask import Flask, jsonify, request, send_file
from docx import Document
import pandas as pd
import os

from werkzeug.utils import secure_filename

from lift_text import (
    rec_form,
    extract_table,
    extract_text_mapping,
    docx_replace
)


app = Flask(__name__)



@app.route("/fill_template", methods=["POST"])
def fill_template():


    sessionid = request.headers.get("SessionId", None)
    if sessionid is None:
        output = {
            "status": "error",
            "message": "sessionid is empty/NONE",
            "response": sessionid
        }
        return output
    else:
        # create folders for input and output files
        session_folder_path = str(pathlib.Path(__file__).parent) + "/flask_session/" + sessionid
        folders_list = [session_folder_path, session_folder_path + "/input", session_folder_path + "/output"]
        if not os.path.exists(session_folder_path):
            for folder in folders_list:
                # flask_logger.debug(folder)
                os.makedirs(folder)

        elif os.path.exists(session_folder_path):
            shutil.rmtree(session_folder_path, ignore_errors=False, onerror=None)
            for folder in folders_list:
                os.makedirs(folder)
            # Parse the input values
        # chart_types = request.form.get("chart_types").split(";")

        # flask_logger.debug(type(chart_types))

        # input  : glenmark_1.pdf
        input_file = request.files["input"]

    if input_file:

        filename = secure_filename(input_file.filename)
        # filename = replace_filenames_space(filename)
        output_filename = filename.split(".")[0] + ".docx"

        input_file.save(input_file.filename)
        input_path = input_file.filename

        form_pages = rec_form(input_path)
        req_tab_headers = ['S.No.','TEST','RESULT','SPECIFICATION','']

        #'S.No.', 'TEST', 'RESULT', 'SPECIFICATION', ''
        #req_tab_headers = ['Sr. No.', 'Test', 'Specification', 'Reference', 'MOA No.']
        extracted_tab = extract_table(req_tab_headers, form_pages)
        print("extracted tab is",extracted_tab)
        df = pd.DataFrame(extracted_tab)
        print("df is",df)
        exce = df.to_excel("sample.xlsx")
        re = df.columns
        print("column values are ",re)
        print("column values are ", df.columns)

        df.columns = req_tab_headers
        print("requested tab headers are",req_tab_headers)
        print("column values are ", df.columns)
        #df = df.drop(['Sr. No.', 'MOA No.'], axis=1)
        df = df.drop(['S.No.',''], axis=1)

        # extracted_tab=extracted_tab.drop(['Sr. No.','MOA No.'], axis = 1)
        text_mapping = extract_text_mapping(form_pages)

        temp_doc = Document("FRM-8112290_1.0_EF.docx")
        #temp_doc.save(output_filename)
        #req_tab_cols = ["Test", "Specification", "Reference"]
        req_tab_cols = ["TEST", "RESULT", "SPECIFICATION"]
        docx_replace(text_mapping, temp_doc, req_tab_cols, df)
        #temp_doc.save(output_filename)
        # input_file = request.files.getlist('file')[0]
        output_folder_path = session_folder_path + "/output"


        if filename:

            input_path = os.path.join(session_folder_path + "/input", filename)
            input_path = os.path.abspath(input_path)
            output_path = os.path.join(session_folder_path + "/output", output_filename)
            output_path = os.path.abspath(output_path)
            temp_doc.save(output_path)
            input_file.save(input_path)

            # input_path = os.path.join(session_folder_path + "/input", filename)
            # input_path = os.path.abspath(input_path)
            # output_path = os.path.join(session_folder_path + "/output", output_filename)
            # output_path = os.path.abspath(output_path)
            # input_file.save(input_path)
            # start_time = time.time()
            # flask_logger.debug(str(filename) + " -> started creating chart pptx file ")
            # create_pptx_chart(input_path, output_path, chart_types)
            # flask_logger.debug(
            #    str(filename) + " -> completed creating chart pptx file  ->" + str(time.time() - start_time))

        else:
            output = {
                "status": "error",
                "message": "Requires input file to be in .docx format",
                "response": filename
            }
            return output
        if os.path.exists(output_path):
            print("file name",output_filename)
            return send_file(output_path, as_attachment=True, attachment_filename=output_filename, cache_timeout=-1)


    # #files = request.files["result.docx"]
    # files = request.files
    # fielsagr = request.data
    # fileval = request.values
    # filea = request.args
    # app.logger.info(files)
    # #file = request
    #
    #
    # return str(files)+str(fielsagr)+str(fileval)+str(filea)


if __name__ == "__main__":
    app.run(debug=True)
