from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from automation import file_merger, clean_csv, export_file, read_file, hts_cleaner, rejected_dataset, merge_hts_pmtct,  run_model, pmtct_cleaner

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xlx'}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ytrjknuk@hedjfn'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        # if ['HTS','PMTCT'] not in request.files:
        #     flash('No selected file')
        #     return redirect(request.url)
        file_hts = request.files['HTS']
        file_pmtct = request.files['PMTCT']
        files = [file_hts, file_pmtct]
        print(files)
        for file in files:
            if file.filename == '':
                flash('No file Selected')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
            for name, value in globals().items():
                if 'pmtct' in name:
                    print(file_path)
                    df = read_file(file_path)
                    clean_df = clean_csv(df)
                    clean_pmtct = pmtct_cleaner(clean_df)
                if 'hts' in name:
                    print(file_path)
                    df = read_file(file_path)
                    clean_df = clean_csv(df)
                    clean_hts = hts_cleaner(clean_df)
            merged_df = merge_hts_pmtct(clean_hts, clean_pmtct)
        final_df = rejected_dataset(merged_df)
        model_output = run_model(final_df)
        df_to_file = export_file(merged_df)
        # return redirect(url_for('download_file', name=filename))
        return render_template('index.html', context={'output':model_output})
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
