﻿# -*- coding: UTF-8 -*-
# !/usr/bin/python3 python3
VERSION = "2019/08/07";
THIS_IS_DAILYPASTE = False;
# DEFAULT_SERVER_IP = '127.0.0.1';
# change it by yourself!!!
# because pooooor python can never get an IP from computer.
# no need to change it anymore.
# somethings has been deprecated due to some reason.
# RIP,[download all module] and [upload all module]

import html
import http.server
import io
import os
import socketserver
import sys
import urllib.parse
import base64
import gzip
import posixpath
import subprocess
import shutil
import zipfile
import platform

# -----SETTING_BEGIN-------

DEFAULT_PORT = 80;
# DEFAULT_LISTENER_PORT = 11235;
CHEKEY = bytes(VERSION, "utf8");
DEFAULT_FILE_DIR = '/home';
DEFAULT_GZIP = 0;
DEFAULT_ENC = 'utf-8';
DEFAULT_ROBOTS_TXT = 'User-agent: *\r\nDisallow: /FILE/\r\n';
DEFAULT_ROBOTS_TXT_ENC = DEFAULT_ROBOTS_TXT.encode(DEFAULT_ENC, 'surrogateescape');
# DEFAULT_ROBOTS_TXT_GZIP = gzip.compress(DEFAULT_ROBOTS_TXT_ENC);
DEFAULT_ICON_B64 = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAACXUlEQVR4Xu2W3VLGIAwFef+XVil+tWyh5AToz9gd98aG5CTjhSG8zOfr58crez2Cr0hhmV4553Ysi28pLNFl1vpGZMm2cIFeCzDLqTDMDi7QYwNmmw4DVOEiXg0w4zQ4+BAu4tUIs46G89pwEY8iMSeDj+DTmPPacCFVgW3OLH0nbMy5x3AhVQHm/FvBDxuumuFCigLMt7ELNss081lI1QhzQTdsVNRErFM1wjwVZdigqolYp2qAWRqa4cOmJmKdYgNmMGqCj0w2iTVWG3C2YBM+kDwLzhU9hMWys+E8h1VY6HYWnNNhERa5nQFndLqDBW5nwlmdZvCjyzPgzA4z+FH2TDjbaQY/yp4JZztd4QfZK2AGp2FJX/ggeQXM4DRU0xeKi14Js1jEe20DNhOfD4dZ1FzyAe6GsmyJxx+gl/cA/MV/4/0LeA/Qc4D4tOP5HbAf4LNsySthFjHP/gBsZvFKmKVmhXQAFnu8AmZQXVr85wOE5b/IBD+4PBPOdrgu/x5g1AGiZ8CZTuccIDoTzuowO8AjjsAZHXL3BRa5nQXndMjdV1goOxvOc8idM1gseRacK8qdd/CB2Qaptc0mnG30d8Vj+Mhkg9TWrglmMJg2NMCHhxpILTVNbHM0XBZTYIOiRlI7TRPbLAcuC3lgo0wjqY2umU+einEPN2y2KpDa+DQTayuGXthQJbXwKRHrYRhF1lggPfUrE9/8GkazNBZJz/qUSe/mwXk1YukIFcJZcHCJWDZCK+FsGIDEklG2CFfCMJH465HWCHcCwYZKwgPYLdHrUxYvsVtGcCrf2zenNym48xMAAAAASUVORK5CYII="
DEFAULT_ICON = base64.b64decode(DEFAULT_ICON_B64);

DEFAULT_TITLE = 'EXsimple';
DEFAULT_TITLE_WORDS = '''
    <h1>%s</h1>
    <h1 class = "subtitle">V%s</h1>
    <h1 class = "subtitle">convenient way to set up a simple file-server , provided by XenoAmess.</h1>
    <p class = "subtitle">github : <a target="_blank" href="https://github.com/XenoAmess/EXsimple">https://github.com/XenoAmess/EXsimple/</a></p>
''' % (DEFAULT_TITLE, VERSION);

if THIS_IS_DAILYPASTE:
    DEFAULT_TITLE = 'DailyPaste!'
    DEFAULT_TITLE_WORDS = '''
    <h1>%s</h1>
    <h1 class = "subtitle">V%s</h1>
    <h1 class = "subtitle">A free file Pastebin who cleans all things at 00:00UTC!</h1>
    <div>
        <p class = "subtitle">(Don't over-use it or I will be bankrupt!)</p>
        <p class = "subtitle">provided by XenoAmess!</p>
        <p class = "subtitle">github : <a target="_blank" href="https://github.com/XenoAmess/EXsimple">https://github.com/XenoAmess/EXsimple/</a></p>
    </div>
''' % (DEFAULT_TITLE, VERSION);

LIST_DIRECTORY_CSS = '''
html,body{
    font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
    margin:0px;
    padding:0;
    width:100%;
    height:100%;
    overflow : auto;
} 
body {
    background-color: #FFFFFF;
}
.-body {
}
ul {
    font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
    font-weight : 800;
    border: 0px;
    border-radius: 0px;
    list-style-type: none;
    position: absolute;
    margin: 0px;
    padding: 0px;
    width : 100% ;
}
li { 
    font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
    font-weight : 800;
    /*filter:alpha(Opacity=60);-moz-opacity:0.6;opacity: 0.6; */  
    margin: 5px;
    display: block;
    border: 2px solid #000000;

    padding: 5px;
    border-radius: 5px 5px;

    background-color: #00FFFF;
}
li.file {
    background-color: #00FFFF;
}
li.folder {
    background-color: #00FF00;
}
li.link {
    background-color: #FF3EFF;
}
a.link_in_list { 
    display : block;
    text-decoration:none;
    font-weight : 700;
    font-size : 20px;
    font-color : #FFFFFF;
}
a.link_in_list:link {
    color: black ; 
    text-decoration:none;
} 
/*常规时候的样式*/
a.link_in_list:visited {
    color: black; 
    text-decoration:none;
} 
/*鼠标指上去的样式*/
a.link_in_list:hover {
    color: black ;
    text-decoration:none;
}
/*访问过后的样式*/
ul li{
    list-style: none;
    display: block;
    word-wrap: break-word;
    word-break: normal; 
}
'''
LIST_DIRECTORY_CSS_ENC = LIST_DIRECTORY_CSS.encode(DEFAULT_ENC, 'surrogateescape');
# LIST_DIRECTORY_CSS_GZIP = gzip.compress(LIST_DIRECTORY_CSS_ENC);

# DEFAULT_JSCRIPT = '''
#         <script type="text/javascript">
#             //modified from http://www.cnblogs.com/dolphinX/p/3290520.html
#             var Dragging=function(validateHandler){ 
#                 var draggingObj=null;
#                 var diffX=0;
#                 var diffY=0;
#                 
#                 function mouseHandler(e){
#                     switch(e.type){
#                         case 'mousedown':
#                             draggingObj=validateHandler(e);//验证是否为可点击移动区域
#                             if(draggingObj!=null){
#                                 diffX=e.clientX-draggingObj.offsetLeft;
#                                 diffY=e.clientY-draggingObj.offsetTop;
#                             }
#                             break;
#                         
#                         case 'mousemove':
#                             if(draggingObj){
#                                 draggingObj.style.left=(e.clientX-diffX)+'px';
#                                 draggingObj.style.top=(e.clientY-diffY)+'px';
#                             }
#                             break;
#                         
#                         case 'mouseup':
#                             draggingObj =null;
#                             diffX=0;
#                             diffY=0;
#                             break;
#                     }
#                 };
#                 
#                 return {
#                     enable:function(){
#                         document.addEventListener('mousedown',mouseHandler);
#                         document.addEventListener('mousemove',mouseHandler);
#                         document.addEventListener('mouseup',mouseHandler);
#                     },
#                     disable:function(){
#                         document.removeEventListener('mousedown',mouseHandler);
#                         document.removeEventListener('mousemove',mouseHandler);
#                         document.removeEventListener('mouseup',mouseHandler);
#                     }
#                 }
#             }
# 
#             function getDraggingDialog(e){
#                 var target=e.target;
#                 while(target && target.className.indexOf('window-title')==-1){
#                     target=target.offsetParent;
#                 }
#                 if(target!=null){
#                     return target.offsetParent;
#                 }else{
#                     return null;
#                 }
#             }
#             
#             Dragging(getDraggingDialog).enable();
#         </script>
# '''

DEFAULT_METHOD_UPLOAD = '''
<!DOCTYPE html>
<html lang="en">
    <head>
    <!--modified from https://www.script-tutorials.com/pure-html5-file-upload/-->
        <meta charset="utf-8" />
        <title>upload</title>
        <style type = "text/css">
        .upload_form_cont {
            background: -moz-linear-gradient(#ffffff, #f2f2f2);
            background: -ms-linear-gradient(#ffffff, #f2f2f2);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #ffffff), color-stop(100%, #f2f2f2));
            background: -webkit-linear-gradient(#ffffff, #f2f2f2);
            background: -o-linear-gradient(#ffffff, #f2f2f2);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#f2f2f2');
            -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#f2f2f2')";
            background: linear-gradient(#ffffff, #f2f2f2);
        
            color:#000;
            overflow:hidden;
        }
        #upload_form {
            float:left;
            padding:5px;
            width:100%;
        }
        #preview {
            background-color:#fff;
            display:block;
            /*float:left;*/
            width:80%;
        }
        #upload_form > div {
            margin-bottom:10px;
        }
        #speed,#remaining {
            float:left;
            width:80%;
        }
        #b_transfered {
            float:right;
            text-align:right;
        }
        .clear_both {
            clear:both;
        }
        input {
            border-radius:10px;
            -moz-border-radius:10px;
            -ms-border-radius:10px;
            -o-border-radius:10px;
            -webkit-border-radius:10px;
        
            border:1px solid #ccc;
            font-size:14pt;
            padding:5px 10px;
        }
        input[type=button] {
            background: -moz-linear-gradient(#ffffff, #dfdfdf);
            background: -ms-linear-gradient(#ffffff, #dfdfdf);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #ffffff), color-stop(100%, #dfdfdf));
            background: -webkit-linear-gradient(#ffffff, #dfdfdf);
            background: -o-linear-gradient(#ffffff, #dfdfdf);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#dfdfdf');
            -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#dfdfdf')";
            background: linear-gradient(#ffffff, #dfdfdf);
        }
        #upload_file {
            width:90%;
        }
        #progress_info {
            font-size:10pt;
        }
        #fileinfo,#error,#error2,#abort,#warnsize {
            color:#aaa;
            display:none;
            font-size:10pt;
            font-style:italic;
            margin-top:10px;
        }
        #progress {
            border:1px solid #ccc;
            display:none;
            float:left;
            height:14px;
        
            border-radius:10px;
            -moz-border-radius:10px;
            -ms-border-radius:10px;
            -o-border-radius:10px;
            -webkit-border-radius:10px;
        
            background: -moz-linear-gradient(#66cc00, #4b9500);
            background: -ms-linear-gradient(#66cc00, #4b9500);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #66cc00), color-stop(100%, #4b9500));
            background: -webkit-linear-gradient(#66cc00, #4b9500);
            background: -o-linear-gradient(#66cc00, #4b9500);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#66cc00', endColorstr='#4b9500');
            -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr='#66cc00', endColorstr='#4b9500')";
            background: linear-gradient(#66cc00, #4b9500);
        }
        #progress_percent {
            float:right;
        }
        #upload_response {
            margin-top: 5px;
            padding: 5px;
            overflow: hidden;
            display: none;
            border: 1px solid #ccc;
        
            border-radius:10px;
            -moz-border-radius:10px;
            -ms-border-radius:10px;
            -o-border-radius:10px;
            -webkit-border-radius:10px;
        
            box-shadow: 0 0 5px #ccc;
            background: -moz-linear-gradient(#bbb, #eee);
            background: -ms-linear-gradient(#bbb, #eee);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #bbb), color-stop(100%, #eee));
            background: -webkit-linear-gradient(#bbb, #eee);
            background: -o-linear-gradient(#bbb, #eee);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#bbb', endColorstr='#eee');
            -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr='#bbb', endColorstr='#eee')";
            background: linear-gradient(#bbb, #eee);
        }
        </style>
        
        <script type="text/javascript" language="javascript">
        // common variables
        var iBytesUploaded = 0;
        var iBytesTotal = 0;
        var iPreviousBytesLoaded = 0;
        var iMaxFilesize = 1048576; // 1MB
        var oTimer = 0;
        var sResultFileSize = '';
        
        function secondsToTime(secs) { // we will use this function to convert seconds in normal time format
            var hr = Math.floor(secs / 3600);
            var min = Math.floor((secs - (hr * 3600))/60);
            var sec = Math.floor(secs - (hr * 3600) -  (min * 60));
        
            if (hr < 10) {hr = "0" + hr; }
            if (min < 10) {min = "0" + min;}
            if (sec < 10) {sec = "0" + sec;}
            if (hr) {hr = "00";}
            return hr + ':' + min + ':' + sec;
        };
        
        function bytesToSize(bytes) {
            var sizes = ['Bytes', 'KB', 'MB'];
            if (bytes == 0) return 'n/a';
            var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
            return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
        };
        
        function fileSelected() {
        
            // hide different warnings
            document.getElementById('upload_response').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            document.getElementById('error2').style.display = 'none';
            document.getElementById('abort').style.display = 'none';
            document.getElementById('warnsize').style.display = 'none';
        
            // get selected file element
            
            for(i=0;i<document.getElementById('upload_file').files.length;i++){
               var oFile = document.getElementById('upload_file').files[i];
                // little test for filesize
                //if (oFile.size > iMaxFilesize) {
                //    document.getElementById('warnsize').style.display = 'block';
                //    return;
                //}
            
                // get preview element
                var imageDiv = document.getElementById('preview');
                
                // prepare HTML5 FileReader
                var oReader = new FileReader();
                oReader.onload = function(e){
                    //console.log(e);
                    // e.target.result contains the DataURL which we will use as a source of the image
                    var oImage = document.createElement("img");
                    oImage.width = "300";
                    oImage.height = "300";
                    
                    
                    oImage.src = e.target.result;
                    oImage.style.visibility ="visible";
                    //console.log(oImage.src);
                    
                    oImage.onload = function () { // binding onload event
                        // we are going to display some custom image information here
                        sResultFileSize = bytesToSize(oFile.size);
                        var fileinfo = document.createElement("div");
                        imageDiv.appendChild(fileinfo);
                        fileinfo.appendChild(oImage);
                        fileinfo.style.display = 'block';
                    };
                    
                };
                oReader.readAsDataURL(oFile);
            }     
            // read selected file as DataURL       
        }
        
        function startUploading() {
            // cleanup all temp states
            iPreviousBytesLoaded = 0;
            document.getElementById('upload_response').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            document.getElementById('error2').style.display = 'none';
            document.getElementById('abort').style.display = 'none';
            document.getElementById('warnsize').style.display = 'none';
            document.getElementById('progress_percent').innerHTML = '';
            var oProgress = document.getElementById('progress');
            oProgress.style.display = 'block';
            oProgress.style.width = '0px';
        
            // get form data for POSTing
            //var vFD = document.getElementById('upload_form').getFormData(); // for FF3
            //console.log(document.getElementById('upload_file'));
            
            
            var vFD = new FormData();
            for (i=0;i<document.getElementById('upload_file').files.length;i++){
                vFD.append(""+document.getElementById('upload_file').files.length,document.getElementById('upload_file').files[i]); 
            }
            var oXHR = new XMLHttpRequest();
            oXHR.upload.addEventListener('progress', uploadProgress, true);
            oXHR.upload.addEventListener('load', uploadFinish, true);
            oXHR.upload.addEventListener('error', uploadError, true);
            oXHR.upload.addEventListener('abort', uploadAbort, true);
            oXHR.open('POST', document.URL);
            oXHR.send(vFD);
            
            //console.log(vFD);
            // create XMLHttpRequest object, adding few event listeners, and POSTing our data

        
            // set inner timer
            oTimer = setInterval(doInnerUpdates, 300);
        }
        
        function doInnerUpdates() { // we will use this function to display upload speed
            var iCB = iBytesUploaded;
            var iDiff = iCB - iPreviousBytesLoaded;
        
            // if nothing new loaded - exit
            if (iDiff == 0)
                return;
        
            iPreviousBytesLoaded = iCB;
            iDiff = iDiff * 2;
            var iBytesRem = iBytesTotal - iPreviousBytesLoaded;
            var secondsRemaining = iBytesRem / iDiff;
        
            // update speed info
            var iSpeed = iDiff.toString() + 'B/s';
            if (iDiff > 1024 * 1024) {
                iSpeed = (Math.round(iDiff * 100/(1024*1024))/100).toString() + 'MB/s';
            } else if (iDiff > 1024) {
                iSpeed =  (Math.round(iDiff * 100/1024)/100).toString() + 'KB/s';
            }
        
            document.getElementById('speed').innerHTML = iSpeed;
            document.getElementById('remaining').innerHTML = '| ' + secondsToTime(secondsRemaining);        
        }
        
        function uploadProgress(e) { // upload process in progress
            if (e.lengthComputable) {
                iBytesUploaded = e.loaded;
                iBytesTotal = e.total;
                var iPercentComplete = Math.round(e.loaded * 100 / e.total);
                var iBytesTransfered = bytesToSize(iBytesUploaded);
                
                document.getElementById('progress_percent').innerHTML = iPercentComplete.toString() + '%';
                document.getElementById('progress').style.width = (iPercentComplete * 4).toString() + 'px';
                document.getElementById('b_transfered').innerHTML = iBytesTransfered;
                if (iPercentComplete == 100) {
                    var oUploadResponse = document.getElementById('upload_response');
                    oUploadResponse.innerHTML = '<h1>Please wait...processing</h1>';
                    oUploadResponse.style.display = 'block';
                }
            } else {
                document.getElementById('progress').innerHTML = 'unable to compute';
            }
        }
        
        function uploadFinish(e) { // upload successfully finished
            var oUploadResponse = document.getElementById('upload_response');
            oUploadResponse.innerHTML = e.target.responseText || "Upload Succeed!";
            oUploadResponse.style.display = 'block';
            document.getElementById('progress_percent').innerHTML = '100%';
            document.getElementById('progress').style.width = '400px';
            document.getElementById('filesize').innerHTML = sResultFileSize;
            document.getElementById('remaining').innerHTML = '| 00:00:00';
        
            clearInterval(oTimer);
        }
        
        function uploadError(e) { // upload error
            document.getElementById('error2').style.display = 'block';
            clearInterval(oTimer);
        }  
        
        function uploadAbort(e) { // upload abort
            document.getElementById('abort').style.display = 'block';
            clearInterval(oTimer);
        }
        </script>

    </head>
    <body>
        <header>
        </header>
        <div class="container">
            <div class="contr"><h2>Select the file and click Upload button</h2></div>

            <div class="upload_form_cont">
                <form id="upload_form" method="post" action="method_upload">
                    <div>
                        <div><label for="upload_file">Please select a file</label></div>
                        <div><input type="file" multiple="multiple" name="upload_file" id="upload_file" onchange="fileSelected();" /></div>
                    </div>
                    <div>
                        <input type="button" value="Upload" onclick="startUploading()" />
                    </div>
                    <div id="fileinfo">
                        <div id="filename"></div>
                        <div id="filesize"></div>
                        <div id="filetype"></div>
                        <div id="filedim"></div>
                    </div>
                    <div id="error">You should select valid image files only!</div>
                    <div id="error2">An error occurred while uploading the file</div>
                    <div id="abort">The upload has been canceled by the user or the browser dropped the connection</div>
                    <div id="warnsize">Your file is very big.Keep in mind that larger the file means larger probability to occur errors.</div>

                    <div id="progress_info">
                        <div id="progress"></div>
                        <div id="progress_percent">&nbsp;</div>
                        <div class="clear_both"></div>
                        <div>
                            <div id="speed">&nbsp;</div>
                            <div id="remaining">&nbsp;</div>
                            <div id="b_transfered">&nbsp;</div>
                            <div class="clear_both"></div>
                        </div>
                        <div id="upload_response"></div>
                    </div>
                </form>
                <div id="preview"/>
            </div>
        </div>
    </body>
</html>
'''
DEFAULT_METHOD_UPLOAD_ENC = DEFAULT_METHOD_UPLOAD.encode(DEFAULT_ENC, 'surrogateescape');
# DEFAULT_METHOD_UPLOAD_GZIP = gzip.compress(DEFAULT_METHOD_UPLOAD_ENC);

DEFAULT_METHOD_GIT_CLONE = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>git-clone</title>
        <style type = "text/css">
        .upload_form_cont {
            background: -moz-linear-gradient(#ffffff, #f2f2f2);
            background: -ms-linear-gradient(#ffffff, #f2f2f2);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #ffffff), color-stop(100%, #f2f2f2));
            background: -webkit-linear-gradient(#ffffff, #f2f2f2);
            background: -o-linear-gradient(#ffffff, #f2f2f2);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#f2f2f2');
            -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#f2f2f2')";
            background: linear-gradient(#ffffff, #f2f2f2);

            color:#000;
            overflow:hidden;
        }
        #upload_form {
            float:left;
            padding:5px;
            width:100%;
        }
        #preview {
            background-color:#fff;
            display:block;
            /*float:left;*/
            width:80%;
        }
        #upload_form > div {
            margin-bottom:10px;
        }
        #speed,#remaining {
            float:left;
            width:80%;
        }
        #b_transfered {
            float:right;
            text-align:right;
        }
        .clear_both {
            clear:both;
        }
        input {
            border-radius:10px;
            -moz-border-radius:10px;
            -ms-border-radius:10px;
            -o-border-radius:10px;
            -webkit-border-radius:10px;

            border:1px solid #ccc;
            font-size:14pt;
            padding:5px 10px;
        }
        input[type=button] {
            background: -moz-linear-gradient(#ffffff, #dfdfdf);
            background: -ms-linear-gradient(#ffffff, #dfdfdf);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #ffffff), color-stop(100%, #dfdfdf));
            background: -webkit-linear-gradient(#ffffff, #dfdfdf);
            background: -o-linear-gradient(#ffffff, #dfdfdf);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#dfdfdf');
            -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#dfdfdf')";
            background: linear-gradient(#ffffff, #dfdfdf);
        }
        #upload_file {
            width:90%;
        }
        #progress_info {
            font-size:10pt;
        }
        #fileinfo,#error,#error2,#abort,#warnsize {
            color:#aaa;
            display:none;
            font-size:10pt;
            font-style:italic;
            margin-top:10px;
        }
        #progress {
            border:1px solid #ccc;
            display:none;
            float:left;
            height:14px;

            border-radius:10px;
            -moz-border-radius:10px;
            -ms-border-radius:10px;
            -o-border-radius:10px;
            -webkit-border-radius:10px;

            background: -moz-linear-gradient(#66cc00, #4b9500);
            background: -ms-linear-gradient(#66cc00, #4b9500);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #66cc00), color-stop(100%, #4b9500));
            background: -webkit-linear-gradient(#66cc00, #4b9500);
            background: -o-linear-gradient(#66cc00, #4b9500);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#66cc00', endColorstr='#4b9500');
            -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr='#66cc00', endColorstr='#4b9500')";
            background: linear-gradient(#66cc00, #4b9500);
        }
        #progress_percent {
            float:right;
        }
        #upload_response {
            margin-top: 5px;
            padding: 5px;
            overflow: hidden;
            display: none;
            border: 1px solid #ccc;

            border-radius:10px;
            -moz-border-radius:10px;
            -ms-border-radius:10px;
            -o-border-radius:10px;
            -webkit-border-radius:10px;

            box-shadow: 0 0 5px #ccc;
            background: -moz-linear-gradient(#bbb, #eee);
            background: -ms-linear-gradient(#bbb, #eee);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #bbb), color-stop(100%, #eee));
            background: -webkit-linear-gradient(#bbb, #eee);
            background: -o-linear-gradient(#bbb, #eee);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#bbb', endColorstr='#eee');
            -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr='#bbb', endColorstr='#eee')";
            background: linear-gradient(#bbb, #eee);
        }
        </style>

        <script type="text/javascript" language="javascript">
        // common variables
        var iBytesUploaded = 0;
        var iBytesTotal = 0;
        var iPreviousBytesLoaded = 0;
        var iMaxFilesize = 1048576; // 1MB
        var oTimer = 0;
        var sResultFileSize = '';

        function secondsToTime(secs) { // we will use this function to convert seconds in normal time format
            var hr = Math.floor(secs / 3600);
            var min = Math.floor((secs - (hr * 3600))/60);
            var sec = Math.floor(secs - (hr * 3600) -  (min * 60));

            if (hr < 10) {hr = "0" + hr; }
            if (min < 10) {min = "0" + min;}
            if (sec < 10) {sec = "0" + sec;}
            if (hr) {hr = "00";}
            return hr + ':' + min + ':' + sec;
        };

        function bytesToSize(bytes) {
            var sizes = ['Bytes', 'KB', 'MB'];
            if (bytes == 0) return 'n/a';
            var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
            return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
        };

        function startUploading() {
            // cleanup all temp states
            iPreviousBytesLoaded = 0;
            document.getElementById('upload_response').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            document.getElementById('error2').style.display = 'none';
            document.getElementById('abort').style.display = 'none';
            document.getElementById('warnsize').style.display = 'none';
            document.getElementById('progress_percent').innerHTML = '';
            var oProgress = document.getElementById('progress');
            oProgress.style.display = 'block';
            oProgress.style.width = '0px';

            // get form data for POSTing
            //var vFD = document.getElementById('upload_form').getFormData(); // for FF3
            //console.log(document.getElementById('upload_file'));


            var vFD = new FormData();
            for (i=0;i<document.getElementById('upload_file').files.length;i++){
                vFD.append(""+document.getElementById('upload_file').files.length,document.getElementById('upload_file').files[i]); 
            }
            var oXHR = new XMLHttpRequest();
            oXHR.upload.addEventListener('progress', uploadProgress, true);
            oXHR.upload.addEventListener('load', uploadFinish, true);
            oXHR.upload.addEventListener('error', uploadError, true);
            oXHR.upload.addEventListener('abort', uploadAbort, true);
            oXHR.open('POST', document.URL);
            oXHR.send(vFD);

            //console.log(vFD);
            // create XMLHttpRequest object, adding few event listeners, and POSTing our data


            // set inner timer
            oTimer = setInterval(doInnerUpdates, 300);
        }

        function doInnerUpdates() { // we will use this function to display upload speed
            var iCB = iBytesUploaded;
            var iDiff = iCB - iPreviousBytesLoaded;

            // if nothing new loaded - exit
            if (iDiff == 0)
                return;

            iPreviousBytesLoaded = iCB;
            iDiff = iDiff * 2;
            var iBytesRem = iBytesTotal - iPreviousBytesLoaded;
            var secondsRemaining = iBytesRem / iDiff;

            // update speed info
            var iSpeed = iDiff.toString() + 'B/s';
            if (iDiff > 1024 * 1024) {
                iSpeed = (Math.round(iDiff * 100/(1024*1024))/100).toString() + 'MB/s';
            } else if (iDiff > 1024) {
                iSpeed =  (Math.round(iDiff * 100/1024)/100).toString() + 'KB/s';
            }

            document.getElementById('speed').innerHTML = iSpeed;
            document.getElementById('remaining').innerHTML = '| ' + secondsToTime(secondsRemaining);        
        }

        function uploadProgress(e) { // upload process in progress
            if (e.lengthComputable) {
                iBytesUploaded = e.loaded;
                iBytesTotal = e.total;
                var iPercentComplete = Math.round(e.loaded * 100 / e.total);
                var iBytesTransfered = bytesToSize(iBytesUploaded);

                document.getElementById('progress_percent').innerHTML = iPercentComplete.toString() + '%';
                document.getElementById('progress').style.width = (iPercentComplete * 4).toString() + 'px';
                document.getElementById('b_transfered').innerHTML = iBytesTransfered;
                if (iPercentComplete == 100) {
                    var oUploadResponse = document.getElementById('upload_response');
                    oUploadResponse.innerHTML = '<h1>Please wait...processing</h1>';
                    oUploadResponse.style.display = 'block';
                }
            } else {
                document.getElementById('progress').innerHTML = 'unable to compute';
            }
        }

        function uploadFinish(e) { // upload successfully finished
            var oUploadResponse = document.getElementById('upload_response');
            oUploadResponse.innerHTML = e.target.responseText || "Upload Succeed!";
            oUploadResponse.style.display = 'block';
            document.getElementById('progress_percent').innerHTML = '100%';
            document.getElementById('progress').style.width = '400px';
            document.getElementById('filesize').innerHTML = sResultFileSize;
            document.getElementById('remaining').innerHTML = '| 00:00:00';

            clearInterval(oTimer);
        }

        function uploadError(e) { // upload error
            document.getElementById('error2').style.display = 'block';
            clearInterval(oTimer);
        }  

        function uploadAbort(e) { // upload abort
            document.getElementById('abort').style.display = 'block';
            clearInterval(oTimer);
        }
        </script>

    </head>
    <body>
        <header>
        </header>
        <div class="container">
            <div class="contr"><h2>Input the repo that you want to git-clone.</h2></div>

            <div class="git_clone_form_cont">
                <form id="git_clone_form" method="post" action="method_git_clone">
                    <input type="text" name="git_clone_repo" />
                    <br/>
                    <input type="submit" value="start git-clone">
                </form>
                <div id="preview"/>
            </div>
        </div>
    </body>
</html>
'''
DEFAULT_METHOD_GIT_CLONE_ENC = DEFAULT_METHOD_GIT_CLONE.encode(DEFAULT_ENC, 'surrogateescape');
# DEFAULT_METHOD_GIT_CLONE_GZIP = gzip.compress(DEFAULT_METHOD_UPLOAD_ENC);

DEFAULT_INDEX = '''
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link rel="icon" type="image/png" href="/favicon.png" />
        <style type="text/css">
            html,body{
                font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
                margin:0px;
                padding:0;
                width:100%%;
                height:100%%;
                overflow : auto;
            } 
            body {
                background-color: #888888;
            }
            h1 {
                margin: 0px;
                padding: 0px;
                color : orange;
                font-weight : 800;
                font-size : 80px;
                font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
            }
            h1.subtitle {
                font-size : 30px;
            }
            p.subtitle{
                margin: 0px;
                padding: 0px;
                color : orange;
                font-weight : 800;
                font-size : 30px;
                font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
            }
            div.window {
                font-weight : 800;
                font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
                position: absolute;;padding: 0px;
                margin: 0px;
                /*display: block;*/
                border: 2px solid #000000;
                padding: 0px;
                border-radius: 8px 8px;
                background-color: #FFFFFF;
                width : 400px ;
                height : 600px ;
            }
            .window-title{
                color:#FFFFFF;
                background-color:#404040;
                font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
                font-size:16pt;
                cursor:move; 
                height:20px;
                padding:4px;
            }
            .window-button {
                color:#FFFFFF;
                background-color:#404040;
                font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
                font-size:16pt;
                cursor:move;
                height:20px;
                padding:4px;
            }
            .window-url {
                color:#FFFFFF;
                background-color:#404040;
                font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
                font-size:16pt;
                cursor:move; 
                height:30px;
                padding:4px;
            }
            .window-body {
                font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;
                position: absolute;
                margin: 0px;
                /*display: block;*/
                padding: 0px;
                border-radius: 8px 8px;
                background-color: #FFFFFF;
                overflow : hidden;
                left : 0px;
                right : 0px;
                top : 95px;
                bottom: 0px;
            }
            input[type=button] {
                background: -moz-linear-gradient(#ffffff, #dfdfdf);
                background: -ms-linear-gradient(#ffffff, #dfdfdf);
                background: -webkit-gradient(linear, left top, left bottom, color-stop(0%%, #ffffff), color-stop(100%%, #dfdfdf));
                background: -webkit-linear-gradient(#ffffff, #dfdfdf);
                background: -o-linear-gradient(#ffffff, #dfdfdf);
                filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#dfdfdf');
                -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#dfdfdf')";
                background: linear-gradient(#ffffff, #dfdfdf);
                border-radius: 5px 5px;
            }
        </style>

        <script type="text/javascript">
        //http://www.jb51.net/article/36496.htm
            String.prototype.endWith=function(s){
                if(s==null||s==""||this.length==0||s.length>this.length)
                    return false;
                if(this.substring(this.length-s.length)==s)
                    return true;
                else
                    return false;
                return true;
            }
            String.prototype.startWith=function(s){
                if(s==null||s==""||this.length==0||s.length>this.length)
                    return false;
                if(this.substr(0,s.length)==s)
                    return true;
                else
                    return false;
                return true;
            }
             
            //modified from http://www.cnblogs.com/dolphinX/p/3290520.html
            var Dragging=function(validateHandler){ 
                var draggingObj=null;
                var diffX=0;
                var diffY=0;
                
                function mouseHandler(e){
                    switch(e.type){
                        case 'mousedown':
                            draggingObj=validateHandler(e);//验证是否为可点击移动区域
                            if(draggingObj!=null){
                                diffX=e.clientX-draggingObj.offsetLeft;
                                diffY=e.clientY-draggingObj.offsetTop;
                            }
                            break;
                        
                        case 'mousemove':
                            if(draggingObj){
                                draggingObj.style.left=(e.clientX-diffX)+'px';
                                draggingObj.style.top=(e.clientY-diffY)+'px';
                            }
                            break;
                        
                        case 'mouseup':
                            draggingObj =null;
                            diffX=0;
                            diffY=0;
                            break;
                    }
                };
                
                return {
                    enable:function(){
                        document.addEventListener('mousedown',mouseHandler);
                        document.addEventListener('mousemove',mouseHandler);
                        document.addEventListener('mouseup',mouseHandler);
                    },
                    disable:function(){
                        document.removeEventListener('mousedown',mouseHandler);
                        document.removeEventListener('mousemove',mouseHandler);
                        document.removeEventListener('mouseup',mouseHandler);
                    }
                }
            }

            function getDraggingDialog(e){
                var target=e.target;
                while(target && target.className.indexOf('window-title')==-1){
                    target=target.offsetParent;
                }
                if(target!=null){
                    return target.offsetParent;
                }else{
                    return null;
                }
            }
                
        
            function if_endWith_method(roota){
                if(roota.endWith("/index.html") ||roota.endWith("/method_upload") ||roota.endWith("/method_new_folder") ||roota.endWith("/method_down_all")||roota.endWith("/method_up_all")||roota.endWith("/method_git_clone")){
                    return true;
                }
                return false;
            }
                
            function method_gotomain(){
                 var roota ="/FILE/";
                 document.getElementById("innerframe").src = roota;  
            };
            
            
            function method_back(){
                var roota =  window.frames["innerframe"].document.location.pathname;
                while(roota.endWith("/")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                roota = roota.substring(0,roota.lastIndexOf("/"));
                while(roota.endWith("/")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                roota += "/";
                document.getElementById("innerframe").src = roota;  
            }; 
            
            function method_upload(){
                var roota =  window.frames["innerframe"].document.location.pathname;
                
                if(roota.endWith("//")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                if(if_endWith_method(roota)){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                while(roota.endWith("/")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                roota = roota +"/method_upload";
                document.getElementById("innerframe").src = roota;  
            }; 
            function method_new_folder(){
                var roota = window.frames["innerframe"].document.location.pathname;
                
                if(roota.endWith("//")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                if(if_endWith_method(roota)){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                while(roota.endWith("/")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                roota = roota +"/method_new_folder";
                document.getElementById("innerframe").src = roota;
            }; 
            function method_git_clone(){
                var roota = window.frames["innerframe"].document.location.pathname;
                
                if(roota.endWith("//")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                if(if_endWith_method(roota)){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                while(roota.endWith("/")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                roota = roota +"/method_git_clone";
                document.getElementById("innerframe").src = roota;
            }; 
            function method_down_all(){
                var roota =  window.frames["innerframe"].document.location.pathname;
                if(roota.endWith("//")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                if(if_endWith_method(roota)){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                while(roota.endWith("/")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                roota = roota +"/method_down_all.py";
                document.getElementById("innerframe").src = roota;
            }; 
            function method_up_all(){
                var roota =  window.frames["innerframe"].document.location.pathname;
                if(roota.endWith("//")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                if(if_endWith_method(roota)){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                while(roota.endWith("/")){
                    roota = roota.substring(0,roota.lastIndexOf("/"));
                }
                roota = roota +"/method_up_all.py";
                document.getElementById("innerframe").src = roota;
            }; 

            function keydownEvent() {
                var e = window.event || arguments.callee.caller.arguments[0];
                if (e && e.keyCode == 13 ) {
                    document.getElementById("innerframe").src = location.protocol +"//" + location.host + "/FILE"+document.getElementById("URL").value;
                }
            };

            function bodyInit(){
                document.getElementById("innerframe").src = location.protocol +"//" + location.host + "/FILE/" ;
                
                //if the html is in a inframe, or is on a mobile device.
                if(window.location!=top.location||(/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent))){
                    document.getElementById("titlewords").style.display="none";
                    document.getElementById("mainWindow").style.width="100%%";
                    document.getElementById("mainWindow").style.height="100%%";
                }else{
                    Dragging(getDraggingDialog).enable();
                }
            
            }
            function setURL(strURL){
                document.getElementById("URL").value = strURL ;
            }   
        </script>
        <title>%s</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=2.0, user-scalable=yes" />
    </head>
    <body onload = "bodyInit()">
        <div id="titlewords">%s</div>
        <div id="mainWindow" style = "clear:both" class = "window">
            <div class = "window-title">%s</div>
            <div class = "window-button">
                <input type="button" value = "main" id = "method_gotomain" onclick = "method_gotomain()"/>
                <input type="button" value = "back" id = "method_back" onclick = "method_back()"/>
                <input type="button" value = "upload" id = "method_upload" onclick = "method_upload()"/>
                <input type="button" value = "new-folder" id = "method_new_folder" onclick = "method_new_folder()"/>
                <input type="button" value = "git-clone" id = "git_clone" onclick = "method_git_clone()"/>
                <!--
                    <br/>
                    <input type="button" value = "down-all" id = "method_down_all" onclick = "method_down_all()"/>
                    <input type="button" value = "up-all" id = "method_up_all" onclick = "method_up_all()"/>
                -->
            </div>
            <div class = "window-url">
                <input type="text" name="URL" id ="URL" value="" onKeyDown="keydownEvent()"  style="width:95%%"/>
            </div>
            <div class = "window-body">
                <iframe id = "innerframe" name = "innerframe" target = "_self" frameborder="false"  width = "100%%" height = "100%%" style="border:none;"   allowtransparency="false" scrolling="auto" style="overflow-x:scroll; overflow-y:hidden;"/>
            </div>
        </div>
    </body>
</html>
''' % (DEFAULT_TITLE, DEFAULT_TITLE_WORDS, DEFAULT_TITLE);
DEFAULT_INDEX_ENC = DEFAULT_INDEX.encode(DEFAULT_ENC, 'surrogateescape');
# DEFAULT_INDEX_GZIP = gzip.compress(DEFAULT_INDEX_ENC);
# DEFAULT_METHOD_PY = '''
# MODE = %d;
# CHEKEY = b'%s';
# REQUEST_DIR = '%s';
# SERVER_IP = '%s';
# SERVER_PORT = %d;
# 
# 
# DEFAULT_ENC = 'utf-8';
# CLIENT_DIR = '';
# import socket
# import struct
# import os
# 
# def download():   
#     while(1):
#         b_now_path_len = struct.unpack('i', sock.recv(4))[0];
#         print(b_now_path_len);
#         if(b_now_path_len == -1):
#             break;
#         b_now_path = sock.recv(b_now_path_len);
#         now_path = str(b_now_path, DEFAULT_ENC);
#         print(now_path);
#         now_path = CLIENT_DIR + '/' + now_path;
#         now_dir = os.path.dirname(now_path);
#         print(now_dir);
#         try:
#             os.makedirs(now_dir);
#         except:
#             pass;
#         
#         
#         now_size = struct.unpack('Q', sock.recv(8))[0];
#         print(now_size);
#         now_file = open(now_path, 'wb');
#         
#         while(now_size > 8388608):
#             now_size -= 8388608;
#             now_file.write(sock.recv(8388608));
#             
#         now_file.write(sock.recv(now_size));
#         now_file.close();
#         
# def upload():
#     for each_path in os.walk(CLIENT_DIR):
#         for f in each_path[2]:
#             now_path = os.path.join(each_path[0], f);
#             if(f == 'method_up_all.py'):
#                 continue;
#             now_path_name = now_path[len(CLIENT_DIR):len(now_path)];
#             print(now_path);
#             print(now_path_name);
#             b_now_path_name = bytes(now_path_name, DEFAULT_ENC);
#             b_now_path_name_len = len(b_now_path_name);
#             sock.send(struct.pack('i', b_now_path_name_len));
#             sock.send(b_now_path_name);
#             
#             now_size = os.path.getsize(now_path);
#             print(now_size);
#             sock.send(struct.pack('Q', now_size));
#             
#             now_file = open(now_path, 'rb');
#             
#             file_content = now_file.read(8388608);
#             while(file_content):
#                 sock.send(file_content);
#                 file_content = now_file.read(8388608);
#             now_file.close();
#     sock.send(struct.pack('i', -1));  
# 
# CLIENT_DIR = os.getcwd();
# print(CLIENT_DIR);
# 
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
# sock.connect((SERVER_IP, SERVER_PORT));
# print("CHEKEY");
# sock.send(CHEKEY);
# print(CHEKEY);
# sock.send(struct.pack('I', MODE));
# sock.send(struct.pack('I', len(REQUEST_DIR)));
# sock.send(bytes(REQUEST_DIR, DEFAULT_ENC));
# 
# if(MODE == 0):
#     download();
# elif(MODE == 1):
#     upload();
# ''';

MODE_DEBUG = False;


def DEBUG_PRINT(*strs):
    if (MODE_DEBUG):
        #         print("\033[1;36;41m",end='');
        for stra in strs:
            print(stra, end=' ');
        print();


#         print("\033[0m",end='');

# DEFAULT_ENC_METHOD_DOWN_ALL = DEFAULT_METHOD_DOWN_ALL.encode(DEFAULT_ENC, 'surrogateescape');


def txt_wrap_by(start_str, end_str, html_str):
    '''取出字符串html_str中的，被start_str与end_str包绕的字符串.这个版本和以前不同.将会从头和从尾两端向中间撸.'''
    start = html_str.find(start_str);
    if start >= 0:
        start += len(start_str);

    t_end = html_str[::-1].find(end_str[::-1]);
    if t_end >= 0:
        t_end += len(end_str);
    end = len(html_str) - t_end;
    return html_str[start:end].strip();


def QUICK_START(file_dir=DEFAULT_FILE_DIR, port=DEFAULT_PORT):
    global DEFAULT_PORT;
    global DEFAULT_FILE_DIR
    DEFAULT_PORT = port;
    DEFAULT_FILE_DIR = file_dir;

    try:
        os.makedirs(DEFAULT_FILE_DIR);
    except:
        pass;
    ss = socketserver.ThreadingTCPServer(('', port), EX_SimpleHTTPRequestHandler);
    print("dir %s serving at port %s" % (file_dir, port));
    #     LISTENER = ServerListener();
    #     LISTENER.start();
    ss.serve_forever();


class EX_SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        http.server.SimpleHTTPRequestHandler.__init__(self=self, request=request, client_address=client_address,
                                                      server=server);

    def give_index(self):
        f = io.BytesIO();
        #         f.write(DEFAULT_INDEX_GZIP);
        f.write(DEFAULT_INDEX_ENC);
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % DEFAULT_ENC)
        #         self.send_header("Content-Length", str(len(DEFAULT_ENC_INDEX)))
        #         self.send_header("Content-Encoding", "gzip")
        self.end_headers()
        return f

    def give_robots_txt(self):
        f = io.BytesIO();
        #         f.write(DEFAULT_ROBOTS_TXT_GZIP)
        f.write(DEFAULT_ROBOTS_TXT_ENC)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/txt; charset=%s" % DEFAULT_ENC)
        #         self.send_header("Content-Length", str(len(DEFAULT_ROBOTS_TXT)))
        #         self.send_header("Content-Encoding", "gzip")
        self.end_headers()
        return f

    def give_list_directory_css(self):
        f = io.BytesIO();
        #         f.write(LIST_DIRECTORY_CSS_GZIP)
        f.write(LIST_DIRECTORY_CSS_ENC)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/css; charset=%s" % DEFAULT_ENC)
        #         self.send_header("Content-Length", str(len(DEFAULT_ENC_CSS)))
        #         self.send_header("Content-Encoding", "gzip")
        self.end_headers()
        return f

    def give_method_upload(self):
        f = io.BytesIO();
        #         f.write(DEFAULT_METHOD_UPLOAD_GZIP)
        f.write(DEFAULT_METHOD_UPLOAD_ENC)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % DEFAULT_ENC)
        #         self.send_header("Content-Length", str(len(DEFAULT_ENC_METHOD_UPLOAD)))
        #         self.send_header("Content-Encoding", "gzip")
        self.end_headers()
        return f

    def give_method_git_clone(self):
        f = io.BytesIO();
        #         f.write(DEFAULT_METHOD_UPLOAD_GZIP)
        f.write(DEFAULT_METHOD_GIT_CLONE_ENC)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % DEFAULT_ENC)
        #         self.send_header("Content-Length", str(len(DEFAULT_ENC_METHOD_UPLOAD)))
        #         self.send_header("Content-Encoding", "gzip")
        self.end_headers()
        return f

    def empty_here(self, path):
        DEBUG_PRINT('EMPTY here:', path);
        RETURNED_MESSAGE = '''
                <html>
                   <head/>
                   <body>
                       <h3>No file nor folder here.Here 's empty.Click [new-folder] to creat a folder here:<br/>%s</h3>
                   </body> 
                </html>
                ''' % (self.path[5:]);

        RETURNED_MESSAGE_ENC = RETURNED_MESSAGE.encode(DEFAULT_ENC, 'surrogateescape')

        f = io.BytesIO();
        #         f.write(gzip.compress(RETURNED_MESSAGE_ENC));
        f.write(RETURNED_MESSAGE_ENC);
        f.seek(0);
        self.send_response(200);
        self.send_header("Content-type", "text/html; charset=%s" % DEFAULT_ENC);
        #         self.send_header("Content-Length", str(len(ENC_RETURNED_MESSAGE)));

        self.end_headers();
        return f;

    def give_method_new_folder(self, path):
        DEBUG_PRINT('new FOLDER:', path);
        RETURNED_MESSAGE = '';

        if (not self.path.startswith("/FILE/")):
            return "";

        if (os.path.isdir(path)):
            RETURNED_MESSAGE = '''
            <html>
               <head/>
               <body>
                   <h3>ERROR!You had tried to creat an already-existed folder at:<br/>%s</h3>
               </body> 
            </html>
            ''' % (self.path[5:len(self.path) - len('method_new_folder')]);

        elif (os.path.isfile(path)):
            RETURNED_MESSAGE = '''
            <html>
               <head/>
               <body>
                   <h3>ERROR!You had tried to creat an folder whose path is same to an already-existed file at:<br/>%s</h3>
               </body> 
            </html>
            ''' % (self.path[5:len(self.path) - len('method_new_folder')]);
        else:
            try:
                os.makedirs(path);
                RETURNED_MESSAGE = '''
                <html>
                   <head/>
                   <body>
                       <h3>SUCCESS!You had created a new folder at:<br/>%s</h3>
                   </body> 
                </html>
                ''' % (self.path[5:len(self.path) - len('method_new_folder')]);
            except BaseException:
                RETURNED_MESSAGE = '''
                <html>
                   <head/>
                   <body>
                       <h3>ERROR!You had failed to create a new folder at:<br/>%s</h3>
                   </body> 
                </html>
                ''' % (self.path[5:len(self.path) - len('method_new_folder')]);

        RETURNED_MESSAGE_ENC = RETURNED_MESSAGE.encode(DEFAULT_ENC, 'surrogateescape')

        f = io.BytesIO();
        f.write(RETURNED_MESSAGE_ENC);
        f.seek(0);
        self.send_response(200);
        self.send_header("Content-type", "text/html; charset=%s" % DEFAULT_ENC);
        #         self.send_header("Content-Length", str(len(ENC_RETURNED_MESSAGE)));

        self.end_headers();
        return f;

    #     def give_method_down_all(self):
    #         DEBUG_PRINT('EMPTY here:');
    #         RETURNED_MESSAGE = DEFAULT_METHOD_PY % (0, str(CHEKEY, DEFAULT_ENC), os.path.dirname(self.path), DEFAULT_SERVER_IP, DEFAULT_LISTENER_PORT);
    #         ENC_RETURNED_MESSAGE = RETURNED_MESSAGE.encode(DEFAULT_ENC, 'surrogateescape')
    #
    #         f = io.BytesIO();
    #         f.write(ENC_RETURNED_MESSAGE);
    #         f.seek(0);
    #         self.send_response(200);
    #         self.send_header("Content-type", "code/python3; charset=%s" % DEFAULT_ENC);
    #         self.send_header("Content-Length", str(len(ENC_RETURNED_MESSAGE)));
    #         self.end_headers();
    #         return f;
    #
    #     def give_method_up_all(self):
    #         DEBUG_PRINT('EMPTY here:');
    #         RETURNED_MESSAGE = DEFAULT_METHOD_PY % (1, str(CHEKEY, DEFAULT_ENC), os.path.dirname(self.path), DEFAULT_SERVER_IP, DEFAULT_LISTENER_PORT);
    #         ENC_RETURNED_MESSAGE = RETURNED_MESSAGE.encode(DEFAULT_ENC, 'surrogateescape')
    #
    #         f = io.BytesIO();
    #         f.write(ENC_RETURNED_MESSAGE);
    #         f.seek(0);
    #         self.send_response(200);
    #         self.send_header("Content-type", "code/python3; charset=%s" % DEFAULT_ENC);
    #         self.send_header("Content-Length", str(len(ENC_RETURNED_MESSAGE)));
    #         self.end_headers();
    #         return f;

    def give_ico(self):
        f = io.BytesIO();
        f.write(DEFAULT_ICON)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "image/x-icon")
        #         self.send_header("Content-Length", str(len(DEFAULT_ICON)))
        #         self.send_header("Content-Encoding", "gzip")
        self.end_headers()
        return f

    def _writeheaders(self):
        DEBUG_PRINT("_writeheaders")
        DEBUG_PRINT("self.path", self.path)
        DEBUG_PRINT("self.headers", self.headers)
        self.send_response(200);
        self.send_header('Content-type', 'text/html');
        self.end_headers()

    def printHeaders(self):
        DEBUG_PRINT();
        DEBUG_PRINT();
        DEBUG_PRINT("-----HEADERS_BEGIN-----");
        DEBUG_PRINT(self.headers);
        DEBUG_PRINT("-----HEADERS_END-------");
        DEBUG_PRINT();
        DEBUG_PRINT();

    def do_GET(self):
        """Serve a GET request."""
        DEBUG_PRINT("do_GET");

        self.printHeaders();

        f = self.send_head()
        if f:
            try:
                try:
                    g = gzip.GzipFile(mode="rb", fileobj=f);
                    self.copyfile(g, self.wfile);
                except OSError:
                    f.seek(0);
                    self.copyfile(f, self.wfile);
            finally:
                g.close();
                f.close();

    def do_POST(self):
        DEBUG_PRINT("do_POST");
        DEBUG_PRINT(self.path);
        self.printHeaders();
        if self.path.endswith("method_upload"):
            self.receive_post_method_upload();
        elif self.path.endswith("method_git_clone"):
            self.receive_post_method_git_clone();

    def receive_post_method_upload(self):
        path = self.translate_path(self.path);
        path = path[:len(path) - len("method_upload")];

        DEBUG_PRINT('RAW PATH:', self.path);
        DEBUG_PRINT('TRSLATED PATH:', path);

        if (not self.path.startswith("/FILE/")):
            self.send_error(403, "No permission to upload in this folder!")
            return None

        self._writeheaders();
        remain_bytes = int(self.headers.get('content-length'));

        #         DEBUG_PRINT(self.headers.get('Content-Type').split('boundary=')[1])
        str_boundary = self.headers.get('Content-Type').split('boundary=')[1].strip('-');
        b_boundary = bytes(str_boundary, DEFAULT_ENC);

        DEBUG_PRINT("remain_bytes", remain_bytes);
        DEBUG_PRINT("str_boundary", str_boundary);

        #         index = self.headers.find('boundary=');

        # -----------------------------9158069810016882161586011283\r\n
        now_line = self.rfile.readline();
        remain_bytes -= len(now_line);
        DEBUG_PRINT("now_line", now_line);
        filesum = 1 << 30;
        getfilenum = 0;
        while getfilenum < filesum:
            DEBUG_PRINT("getfilenum", getfilenum);
            getfilenum += 1;
            # Content-Disposition: form-data; name="image_file"; filename="1.txt"\r\n
            now_line = b"";
            now_line = self.rfile.readline();
            remain_bytes -= len(now_line);

            DEBUG_PRINT("NAME_LINE", now_line);
            str_filename = str(txt_wrap_by(b'filename="', b'"', now_line), DEFAULT_ENC);
            if (filesum == (1 << 30)):
                filesum = int(str(txt_wrap_by(b'name="', b'"; filename=', now_line), DEFAULT_ENC))
            DEBUG_PRINT("filesum", filesum);
            #             DEBUG_PRINT("strbname",);
            #             DEBUG_PRINT(str(txt_wrap_by(b'name="', b'"; filename=', now_line), DEFAULT_ENC));
            # Content-Type: text/plain\r\n
            now_line = self.rfile.readline();
            DEBUG_PRINT("firstline", now_line);

            remain_bytes -= len(now_line);
            # \r\n
            now_line = self.rfile.readline();
            remain_bytes -= len(now_line);
            DEBUG_PRINT("secondline", now_line);

            DEBUG_PRINT("path", path);
            DEBUG_PRINT("str_filename", str_filename);
            f = io.BufferedIOBase();
            global DEFAULT_GZIP;
            if (DEFAULT_GZIP == 1):
                f = gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=open(path + str_filename, 'wb'));
            else:
                f = open(path + str_filename, 'wb');

            now_line = b'';
            old_line = self.rfile.readline();
            DEBUG_PRINT("oldline", old_line);
            while 1:
                now_line = old_line;
                old_line = self.rfile.readline();
                #                 DEBUG_PRINT(old_line);
                if (b_boundary in old_line):
                    DEBUG_PRINT("lastline", old_line);
                    DEBUG_PRINT("last2line", now_line);
                    f.write(now_line[:-2]);
                    break;
                f.write(now_line);
            DEBUG_PRINT("FILE_OUTPUT_COMPLETE:", str_filename);
            f.close();
        DEBUG_PRINT("DO_POST_OVER");
        return self.send_head();

    #         return self.send_head();

    #     #modified from http://www.jb51.net/article/57240.htm
    #         print('POST,HEHE');
    #         form = cgi.FieldStorage(
    #             fp=self.rfile,
    #             headers=self.headers,
    #             environ={'REQUEST_METHOD':'POST',
    #                      'CONTENT_TYPE':self.headers['Content-Type'],
    #                      }
    #         )
    #         self.send_response(200)
    #         self.end_headers()
    #         self.wfile.write('Client: %sn ' % str(self.client_address))
    #         self.wfile.write('User-agent: %sn' % str(self.headers['user-agent']))
    #         self.wfile.write('Path: %sn' % self.path)
    #         self.wfile.write('Form data:n')
    #         for field in form.keys():
    #             field_item = form[field]
    #             filename = field_item.filename
    #             filevalue = field_item.value
    #             filesize = len(filevalue)  # 文件大小(字节)
    #             print (len(filevalue))
    #             with open(filename.decode('utf-8') + 'a', 'wb') as f:
    #                 f.write(filevalue)
    #         return

    def receive_post_method_git_clone(self):
        path = self.translate_path(self.path);
        path = path[:len(path) - len("method_git_clone")];

        DEBUG_PRINT('RAW PATH:', self.path);
        DEBUG_PRINT('TRSLATED PATH:', path);

        self._writeheaders();
        remain_bytes = int(self.headers.get('content-length'));

        if remain_bytes >= 10000:
            return None;

        line = self.rfile.read(remain_bytes).decode("utf-8")
        git_repo = urllib.parse.unquote(line[len("git_clone_repo="):]);
        DEBUG_PRINT("git_repo : " + git_repo);

        git_repo_split = git_repo.split("/");
        DEBUG_PRINT(git_repo_split);
        repo_name = git_repo_split[-1];
        if len(repo_name) is 0:
            repo_name = git_repo_split[-2];
        if (repo_name.endswith(".git")):
            repo_name = repo_name[:len(repo_name) - len(".git")]
        DEBUG_PRINT("repo_name : " + repo_name);

        DEBUG_PRINT("path : " + path);
        DEBUG_PRINT("temp folder path : " + path + "__temp__" + repo_name);
        if os.path.isdir(path + "__temp__" + repo_name):
            try:
                shutil.rmtree(path + "__temp__" + repo_name);
            except Exception:
                pass;
        DEBUG_PRINT("zip filepath : " + path + repo_name + ".zip");
        if os.path.isfile(path + repo_name + ".zip"):
            try:
                os.remove(path + repo_name + ".zip");
            except Exception:
                pass;

        if not os.path.isdir(path + "__temp__" + repo_name):
            os.mkdir(path + "__temp__" + repo_name);

        # sysstr = platform.system()
        # if (sysstr == "Windows"):
        #     self.subprocess_cmd(command=[
        #         "cd", path + "__temp__" + repo_name, "&",
        #         "git", "-C", path + "__temp__" + repo_name, "clone", git_repo,
        #     ]);
        # else:

        # self.subprocess_cmd(
        #     [
        #         "git", "clone", git_repo,
        #     ],
        #     path + "__temp__" + repo_name + "/");
        os.system("git clone " + git_repo + " " + path + "__temp__" + repo_name + "/" + repo_name);
        # self.subprocess_cmd(
        #     [
        #         "git", "clone", git_repo,
        #     ],
        # );

        self.zip_dir(path + "__temp__" + repo_name + "/" + repo_name);
        if os.path.isfile(path + "__temp__" + repo_name + "/" + repo_name + ".zip"):
            shutil.move(path + "__temp__" + repo_name + "/" + repo_name + ".zip", path)

        if os.path.isdir(path + "__temp__" + repo_name):
            try:
                shutil.rmtree(path + "__temp__" + repo_name);
            except Exception:
                pass;

        return self.send_head();

    # def subprocess_cmd(self, command, path):
    #     process = subprocess.Popen(command,
    #                                cwd=os.path.dirname(path),
    #                                stdout=subprocess.PIPE,
    #                                stderr=subprocess.PIPE,
    #                                shell=True)
    #     # process.wait();
    #     process.communicate()
    #     DEBUG_PRINT(process);
    #     # DEBUG_PRINT(process.communicate());
    #     # proc_stdout = process.communicate()[0].strip()
    #     # DEBUG_PRINT(proc_stdout);

    def zip_dir(self, dirname):
        zipfilename = dirname + ".zip"
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        else:
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    filelist.append(os.path.join(root, name))

        zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            # print arcname
            zf.write(tar, arcname)
        zf.close()

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller undselfer all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path);

        DEBUG_PRINT('html PATH:', self.path);
        DEBUG_PRINT('real PATH:', path);
        #         DEBUG_PRINT('addr:', self.address_string());

        if (self.path == '/' or self.path == ''):
            return self.give_index();
        #         if(self.path == '/index.html'):
        #             return self.give_index();
        if (self.path == '/robots.txt' or self.path == '/robot.txt'):
            return self.give_robots_txt();
        if (self.path == '/list_directory_css.css'):
            return self.give_list_directory_css();
        if (self.path == '/favicon.png'):
            return self.give_ico();
        if (path.endswith('method_upload')):
            return self.give_method_upload();
        if (path.endswith('method_git_clone')):
            return self.give_method_git_clone();
        #         if(path.endswith('method_down_all.py')):
        #             return self.give_method_down_all();
        #         if(path.endswith('method_up_all.py')):
        #             return self.give_method_up_all();
        if (path.endswith('method_new_folder')):
            return self.give_method_new_folder(path=path[:len(path) - len('method_new_folder')]);

        f = None;
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path);
            if not parts.path.endswith('/'):
                # redirect browser
                self.send_response(301);
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4]);
                new_url = urllib.parse.urlunsplit(new_parts);
                self.send_header("Location", new_url);
                self.end_headers();
                return None;
            #             for index in "index.html", "index.htm":
            #                 index = os.path.join(path, index)
            #                 if os.path.exists(index):
            #                     path = index
            #                     break
            #             else:
            return self.list_directory(path);
        ctype = self.guess_type(path);

        if (not os.path.isfile(path)):
            if (not path.endswith('/')):
                path += '/';
            return self.empty_here(path);

        #         then if here is a file then get it.
        try:
            f = open(path, 'rb');
        except IOError:
            self.send_error(404, "File not found");
            return None
        try:
            self.send_response(200);
            self.send_header("Content-type", ctype);
            fs = os.fstat(f.fileno());
            self.send_header("Content-Length", str(fs[6]));
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime));
            self.end_headers();
            return f;
        except:
            f.close();
            raise

    def do_CONNECT(self):
        return self.send_head();

    def do_OPTIONS(self):
        return self.send_head();

    def do_PROPFIND(self):
        return self.send_head();

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path,
                                               errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath)
        #         title = '路径: %s' % displaypath
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % DEFAULT_ENC)
        r.append('<link type="text/css" rel="stylesheet" href="/list_directory_css.css"/>');
        r.append('<link rel="shortcut icon" type="image/x-icon" href="/favicon.png" />');
        r.append('');
        #         r.append(DEFAULT_JSCRIPT);
        r.append('''
        <script type="text/javascript">
            function sayhi(){
                var urlStr = window.location.pathname;
                //console.log(urlStr);
                urlStr = urlStr.substring(urlStr.indexOf("FILE/")+"FILE/".length-1,urlStr.length);
                //console.log(urlStr);
                parent.setURL(urlStr);
                /*alert(window.location.href);*/
            }
        </script>''');
        r.append('<title>%s</title>\n</head>' % DEFAULT_TITLE)
        r.append('<body onload = "sayhi()" >')
        r.append('<ul>');

        #         如果不在根目录
        if (displaypath != '/FILE/'):

            fatherpath = None;
            for i in range(0, len(displaypath) - 1)[::-1]:
                if (displaypath[i] == '/'):
                    fatherpath = displaypath[:i + 1];
                    break;

            #             DEBUG_PRINT('now user is in displaypath:', displaypath);
            #             DEBUG_PRINT('user can go back fatherpath:', fatherpath);

            if (fatherpath != None):
                r.append('<li class = "link"><a class = "link_in_list" href="%s" target="_self" >%s</a></li>'
                         % (urllib.parse.quote(fatherpath,
                                               errors='surrogatepass'),
                            'GO BACK'));

        for name in list:
            fullname = os.path.join(path, name);
            displayname = linkname = name;
            if os.path.isdir(fullname):
                displayname = name + "/";
                linkname = name + "/";
                r.append('<li class = "folder"><a class = "link_in_list" href="%s" target="_self" >%s</a></li>'
                         % (urllib.parse.quote(linkname,
                                               errors='surrogatepass'),
                            html.escape(displayname)));

        for name in list:
            fullname = os.path.join(path, name);
            displayname = linkname = name;
            if os.path.islink(fullname):
                displayname = name + "@";
                # Note: a link to a directory displays with @ and links with /
                r.append('<li class = "link"><a class = "link_in_list" href="%s" target="_self">%s</a></li>'
                         % (urllib.parse.quote(linkname,
                                               errors='surrogatepass'),
                            html.escape(displayname)));

        for name in list:
            fullname = os.path.join(path, name);
            displayname = linkname = name;
            # Append / for directories or @ for symbolic links
            if os.path.isfile(fullname):
                displayname = name;
                linkname = name;
                r.append('<li class = "file"><a class = "link_in_list" href="%s" target="_blank">%s</a></li>'
                         % (urllib.parse.quote(linkname,
                                               errors='surrogatepass'),
                            html.escape(displayname)));

        r.append('</ul>');
        r.append('</body>');
        r.append('</html>');

        encoded = '\n'.join(r).encode(DEFAULT_ENC, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % DEFAULT_ENC)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

    def translate_path(self, path):
        os.chdir(DEFAULT_FILE_DIR);
        return http.server.SimpleHTTPRequestHandler.translate_path(self, path)


def translate_path(path):
    os.chdir(DEFAULT_FILE_DIR);
    # abandon query parameters
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    # Don't forget explicit trailing slash when normalizing. Issue17324
    trailing_slash = path.rstrip().endswith('/')
    try:
        path = urllib.parse.unquote(path, errors='surrogatepass')
    except UnicodeDecodeError:
        path = urllib.parse.unquote(path)
    path = posixpath.normpath(path)
    words = path.split('/')
    words = filter(None, words)
    path = os.getcwd()
    for word in words:
        drive, word = os.path.splitdrive(word)
        head, word = os.path.split(word)
        if word in (os.curdir, os.pardir): continue
        path = os.path.join(path, word)
    if trailing_slash:
        path += '/'
    return path


# class ServerListener(threading.Thread):
# 
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.thread_stop = False;
#         global DEFAULT_LISTENER_PORT;
#         while(1):
#             try:
#                 self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
#                 self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
#                 self.sock.bind(("0.0.0.0", DEFAULT_LISTENER_PORT));
#                 self.sock.listen(0);
#                 break;
#             except:
#                 DEFAULT_LISTENER_PORT += 1;
#         print("LISTENER:");
#         print(DEFAULT_LISTENER_PORT);
# 
#     def run(self):
#         while True:
#             if(self.thread_stop == True):
#                 self.sock.close();
#                 return
#             client, cltadd = self.sock.accept();
#             ServerDealer(client=client, client_ip=cltadd , listener=self).start();
# 
# 
# class ServerDealer(threading.Thread):
# 
#     def __init__(self, client, listener, client_ip):
#         threading.Thread.__init__(self)
#         self.client = client
#         self.listener = listener
#         self.client_ip = client_ip
#         
#     def run(self):
#         try:     
#             
#             DEBUG_PRINT("here");
#             chekey = self.client.recv(len(CHEKEY));
#             
#             DEBUG_PRINT(chekey);
#             if(chekey != CHEKEY):
#                 return;
#             messagetype = struct.unpack('I', self.client.recv(4))[0];
#             
#             DEBUG_PRINT(messagetype);
#             
#             rawpath_len = struct.unpack('I', self.client.recv(4))[0];
#             
#             DEBUG_PRINT(rawpath_len)
#             rawpath = str(self.client.recv(rawpath_len), DEFAULT_ENC);
#             
#             DEBUG_PRINT(rawpath)
#             
#             realpath = translate_path(rawpath);
#             
#             DEBUG_PRINT("REQUEST_FOLDER");
#             DEBUG_PRINT(realpath);
#             
#             if(messagetype == 0):
#     #             download
#                 for each_path in os.walk(realpath):
#                     for f in each_path[2]:
#                         now_path = os.path.join(each_path[0], f);
#                         now_path_name = now_path[len(realpath):len(now_path)];
#                         
#                         DEBUG_PRINT(now_path);
#                         DEBUG_PRINT(now_path_name);
#                         b_now_path_name = bytes(now_path_name, DEFAULT_ENC);
#                         b_now_path_name_len = len(b_now_path_name);
#                         self.client.send(struct.pack('i', b_now_path_name_len));
#                         self.client.send(b_now_path_name);
#                         
#                         now_size = os.path.getsize(now_path);
#                         
#                         DEBUG_PRINT(now_size);
#                         self.client.send(struct.pack('Q', now_size));
#                         
#                         now_file = open(now_path, 'rb');
#                         
#                         file_content = now_file.read(8388608);
#                         while(file_content):
#                             self.client.send(file_content);
#                             file_content = now_file.read(8388608);
#                         now_file.close();
#                 self.client.send(struct.pack('i', -1));
#                        
#             elif(messagetype == 1):
#     #             upload     
#                 while(1):
#                     b_now_path_len = struct.unpack('i', self.client.recv(4))[0];
#                     
#                     DEBUG_PRINT(b_now_path_len);
#                     if(b_now_path_len == -1):
#                         break;
#                     b_now_path = self.client.recv(b_now_path_len);
#                     now_path = str(b_now_path, DEFAULT_ENC);
#                     
#                     DEBUG_PRINT(now_path);
#                     now_path = realpath + '/' + now_path;
#                     now_dir = os.path.dirname(now_path);
#                     
#                     DEBUG_PRINT(now_dir);
#                     try:
#                         os.makedirs(now_dir);
#                     except:
#                         pass;
#                     
#                     now_size = struct.unpack('Q', self.client.recv(8))[0];
#                     
#                     DEBUG_PRINT(now_size);
#                     now_file = open(now_path, 'wb');
#                     
#                     while(now_size > 8388608):
#                         now_size -= 8388608;
#                         now_file.write(self.client.recv(8388608));
#                         
#                     now_file.write(self.client.recv(now_size));
#                     now_file.close();          
#         
#         except:
#             pass;
#         print("close:", self.client.getpeername())
#     def readline(self):
#         rec = self.inputs.readline()
#         if rec:
#             string = bytes.decode(rec, 'utf-8')
#             if len(string)>2:
#                 string = string[0:-2]
#             else:
#                 string = ' '
#         else:
#             string = False
#         return string


if (__name__ == "__main__"):
    DEFAULT_FILE_DIR = os.getcwd();
    DEBUG_PRINT("received commands:");
    for au in sys.argv:
        DEBUG_PRINT(au);
        au_num = -1;
        try:
            au_num = int(au);
        except:
            pass;
        if (au_num != -1):
            DEFAULT_PORT = au_num;
        else:
            if (au[-len('.py'):] == '.py'):
                pass;
            #                DEFAULT_FILE_DIR = os.path.dirname(au) + '/FILE';

            if (os.path.isdir(au)):
                DEFAULT_FILE_DIR = au;
            elif (au.startswith("dir=")):
                DEFAULT_FILE_DIR = au[-(len(au) - len("dir=")):];
            elif (au.startswith("dir:")):
                DEFAULT_FILE_DIR = au[-(len(au) - len("dir:")):];
            else:
                if (au == "no_gzip"):
                    DEFAULT_GZIP = 0;
                elif (au == "gzip_no"):
                    DEFAULT_GZIP = 0;
                elif (au == "gzip=0"):
                    DEFAULT_GZIP = 0;
                elif (au == "gzip:0"):
                    DEFAULT_GZIP = 0;
                elif (au == "yes_gzip"):
                    DEFAULT_GZIP = 1;
                elif (au == "gzip_yes"):
                    DEFAULT_GZIP = 1;
                elif (au == "gzip=1"):
                    DEFAULT_GZIP = 1;
                elif (au == "gzip:1"):
                    DEFAULT_GZIP = 1;
                elif (au == "gzip"):
                    DEFAULT_GZIP = 1;
                elif (au == "debug"):
                    MODE_DEBUG = True;
                elif (au.startswith("port=")):
                    DEFAULT_PORT = int(au[-(len(au) - len("port=")):]);
                elif (au.startswith("port:")):
                    DEFAULT_PORT = int(au[-(len(au) - len("port:")):]);

    if not os.path.isdir(DEFAULT_FILE_DIR):
        os.mkdir(DEFAULT_FILE_DIR);
    if not os.path.isdir(DEFAULT_FILE_DIR + "/FILE/"):
        os.mkdir(DEFAULT_FILE_DIR + "/FILE/");
    #     print(DEFAULT_FILE_DIR);
    while (1):
        try:
            QUICK_START(DEFAULT_FILE_DIR, DEFAULT_PORT);
        except OSError:
            DEFAULT_PORT += 1;
            pass;
#     QUICK_START("/home/sfeq/FILES", 10001);
