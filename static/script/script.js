import { initializeApp } from "https://www.gstatic.com/firebasejs/9.9.4/firebase-app.js";
import { getAuth,signInWithEmailAndPassword,onAuthStateChanged,signOut } from "https://www.gstatic.com/firebasejs/9.9.4/firebase-auth.js";
import { getDatabase , ref, set} from "https://www.gstatic.com/firebasejs/9.9.4/firebase-database.js";
import { getStorage,ref as sRef, getDownloadURL,uploadBytesResumable } from "https://www.gstatic.com/firebasejs/9.9.4/firebase-storage.js";


const url="http://localhost:5000/uploads/"
// "http://localhost:5000/uploads/"


const firebaseConfig = {
    apiKey: "AIzaSyAaa8Fv5r8l3AjLfFlw4CZk48oNLk-iXfc",
    authDomain: "smartscan-7d1a3.firebaseapp.com",
    projectId: "smartscan-7d1a3",
    storageBucket: "smartscan-7d1a3.appspot.com",
    messagingSenderId: "427150561575",
    appId: "1:427150561575:web:ded4c273c16eba27d85902"
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const storage = getStorage(app);

const createBtn = document.getElementById('create_button')
const uploadBtn = document.getElementById('upload')
const findBtn = document.getElementById('find')
 





var result = '';
        function makeid() {
            result = ''
            var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            var charactersLength = characters.length;
            for (var i = 0; i < 6; i++) {
                result += characters.charAt(Math.floor(Math.random() *
                    charactersLength));
            }
            return url + result;
        }


        //QR CODE GENERATOR
const btn = document.getElementById("document");
var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];
span.onclick = function () {
    modal.style.display = "none";
}

// window.onclick = function (event) {
//     if (event.target == modal) {
//         modal.style.display = "none";
//     }
// }
var qrtext = ''
var qr;
// if (btn) {
//     btn.addEventListener('click', function () {
        
//     })
// }



    

    window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
    }
    var qrtext=''
    var qr;
    if(btn){
        btn.addEventListener('click',function(){
            (function () {
                qr = new QRious({
                    element: document.getElementById('qr-code'),
                    size: 200,
                    value: ''
                });
            })();
            qrtext = makeid()
            console.log(qrtext)
            const code = document.getElementById("code")
            code.innerHTML = result
            const httplink = document.getElementById("httplink")
            httplink.innerHTML = qrtext
            httplink.href = qrtext
            modal.style.display = "block";
            qr.set({
                foreground: 'black',
                size: 200,
                value: qrtext
            });

            
        let found=false;
        let time=100;

        const progress =document.getElementById("progresstime")
        progress.value=100
        const timestamp=document.getElementById("timestamp")
        timestamp.innerHTML=100

        const interval = setInterval(function () {
                if (found==true) {
                    clearInterval(interval)
                }
                if (time<=0){
                    modal.style.display = "none";
                    clearInterval(interval)   
                }
                span.onclick = function() {
                    modal.style.display = "none";
                    clearInterval(interval)
                }
                progress.value=time
                timestamp.innerHTML=time
                if (time%5==0){
                console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>",result)
                getDownloadURL(sRef(storage,result+"/output.pdf"))
                .then((url) => {
                    // console.log("wait\n"+localStorage.getItem("uid")+"\n"+qrtext)
                    const xhr = new XMLHttpRequest();
                    xhr.responseType = 'blob';
                    xhr.onload = (event) => {
                    const blob = xhr.response;
                };
                // xhr.open('GET', url);
                //xhr.send();
                const pdf  = document.getElementById('docx')
                pdf.setAttribute('src',url+"#toolbar=0")
                console.log(url)
                document.getElementById("fileurl").value=url
                if (url.startsWith("http")){
                    found=true
                    const uploaded=document.getElementById("document");
                    uploaded.innerHTML='Uploaded'
                    uploaded.style.background="#4BB543";
                    uploaded.style.color='white';
                }
                else{
                    // console.log("File not found!!")
                }

                localStorage.setItem('url', url)
                modal.style.display = "none";
                })
                .catch((error) => {
                    // console.log("File not found !!!")
                    // console.log(error)
                });
            }
            time-=1
        }
            , 1000)});
    }

    