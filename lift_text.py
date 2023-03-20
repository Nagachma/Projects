from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential



def rec_form(doc_path):

    pdf_path = str(doc_path)
    with open(pdf_path, "rb") as fd:
        form = fd.read()
    endpoint = "https://docz-formrecognizer.cognitiveservices.azure.com/"
    credential = AzureKeyCredential("ffc94e6958d043058c802df8fe949ba4")
    form_recognizer_client = FormRecognizerClient(endpoint, credential)
    poller = form_recognizer_client.begin_recognize_content(form)
    form_pages = poller.result()
    #print("form pages are",form_pages)
    return form_pages


def extract_table(req_tab_headers,form_pages):
    all_tabs=[]

    for page in form_pages:
        print("page tables are",page.tables)
        for table in page.tables:
            #print("table is ",dir(table))
            #'bounding_box', 'cells', 'column_count', 'from_dict', 'page_number', 'row_count', 'to_dict'
            print("table is ", table.bounding_box)
            print("table is ", table.cells)
            print("table is ", table.from_dict)
            print("table is ", table.to_dict)

            rc,cc=table.row_count, table.column_count
            print("inbuilts are",dir(rc),dir(cc))
            print("current tab is", rc,cc)
            cur_tab=[["" for i in range(cc)] for j in range(rc)]
            print("current tab is",cur_tab[0])
            for cell in table.cells:
                print("cell value is ",cell.text)
                cur_tab[cell.row_index][cell.column_index]=cell.text
            print("current tab issssss",cur_tab)
            if cur_tab[0]==req_tab_headers:
                rem_rows=[]
                for r in range(len(cur_tab)-1,-1,-1):
                    if "".join(cur_tab[r])=="":
                        rem_rows.append(r)
                    else:
                        break
                if len(rem_rows)>0:
                    del cur_tab[rem_rows[-1]:]
                del cur_tab[0]
                all_tabs.extend(cur_tab)

    return all_tabs


def extract_text_mapping(form_pages):

    req_tab_headers = ['Sr. No.', 'Test', 'Specification', 'Reference', 'MOA No.']
    text_mapping={}
    text_mapping["Source:"]=form_pages[0].lines[1].text

    print("text mapping source is",text_mapping["Source:"])
    mop=""
    sc=""
    sc_flag=False
    mop_flag=False
    el = []
    for n,line in enumerate(form_pages[0].lines):
        print("line is",line.text)
        el.append(line.text)
        print("n value is ",n)
        if "Mode of Packing" in line.text:
            mop_flag=True
        
        if "STORAGE" in line.text:
            print("STORAGE inside ",line.text)
            mop_flag=False
            sc_flag=True
        
        if "Prepared By" in line.text:
            sc_flag=False

        if mop_flag:
            mop=mop+" "+line.text
        # if sc_flag:
        #     ssc = sc+" "+form_pages[0].lines[n+0].te
        #     print("ssc value is",ssc)
        if sc_flag:
            print("sc_flag value is",sc_flag)
            sc=sc+" "+line.text
            print("sc value is",sc)
            #sc_flag = False

        if "Product" in line.text:
            text_mapping["Product:"] = form_pages[0].lines[n+1].text.strip()

        
        elif "Specification Type :" in line.text:
            text_mapping["Market:"] = form_pages[0].lines[n+2].text.strip()


        elif "Reference" in line.text:
            text_mapping["Reference:"] = form_pages[0].lines[n+1].text.strip()
    print("el list is ",el)

    ci=mop.find(":")
    mop=mop[ci+1:].strip()
    text_mapping["@Packaging details"]=mop

    ci=sc.find(":")

    print("ci value is",ci)
    sc=sc[ci+1:].strip()
    print("sc splitted value is",sc)
    text_mapping["@Storage Conditions"]=sc.split(".")[0]
    print("text mapping is ",text_mapping)
    return text_mapping


def docx_replace(text_mapping,temp_doc,req_tab_cols,df):
    df = df
  
    for paragraph in temp_doc.paragraphs:
        if paragraph.text in text_mapping:
            paragraph.text= text_mapping[paragraph.text]

    for table in temp_doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if paragraph.text in text_mapping:
                        paragraph.text= paragraph.text + " " + text_mapping[paragraph.text]
    
    for t in temp_doc.tables:
        tab_cols=[]
        for col in t.columns:
            for c in col.cells:
                tab_cols.append(c.text)
                if tab_cols==req_tab_cols:
                    for i in range(df.shape[0]):
                        row=t.add_row().cells
                        for j in range(df.shape[1]):
                            row[j].text = str(df.values[i,j])
                break
                        
    #temp_doc.save('result.docx')
