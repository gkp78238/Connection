from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from thoughtspot_tml import Table
import os
from anthropic import Anthropic

client = Anthropic(api_key="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")




main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/update')
def update():
    return render_template('update.html')

@main.route('/help')
def help():
    return render_template('help.html')

@main.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')

@main.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@main.route('/update_tml', methods=['POST'])
def update_tml():
    file = request.files.get('tmlFile')
    if file and file.filename.endswith('.tml'):
        file_path = os.path.join('temp', file.filename)
        file.save(file_path)
        session['tml_file_path'] = file_path
        return redirect(url_for('main.edit_tml'))
    else:
        return jsonify({"error": "No file or incorrect file type"}), 400

@main.route('/edit_tml', methods=['GET', 'POST'])
def edit_tml():
    file_path = session.get('tml_file_path')
    if not file_path:
        return redirect(url_for('main.update'))

    tml_table = Table.load(file_path)

    if request.method == 'POST':
        join_type = request.form.get('join_type')
        join_condition = request.form.get('join_condition')
        destination_table = request.form.get('destination_table')

        new_join = {
            "name": f"{tml_table.table.name}_to_{destination_table}",
            "type": join_type,
            "on": join_condition,
            "destination": {
                "name": destination_table
            }
        }
        tml_table.table.joins_with.append(new_join)

        old_name = request.form.get('old_column_name')
        new_name = request.form.get('new_column_name')
        if old_name and new_name:
            rename_column(tml_table, old_name, new_name)

        new_column_name = request.form.get('new_column_name')
        new_column_type = request.form.get('new_column_type')
        if new_column_name and new_column_type:
            add_column(tml_table, new_column_name, new_column_type)

        new_file_path = os.path.join('temp', f"{os.path.splitext(os.path.basename(file_path))[0]}_modified.table.tml")
        tml_table.dump(new_file_path)

        return redirect(url_for('main.tml_saved', filename=os.path.basename(new_file_path)))

    return render_template('edit_tml.html', tml_table=tml_table)

@main.route('/tml_saved')
def tml_saved():
    filename = request.args.get('filename')
    return render_template('tml_saved.html', filename=filename)

def rename_column(tml_table, old_name, new_name):
    for column in tml_table.table.columns:
        if column.name == old_name:
            column.name = new_name
            return
    raise ValueError(f"Column '{old_name}' not found in the TML file.")

def add_column(tml_table, column_name, column_type):
    new_column = {
        "name": column_name,
        "type": column_type
    }
    tml_table.table.columns.append(new_column)

@main.route('/tml_insights', methods=['POST'])
def tml_insights():
    data = request.json
    question = data.get('question')
    filename = data.get('tml_content')
    
    file_path = os.path.join('temp', filename)
    with open(file_path, 'r') as file:
        tml_content = file.read()
    
    response = generate_response(question, tml_content)
    
    return jsonify({'response': response})




def generate_response(question, tml_data):
    prompt = f"""
    TML File Content:
    {tml_data}

    User Question: {question}

    Provide insights about the TML file based on the question:
    """

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text

