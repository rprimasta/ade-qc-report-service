import os
import gzip, StringIO
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from flask import Flask,render_template,redirect,url_for,request,send_from_directory
import json

app = Flask(__name__)

@app.route("/upload", methods=["POST","GET"])
def upload():
    parse= request.args.get('filename')
    parse_split = parse.split('/')
    f_name = parse_split[len(parse_split)-1]
     
    print f_name
#    return 'sukses'
    data=request.stream.read()
    newFile = open(f_name, "wb")
    newFile.write(data)
    return 'sukses'


@app.route('/pesan/',methods = ['POST','GET'])
def kirim_email():
	response = request.stream.read()
	print "==============================="
	print response
	print "==============================="
	jobj = json.loads(str(response))
	fname = []
	i = 0
	for nm in jobj['files']:
		parse_split = str(nm).split('/')
		print parse_split
    		fname.append(parse_split[len(parse_split)-1])
		i = i+1	
	for nm in fname:
		print nm
	costumer =("Dear ") + str( request.args.get('from'))
        kontraktor  =("Kontraktor      : ") + str( request.args.get('ktr'))
        pekerjaan =("Pekerjaan     :  ") +  str(request.args.get('pkn'))
	lokasi = ("Kordinat Lokasi : ") + str(request.args.get('loc'))
	tujuan = request.args.get('target')
	report = request.args.get('msg')
	
	#====sent email=====

	server = smtplib.SMTP('smtp.gmail.com:587')
        #server.connect("smtp.gmail.com",465)
        server.ehlo()
        server.starttls()
        #Next, log in to the server
        server.login("alert.inovindojayaabadi@gmail.com", "inovindo!2018")
        msg = MIMEMultipart()
        msg['Subject'] = 'Laporan Qc'
        msg['From'] = 'alert.inovindojayaabadi@gmail.com'
        msg['To'] = tujuan
	penutup = "Demikian laporan yang Kami buat. Apakah pekerjaan sudah sesuai?\nMohon tanggapan email ini. \nTerima Kasih."


	pesan2 = costumer+(",\n\n")+kontraktor+("\n")+pekerjaan+("\n")+lokasi+("\n\n")+report+("\n")+penutup
        text = MIMEText(pesan2)
        msg.attach(text)
	for nm in fname:
		img_data = open(nm,'rb').read()
		image = MIMEImage(img_data,name=os.path.basename(nm))
		msg.attach(image)
	server.sendmail("alert.inovindojayaabadi@gmail.com", tujuan ,msg.as_string() )
        server.quit()	
	return ("Pesan Terkirim")
@app.route('/')
def index():
	return render_template("upload.html")
		

if __name__ == '__main__':
   app.run(debug = True,host='0.0.0.0',port=5002)
