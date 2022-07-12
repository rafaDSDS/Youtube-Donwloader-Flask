from flask import Blueprint,render_template, request,redirect, send_file, session,url_for
from pytube import YouTube
from io import BytesIO

view = Blueprint('view',__name__)

@view.route('/',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        link = str(request.form.get('link'))
        session['link'] = link
        try:link = YouTube(link)
        except Exception as error:return render_template('error.html',error=error)
        return render_template('download.html',link=link)
    return render_template('home.html')

@view.route("/download", methods = ["GET", "POST"])
def download_video():
    if request.method == "POST":
        try:
            buffer = BytesIO()
            url = YouTube(session['link'])
            res = request.form.get('res')
            mp3 = str(request.form.get('mp3'))
            if mp3 != 'on':video = url.streams.get_by_resolution(str(res))
            else:video = url.streams.get_audio_only()
            video.stream_to_buffer(buffer)
            buffer.seek(0)
            name = url.title
            temp = ''
            for c in name:
                if c == '>' or c == '<' or c == '/' or c == '\\' or c == '*' or c == '?' or c == '"':pass
                else:temp += c
            name = temp
            if mp3 == 'on':name = f'{name}.mp3'
            else:name = f'{name}.mp4'
            return send_file(buffer, as_attachment=True, download_name=name, mimetype="video/mp4")
        except Exception as error:return render_template('error.html', error=error)
    return redirect(url_for("view.home"))
