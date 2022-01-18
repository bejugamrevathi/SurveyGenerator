import sys
import json
from semantics_syntax import semantic_syntax

def generate_html(db):
    cs  = db['caption']
    s1 ='''
    <html>
        <head>
            <title>'''+cs+'''</title>
            <script src="'''+db['name']+'''.js"></script>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        </head>
        <body>
            <h3>'''+cs+'''</h3><br/>
        '''
    elements = db['elements']
    for x in elements:
         etype = x['etype']
         if etype=='textbox':
             s1=s1+'''
            <label>'''+x['caption']+'''</label>
            <input name= "'''+x['ename']+'''" size= "'''+x['size']+'''" maxlength="'''+x['maxlength']
             s1=s1+'''" type = "text" '''
             if x['required']=='true':
                s1+='''required />
            <br/><br/>'''
             else:
                s1+='''/>
            <br/><br/>'''

         elif etype=='checkbox':
             s1=s1+'''

            <label>'''+x['caption']+'''</label><br/>'''
             for k in x['group']:
                 s1=s1+'''
            <label><input type="checkbox" value="'''+k['value']+'''" name="'''+x['ename']
                 if 'checked' in k:
                     s1=s1+'''"  checked/>'''+k['caption']+'''</label><br/>'''
                 else:
                     s1=s1+'''"/>'''+k['caption']+'''</label><br/>'''

         elif etype=='selectlist':
             s1=s1+'''
            <br/>
            <label>'''+x['caption']+'''</label><br/>
            <select name="'''+x['ename']+'''">'''
             for k in x['group']:
                 s1=s1+'''
                <option value="'''+k['value']+'''">'''+k['caption']+'''</option>'''
             s1+='''
            </select><br/>'''
         elif etype=='radiobutton':
             s1=s1+'''
            <br/>
            <label>'''+x['caption']+'''</label><br/>'''
             for k in x['group']:
                 s1=s1+'''
            <label><input type="radio" value="'''+k['value']+'''" name="'''+x['ename']+'''" />'''+k['caption']+'''</label><br/>'''
         elif etype=='submit':
             s1+='''
            <br/>
            <button onclick="myFunction()" name="'''+x['ename']+'''">'''+x['caption']+'''</button>'''
         elif etype=='reset':
             s1+='''
            <button onclick="reload()" name="'''+x['ename']+'''">'''+x['caption']+'''</button>'''
         elif etype=='multiselectlist':
             s1=s1+'''
            <br/>

            <label>'''+x['caption']+'''</label><br/>
            <select name="'''+x['ename']+'''" size="'''+x['size']+'''" multiple>'''
             for k in x['group']:
                 s1=s1+'''
                <option value="'''+k['value']+'''">'''+k['caption']+'''</option>'''
             s1+='''
            </select><br/>'''
    s1+='''
        </body>
    </html>'''

    #print(s1)
    f = open(db['name']+".html", "w+")
    f.write(s1)
    f.close()


def generate_js(db):
    cs=db['elements']
    s2='''function myFunction(){

    var data = {};
    var flag = false;'''
    elements = db['elements']


    for x in elements:
        etype = x['etype']
        if etype=='textbox':

            if x['datatype'] == 'integer':
                s2+='''
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''")[0].value;
    if(/^\d+$/.test('''+x['ename']+''')){
        data["'''+x['ename']+'''"] = '''+x['ename']+''';
    }else{
        flag = true;
        alert("Invalid DataType for '''+x['ename']+'''. Expected is '''+x['datatype']+'''");
    }'''
            else:
                s2+='''
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''")[0].value;
    data["'''+x['ename']+'''"] = '''+x['ename']

            if x['required']=='true':
               s2+='''
    if('''+x['ename']+'''==''){
        alert("'''+x['ename']+''' is required field");
        flag = true;
    }'''
        
        elif etype=='checkbox':
            s2+='''
    var '''+x['ename']+'''Selected = [];
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''");
    for(i=0; i<'''+x['ename']+'''.length; i++){
        if('''+x['ename']+'''[i].checked == true){
            '''+x['ename']+'''Selected.push('''+x['ename']+'''[i].parentElement.innerText)
        }
    }
    data["'''+x['ename']+'''"] = '''+x['ename']+'''Selected;'''

        elif etype=='selectlist':
            s2+='''
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''")[0];
    var '''+x['ename']+'''Selected = '''+x['ename']+'''.options['''+x['ename']+'''.selectedIndex].textContent;
    data["'''+x['ename']+'''"] = '''+x['ename']+'''Selected;'''

        elif etype=='radiobutton':
            s2+='''
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''");
    for(i=0; i<'''+x['ename']+'''.length; i++){
        if('''+x['ename']+'''[i].checked == true){
            data["'''+x['ename']+'''"] = '''+x['ename']+'''[i].parentElement.innerText;
        }
    }'''
        elif etype=="multiselectlist":
            s2+='''
    var '''+x['ename']+''' = document.getElementsByName("'''+x['ename']+'''")[0];
    var '''+x['ename']+'''Selected = [];
    for(var i=0; i<'''+x['ename']+'''.length; i++){
        if('''+x['ename']+'''.options[i].selected){
            '''+x['ename']+'''Selected.push('''+x['ename']+'''.options[i].textContent);
        }
    }
    data["'''+x['ename']+'''"] = '''+x['ename']+'''Selected;'''

    s2+='''
    console.log(data);
    if(!flag){
        var url = \''''+db['backendURL']+'''\'
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                if (response.ok == true) {
                    alert(response.msg)
                }
                else if(response.ok == false){
                    alert(response.msg)
                }
            },
            error: function(error) {
                alert("ERROR");
                console.log(error);
            }
        });
    }
}

function reload(){
    window.location.reload();
}

function displayData(){
    var url = \''''+db['backendURL']+'''\'
    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            console.log(response)
            for(let k in response){
                var h2 = document.createElement('h2')
                h2.innerHTML = k
                var table = document.createElement('table')
                table.setAttribute('border',1)
                var th = document.createElement('tr')
                headerList = response[k]['headers']
                for(i=0; i<headerList.length; i++){
                    var td = document.createElement('th')
                    var text = document.createTextNode(headerList[i])
                    td.appendChild(text)
                    th.appendChild(td)
                }
                table.appendChild(th)
                dataList = response[k]['data']
                
                for(i=0; i<dataList.length; i++){
                    var tr = document.createElement('tr')
                    for(j=0; j<dataList[i].length; j++){
                        var td = document.createElement('td')
                        var text = document.createTextNode(dataList[i][j])
                        td.appendChild(text)
                        tr.appendChild(td)
                    }
                    table.appendChild(tr)
                }
                document.getElementById('addTable').appendChild(h2)
                h2.append(table)
                br1=document.createElement('br')
                br2=document.createElement('br')
                document.getElementById('addTable').appendChild(br2)
                document.getElementById('addTable').appendChild(br1)
            }
            

        },
        error: function(error) {
            alert("ERROR");
        }
    });
}'''
    #print(s2)
    f = open(db['name']+".js", "w+")
    f.write(s2)
    f.close()



mainTable=[]
seperateTable=[]



def generate_py(db):
    s3='''
import json
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import mysql.connector as mysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/webforms/', methods=['POST'])
def insert_data():'''


    key = ''
    for x in db['elements']:
        etype = x['etype']
        if etype == "textbox" or etype=='selectlist' or etype=='radiobutton':
            mainTable.append(x['ename'])
        elif etype == "checkbox" or etype=='multiselectlist' :
            seperateTable.append(x['ename'])

        if 'key' in x:
            key = x['ename']

    s3+='''
    sql1 = "INSERT INTO '''+db['name']+'''('''
    for x in mainTable:
        s3+=x+''','''
    s3=s3=s3[:-1]+''') values ('''
    for x in mainTable:
        s3+=''' '" + request.json[\''''+x+'''\'] + "','''

    s3=s3[:-1]+''' );" '''

    s3+='''
    database = mysql.connect(
        host = 'localhost',
        database = \''''+db['mysqlDB']+'''\',
        user = \''''+db['mysqlUserID']+'''\',
        passwd = \''''+db['mysqlPWD']+'''\',
        auth_plugin = 'mysql_native_password'
    )
    cursor = database.cursor()
    try:
        cursor.execute(sql1)
        database.commit()
        result = {"ok": True, "msg": 'Main table data insertion Success'}
    except Exception as e:
        database.rollback()
        cursor.close()
        database.close()
        result = {"ok": False, "msg": 'Data Inserstion into '''+db['name']+''' table Failed'}
        return jsonify(result)'''

    #print(seperateTable)
    for y in seperateTable:
        s3+='''
    for k in request.json[\''''+y+'''\']:
        '''+y+''' = "INSERT INTO '''+y+''' values ('" +request.json[\''''+key+'''\']+ "','" +k+ "');"
        try:
            cursor.execute('''+y+''')
            result = {"ok": True, "msg": 'seperate data insertion Success'}
        except Exception as e:
            database.rollback()
            cursor.close()
            database.close()
            result = {"ok": False, "msg": 'Data Inserstion into '''+y+''' table Failed'}
            return jsonify(result)'''

    s3+='''
    database.commit()
    cursor.close()
    database.close()
    return jsonify(result)'''

    s3+='''


@app.route('/webforms/', methods=['GET'])
def get_data():
    db = mysql.connect(
        host = 'localhost',
        database = \''''+db['mysqlDB']+'''\',
        user = \''''+db['mysqlUserID']+'''\',
        passwd = \''''+db['mysqlPWD']+'''\',
        auth_plugin = 'mysql_native_password'
    )
    query1 = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \''''+db['mysqlDB']+'''\' AND TABLE_NAME = \''''+db['name']+'''\'"
    query2 = "select * from '''+db['name']+'''"
    cursor = db.cursor()
    try:
        cursor.execute(query1)
        '''+db['name']+'''={}
        '''+db['name']+'''['headers'] = [str(x[0]) for x in cursor]
    except Exception as e:
        cursor.close()
        db.close()
        result = {"ok": False, "msg": 'Error occured'}
        return jsonify(result)

    try:
        cursor.execute(query2)
        '''+db['name']+'''['data'] = cursor.fetchall()
    except Exception as e:
        cursor.close()
        db.close()
        result = {"ok": False, "msg": 'Error Occured'}
        return jsonify(result)
    '''
    for k in seperateTable:
        s3+='''
    Headers'''+k+''' = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \''''+db['mysqlDB']+'''\' AND TABLE_NAME = \''''+k+'''\' order by ordinal_position;"
    try:
        cursor.execute(Headers'''+k+''')
        '''+k+''' = {}
        '''+k+'''['headers'] = [str(x[0]) for x in cursor]
        Data'''+k+''' = "Select * from '''+k+'''"
        cursor.execute(Data'''+k+''')
        '''+k+'''['data'] = cursor.fetchall()
    except Exception as e:
        cursor.close()
        db.close()
        result = {"ok": False, "msg": 'Error occured'}
        return jsonify(result)
    '''
    s3+='''
    total={}
    total[\''''+db['name']+'''\'] = '''+db['name']
    for k in seperateTable:
        s3+='''
    total[\''''+k+'''\']='''+k
    
    
    s3+='''
    cursor.close()
    db.close()
    print(total)
    return jsonify(total)

if __name__ == '__main__':
    app.run(host='localhost',debug=True)'''

    #print(s3)
    f = open(db['name']+".py", "w+")
    f.write(s3)
    f.close()




def max_length(sample):
    filt_key = "caption"
    temp = (sub[filt_key] for sub in sample) 
    res = max(len(ele) for ele in temp if ele is not None)
    return str(res)

def generate_sql(db):
    sample = '''CREATE DATABASE IF NOT EXISTS '''+db['mysqlDB']+''';
USE '''+db['mysqlDB']+''';'''
    
    elements = db['elements']
    for x in elements:
        if(x['etype']== "checkbox" or x['etype']== "multiselectlist"):
            sample =sample+'''
drop table if exists '''+x['ename']+''';'''
    sample =sample+'''
drop table if exists '''+db['name']+''';'''
    sample =sample +'''
SET FOREIGN_KEY_CHECKS=1;'''
    sample = sample + '''
create table '''+db['name']+'''('''
    for x in elements:
        if(len(x) >=5):
            if(x['etype']=='textbox' or x['etype']=='selectlist' or x['etype']=='radiobutton'):
                if(x['datatype']=='integer'):
                    sample = sample +''''''+x['ename']+''' int,'''
                if(x['datatype']=='string' and 'maxlength' in x):
                    sample = sample +''''''+x['ename']+''' varchar('''+x['maxlength']+'''),'''
                if(x['datatype']=='string' and 'group' in x):
                    sample = sample + ''''''+x['ename']+''' varchar('''+str(max_length(x['group']))+'''),'''
    for x in elements:
        if('key' in x):
            sample = sample + '''primary key('''+x['ename']+''')'''
    sample = sample + ''');'''

    
    
    for x in elements:
        if(x['etype']=='checkbox'):
            sample = sample + '''
create table'''
            col = x['ename']
            length=max_length(x['group'])
            sample = sample + ''' '''+x['ename']+'''('''
    for x in elements:
        if('key' in x):
            sample = sample+''''''+x['ename']+''' int,'''+col+'''_col varchar('''+length+'''), primary key('''+x['ename']+''','''+col+'''_col),foreign key('''+x['ename']+''') references '''+db['name']+'''('''+x['ename']+''') ''' 
    sample = sample + ''');'''
    
    col2 = ' '
    for x in elements:
        if('key' in x):
            key = x['ename']

    for x in elements:
        if(x['etype']=='multiselectlist'):
            sample = sample + '''
create table '''+x['ename']+'''( '''
            col2 = x['ename']
            length=max_length(x['group'])
            sample = sample+''''''+key+''' int,'''+col2+'''_col varchar('''+length+'''), primary key('''+key+''','''+col2+'''_col),foreign key('''+key+''') references '''+db['name']+'''('''+key+''') ''' 
            sample = sample + ''');'''
        

    f = open(db['name']+".sql", "w+")
    f.write(sample)
    f.close()



def generate_display_html(db):
    s4 = '''
    <html>
        <head>
            <title>'''+db['name']+'''Data</title>
            <script src="'''+db['name']+'''.js"></script>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        </head>
        <body>
            <button onclick="displayData()" />Display Data</button>
            <div id = 'addTable'>
                <br/><br/>
            </div>
        </body>
    </html>
    '''
    #print(s4)
    f = open(db['name']+"_display.html", "w+")
    f.write(s4)
    f.close()


def main():
    if(semantic_syntax() == 0):
        with open(sys.argv[1],'r') as fp:
            db = json.load(fp)
            generate_html(db)
            generate_js(db)
            generate_py(db)
            generate_sql(db)
            generate_display_html(db)
            print("Files generated successfully")
    else: 
        print("Check for Syntax or Semantic errors as mentioned above")

main()
