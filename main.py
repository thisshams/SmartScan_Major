from flask import Flask,render_template,request
import os
import pyrebase
import cv2
from PIL import Image,ImageOps
import numpy as np
import img2pdf
from fpdf import FPDF
import requests


app=Flask(__name__)

config = {
        "apiKey": "AIzaSyAaa8Fv5r8l3AjLfFlw4CZk48oNLk-iXfc",
        "authDomain": "smartscan-7d1a3.firebaseapp.com",
        "projectId": "smartscan-7d1a3",
        "storageBucket": "smartscan-7d1a3.appspot.com",
        "messagingSenderId": "427150561575",
        "appId": "1:427150561575:web:ded4c273c16eba27d85902",
        "databaseURL": "https://smartscan-7d1a3-default-rtdb.firebaseio.com/",
        "serviceAccount":  {
            "type": "service_account",
            "project_id": "smartscan-7d1a3",
            "private_key_id": "c2387e82c1ca27062a570fbc6c0d15fe133e7bae",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDCPYct1GO/FL0X\nWeryId95vXXnWfBhjZW/CZRjMSB41Qi774s+CvgVnAqjYiDoyRaWW01DZ3nQmYgd\n2zZpb4qOUK9/YBkNURzeaS7yeSv2zp2bdnbfOqYp65sod49Pxisf2xwVYHeVcwmH\nbd6sND6ke33trHQvf3v8aBhFI729/nmj/O3DHkd2pEF0ytK9OM7efLQTArntfZcr\nhULVoNBYwpWakIUtUHTba8ohPBGGWRxC5RkAyLSe/4iB230JDLcLPiRUgGVvkB4a\nzoq1ImKE/V11BBI48nU7HVDgTiJ3powjlyMsRxog1GNBCR/JIjButyDfZRILb5TR\nXOMkJE61AgMBAAECggEAFB92sS9HNCUMX+5vUi1jLwQLQnAFYL3fzR5LcqlEwW/k\niz/KT5+oSujTC1Efsq4eem40B28hZhR5zwoGTY8CLjM6szn77m7ATGReOj2GaffG\nyTPRJdg4HbCsbtlQDgYsMo0rECXhzahQzOh7gKCa+sRWa/iJQuB0slYAaa1Fu3iC\nii+arUmPYK2usprVTFhQGSMINfSo4JbNF1VzozgeLp4EGkivexuMcCKJC3oqT9/t\n+4p/OZjvNSdhlIp0O7e+yx6VYFeEQ0PXD2LeDbukhnTTBKq8LbrNuzJiQqydrMcI\n7v7wmKLLttIU79g7LsOpsNnq1ZvgNCIWZQfNkTx4YQKBgQD78SDmkXlP/y9wrB5T\nex2N0ELdRbK3KkrMcoUud/uiDOTmMTl0lgX6hhQFRxZOKXAmoaKhK1ZKicHhUp0x\nuSeQhy0m/R4BLRo1CInJDOYCIR0TZ8akN2zwRy5WlDeHJvNJer4vWLM6YiRUTFAP\nO0Y6IJeUkUOYxWHY5EA039JdEQKBgQDFXng6Npf9ZW5Q6hkvrK0egCXESgcTg1tM\npmQhsCwmjtK0ZWhrCO77+d7vg+OF3TZCvQLxivkWDa11kTzyACsJaZoWD1o5eOwH\nYLxqnFntf5heDgDcrBnVpGPPJC6S97BjB0Qp9+kmcBlIvffv656F57r/++gOPzL8\nYQK3ingnZQKBgGS4SUbj8XOhuP16UcVd+rqu/4wmSQQgzDZfsg6ZuOdX8Ep2c1nA\ngDNfVrGlca1ds5A+Hh4AjUbPO8swk9dFBiQpZkun9U7TER8SgsL1fR5szorreeY8\nojiMvGGwb2KAl9JQV6fl9gDpK0zoFTmBoNmsHe0vBa8VecCTv3dj412BAoGAMrlL\nttJPD42g42S2ol0DhQI0MpU/6lDpBvMAavQG9MXh+wDQ7Ck4mkOmevHvaHjouBAx\nkHhB+dv8B2oTOrK2XM3qDt9VNc4RAvhmlBOovPP86bc5m30TiqecCyFmYtkLWPgG\nGa8gGYPXy60e6mcor4tVsPJBul+dr+USuK76oE0CgYBPVbcLaN3heGgklIGtBiHC\nWC8cPWieltTJal7F24HWYKmcaJNHQMvbPZPfc3kAIrFWjhqNduU62p1g1dfpEClJ\nY4C3adEbaiG2eh4AbH1AFZbW0235f1U7yRkzEi9fXfETkrnm4NEVUeIEU5Z12GE7\nRHRMn7sKVqA/ViySgGXPPQ==\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-qzn7o@smartscan-7d1a3.iam.gserviceaccount.com",
            "client_id": "104110910319662337608",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-qzn7o%40smartscan-7d1a3.iam.gserviceaccount.com"
        }
    }

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()
db = firebase_storage.database()


@app.route("/",methods=['GET',"POST"])
def home():
    if request.method=='POST':
        name=request.form.get("name")
        gender=request.form.get("gender")
        dob=request.form.get("dob")
        file=request.form.get("fileurl")
        print(request.form)
        print("\33[1;32m index.html POST \33[m")
        print(name,gender,dob,file)
        fdata=requests.get(file).content
        data={"Name":name,"Gender":gender,"DOB":dob,"File":str(fdata)}
        db.child(name).set(data)
        return render_template("success.html")
    return render_template("index.html")

# @app.route("/{}")

@app.route("/uploads/<string:code>",methods=['GET','POST'])
def uploads(code):
    numberofFiles=0
    UPLOAD_FOLDER = "files/"+code+"/"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == "POST":
        # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",request.files["files"])
        files = request.files.getlist("files")
        os.makedirs(UPLOAD_FOLDER)
        for file in files:
            print("####################################",file.filename)
            if len(files)==1:
                if file.filename.endswith(".pdf") or file.filename.endswith(".PDF"):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], "output.pdf"))
                    storage.child(code+"/output.pdf").put("files/"+code+"/output.pdf")
                    return render_template("success.html",code=code)
                else:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], "img1.jpg"))
                    img_path = "files/"+code+"/img1.jpg"
                    pdf_path = "files/"+code+"/output.pdf"
                    img=cv2.imread(img_path)
                    processImage(img,code,1)
                    compress(code,1)
                    image = Image.open("files/"+code+"/compress1.jpg")
                    image = ImageOps.exif_transpose(image)
                    image = image.convert('RGB')
                    image.save(pdf_path)
                    print("Successfully made pdf file")

                    storage.child(code+"/output.pdf").put("files/"+code+"/output.pdf")
                    return render_template("success.html",code=code)
        for file in files:
            numberofFiles+=1
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "img"+str(numberofFiles)+".jpg"))

        print("----------------------->>>>>>",os.listdir("files/"+code+"/"))
        count=1   
        for i in os.listdir("files/"+code+"/"):
            img=cv2.imread("files/"+code+"/"+i)
            # h,w,_=img.shape
            # img = cv2.resize(img, min((1240,1754),(w,h)))
            processImage(img,code,count)
            compress(code,count)
            count+=1


        with open("files/"+code+"/output.pdf", "wb") as f:
            f.write(img2pdf.convert([f'files/{code}/{i}' for i in os.listdir("files/"+code+"/") if (i.startswith("compress") and i.endswith(".jpg"))]))
        
        storage.child(code+"/output.pdf").put("files/"+code+"/output.pdf")
        return render_template("success.html", code=code)


        

    

    return render_template("uploads.html",code=code)





def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min



def processImage(img,code,count):
    img = img.copy()
    kSize = 51
    whitePoint = 127
    blackPoint = 66

    if not kSize % 2:
        kSize += 1

    kernel = np.ones((kSize, kSize), np.float32)/(kSize*kSize)

    filtered = cv2.filter2D(img, -1, kernel)

    filtered = img.astype('float32') - filtered.astype('float32')
    filtered = filtered + 127*np.ones(img.shape, np.uint8)

    filtered = filtered.astype('uint8')

    img = filtered

    _, img = cv2.threshold(img, whitePoint, 255, cv2.THRESH_TRUNC)

    img = img.astype('int32')
    img = map(img, 0, whitePoint, 0, 255)
    img = img.astype('uint8')

    print("Scanning Done.")

    # refer repository's wiki page for detailed explanation

    img = img.astype('int32')

    img = map(img, blackPoint, 255, 0, 255)


    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_TOZERO)

    
    cv2.imwrite("files/"+code+"/scan"+str(count)+".jpg",img)
    print("image scan complete", count)


def compress(code,count):
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = Image.fromarray(img)
    img=Image.open("files/"+code+"/scan"+str(count)+".jpg")
    w, h = img.size
    img = img.resize(min((1240,1754),(w, h)), Image.ANTIALIAS)
    img.save("files/"+code+"/compress"+str(count)+".jpg",quality=60,optimizer=True)
    print("compression done",count)



if __name__=="__main__":
    app.run(debug=True)