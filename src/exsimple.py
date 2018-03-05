# -*- coding: UTF-8 -*-
#!/usr/bin/python3 python3
VERSION = "2018/03/05";
DEFAULT_SERVER_IP = '127.0.0.1';
# change it by yourself!!!
# because pooooor python can never get an IP from computer.

import html
import http.server
import io
import os
import socketserver
import sys
import urllib.parse
import base64
from builtins import type
import cgi
import gzip
import copy
import threading
import socket
import struct
import posixpath

# -----SETTING_BEGIN-------

DEFAULT_PORT = 80;
DEFAULT_LISTENER_PORT = 11235;

CHEKEY = bytes(VERSION, encoding = "utf8")

DEFAULT_FILE_DIR = '/home';
DEFAULT_GZIP = 0;

# -----SETTING_END-------

# DEFAULT_ENC = sys.getfilesystemencoding();
DEFAULT_ENC = 'utf-8';

DEFAULT_ROBOTS_TXT = 'User-agent: *\r\nDisallow: /FILE/\r\n'

DEFAULT_ENC_ROBOTS_TXT = DEFAULT_ROBOTS_TXT.encode(DEFAULT_ENC, 'surrogateescape');

DEFAULT_CSS = '''
<style type="text/css">
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
</style>
'''

DEFAULT_ENC_CSS = DEFAULT_CSS.encode(DEFAULT_ENC, 'surrogateescape')
DEFAULT_ICON_B64 = 'AAABAAMAEBAAAAEAIABoBAAANgAAACAgAAABACAAqBAAAJ4EAAAwMAAAAQAgAKglAABGFQAAKAAAABAAAAAgAAAAAQAgAAAAAABABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAHQAAADUAAABCAAAARwAAAEUAAAA4AAAAHwAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP9DxTDnT+swv0v33JtD//xzM//8Zx/rYEpfAewAAADsAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE7e/fdE2///Otj//zDU//8m0P///////xvL/fcAAABAAAAAHAAAAAkAAAAFAAAAAQAAAAIAAAAJAAAAEwAAABJY4///Tt///0Tb//861///MNP//yXQ//8czP//AAAAQQAAADUAAAAsAAAAHgAAAAsAAAAIAAAAIQAAADwAAAA1Yuf//1jj//9O3///PcfoqjTF66kqwuupIb7rqRi766kYu+upEpvGeQAAAEEAAAAgo3VAb6JzPfeccDr/AAAAS2zr//9i5///WOP//07f//9D2///Odf//y/T//8kz///HMz//xzM//8SmsJ6AAAANK59Q9eoeUH/oXQ9/0syHFtv4/WzbOv//2Hn//9X4///Td///0Pb//851///LtP//yTP//8czP//GsHzwgAAAEGygUb3rX1E/6Z4QP+RZzaqAAAATm7h8qZq6f33Yeb//1fj//9N3///Qtv//zjX//8u0///JM///xvL/fcAAABHuYdK/7KBR/+rfEP/pXY//5NpNrZFMRtcAAAATAAAAEgAAABHAAAAQUXD4mtB2f33ONf//y3T//8jz///AAAARr6LTf+3hUn/sIBG/6p7Qv+jdT7/nHA7/5ZqN/+UaTb/kmg194dgMrYAAABPRc7siELa//831v//LdP//wAAAD3Dj1D/vIlM/7WESP+vf0X/qHlB/6F0Pf+bbzr/lGk2/5RpNv+UaTb/h2AytgAAAENL3v//Qdr//zbV/e0AAAAkxpFSvcGNT/+7iEv/tINI/619RP+meED/oHM9/5ltOf+UaTb/lGk2/5RpNv8AAABIVeL//0rd/fc+1fmCAAAACgAAAADEj05+v4pMoLaFSKGtfUOjoXQ9p5ZsOaqQZjaql2w4/5Rp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'
DEFAULT_ICON = base64.b64decode(DEFAULT_ICON_B64);
DEFAULT_TITLE = 'EXsimple';
DEFAULT_JSCRIPT = '''
        <script type="text/javascript">
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
            
            Dragging(getDraggingDialog).enable();
        </script>
'''

DEFAULT_METHOD_UPLOAD = '''
<html lang="en" >
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
    var oFile = document.getElementById('upload_file').files[0];


    // little test for filesize
    if (oFile.size > iMaxFilesize) {
        document.getElementById('warnsize').style.display = 'block';
        return;
    }

    // get preview element
    var oImage = document.getElementById('preview');

    // prepare HTML5 FileReader
    var oReader = new FileReader();
        oReader.onload = function(e){

        // e.target.result contains the DataURL which we will use as a source of the image
        oImage.src = e.target.result;

        oImage.onload = function () { // binding onload event

            // we are going to display some custom image information here
            sResultFileSize = bytesToSize(oFile.size);
            document.getElementById('fileinfo').style.display = 'block';
            document.getElementById('filename').innerHTML = 'Name: ' + oFile.name;
            document.getElementById('filesize').innerHTML = 'Size: ' + sResultFileSize;
            document.getElementById('filetype').innerHTML = 'Type: ' + oFile.type;
            document.getElementById('filedim').innerHTML = 'Dimension: ' + oImage.naturalWidth + ' x ' + oImage.naturalHeight;
        };
    };

    // read selected file as DataURL
    oReader.readAsDataURL(oFile);
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
    var vFD = new FormData(document.getElementById('upload_form')); 

    // create XMLHttpRequest object, adding few event listeners, and POSTing our data
    var oXHR = new XMLHttpRequest();        
    oXHR.upload.addEventListener('progress', uploadProgress, false);
    oXHR.addEventListener('load', uploadFinish, false);
    oXHR.addEventListener('error', uploadError, false);
    oXHR.addEventListener('abort', uploadAbort, false);
    oXHR.open('POST', '');
    oXHR.send(vFD);

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
    oUploadResponse.innerHTML = e.target.responseText;
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
                <form id="upload_form" enctype="multipart/form-data" method="post" action="upload.php">
                    <div>
                        <div><label for="upload_file">Please select a file</label></div>
                        <div><input type="file" name="upload_file" id="upload_file" onchange="fileSelected();" /></div>
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
                    <div id="warnsize">Your file is very big. We can't accept it. Please select more small file</div>

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

                <img id="preview" />
            </div>
        </div>
    </body>
</html>
'''
DEFAULT_ENC_METHOD_UPLOAD = DEFAULT_METHOD_UPLOAD.encode(DEFAULT_ENC, 'surrogateescape');

DEFAULT_INDEX = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="shortcut icon" type="image/x-icon" href="/FILE/favicon.ico" mce_href="/FILE/favicon.ico"/>

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
    height:50px;
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
    top : 125px;
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
            
            Dragging(getDraggingDialog).enable();
        
        function if_endWith_method(roota){
            if(roota.endWith("/index.html") ||roota.endWith("/method_upload") ||roota.endWith("/method_new_folder") ||roota.endWith("/method_down_all")||roota.endWith("/method_up_all")){
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
       
        
        function inininin(){
            document.getElementById("innerframe").src = location.protocol +"//" + location.host + "/FILE/" ;
        }
        function setURL(strURL){
            document.getElementById("URL").value = strURL ;
        }
        
        </script>

<title>%s</title>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<script>
  (adsbygoogle = window.adsbygoogle || []).push({
    google_ad_client: "ca-pub-6228761866839926",
    enable_page_level_ads: true
  });
</script>
</head>
<body  onload = "inininin()">
<h1>%s</h1>
<h1 class = "subtitle">convenient way to set up a simple file-server , provided by XenoAmess.</h1>
<h1 class = "subtitle">github : <a target="_blank" href="https://github.com/XenoAmess/EXsimple">https://github.com/XenoAmess/EXsimple/</a></h1>
<div style = "clear:both" class = "window">
<div class = "window-title">%s</div>
<div class = "window-button">
            <input type="button" value = "main" id = "method_gotomain" onclick = "method_gotomain()"/>
            <input type="button" value = "back" id = "method_back" onclick = "method_back()"/>
            <input type="button" value = "upload" id = "method_upload" onclick = "method_upload()"/>
            <input type="button" value = "new-folder" id = "method_upload" onclick = "method_new_folder()"/>
            <br/>
            <input type="button" value = "down-all" id = "method_down_all" onclick = "method_down_all()"/>
            <input type="button" value = "up-all" id = "method_up_all" onclick = "method_up_all()"/>
</div>
<div class = "window-url">
<input type="text" name="URL" id ="URL" value="" onKeyDown="keydownEvent()"  style="width:95%%"/>
</div>
<div class = "window-body">
<iframe id = "innerframe" name = "innerframe" target = "_self" frameborder="false"  width = "100%%" height = "100%%" style="border:none;"   allowtransparency="false">
</iframe>   
</div>
</div>
</body>
</html>
''' % (DEFAULT_TITLE,DEFAULT_TITLE,DEFAULT_TITLE)

DEFAULT_ENC_INDEX = DEFAULT_INDEX.encode(DEFAULT_ENC, 'surrogateescape');

DEFAULT_METHOD_PY = '''
MODE = %d;
CHEKEY = b'%s';
REQUEST_DIR = '%s';
SERVER_IP = '%s';
SERVER_PORT = %d;


DEFAULT_ENC = 'utf-8';
CLIENT_DIR = '';
import socket
import struct
import os

def download():   
    while(1):
        b_now_path_len = struct.unpack('i', sock.recv(4))[0];
        print(b_now_path_len);
        if(b_now_path_len == -1):
            break;
        b_now_path = sock.recv(b_now_path_len);
        now_path = str(b_now_path, encoding=DEFAULT_ENC);
        print(now_path);
        now_path = CLIENT_DIR + '/' + now_path;
        now_dir = os.path.dirname(now_path);
        print(now_dir);
        try:
            os.makedirs(now_dir);
        except:
            pass;
        
        
        now_size = struct.unpack('Q', sock.recv(8))[0];
        print(now_size);
        now_file = open(now_path, 'wb');
        
        while(now_size > 8388608):
            now_size -= 8388608;
            now_file.write(sock.recv(8388608));
            
        now_file.write(sock.recv(now_size));
        now_file.close();
        
def upload():
    for each_path in os.walk(CLIENT_DIR):
        for f in each_path[2]:
            now_path = os.path.join(each_path[0], f);
            if(f == 'method_up_all.py'):
                continue;
            now_path_name = now_path[len(CLIENT_DIR):len(now_path)];
            print(now_path);
            print(now_path_name);
            b_now_path_name = bytes(now_path_name, encoding=DEFAULT_ENC);
            b_now_path_name_len = len(b_now_path_name);
            sock.send(struct.pack('i', b_now_path_name_len));
            sock.send(b_now_path_name);
            
            now_size = os.path.getsize(now_path);
            print(now_size);
            sock.send(struct.pack('Q', now_size));
            
            now_file = open(now_path, 'rb');
            
            file_content = now_file.read(8388608);
            while(file_content):
                sock.send(file_content);
                file_content = now_file.read(8388608);
            now_file.close();
    sock.send(struct.pack('i', -1));  
        
        
        
        
        
        
         

CLIENT_DIR = os.getcwd();
print(CLIENT_DIR);

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.connect((SERVER_IP, SERVER_PORT));
print("CHEKEY");
sock.send(CHEKEY);
print(CHEKEY);
sock.send(struct.pack('I', MODE));
sock.send(struct.pack('I', len(REQUEST_DIR)));
sock.send(bytes(REQUEST_DIR, encoding=DEFAULT_ENC));

if(MODE == 0):
    download();
elif(MODE == 1):
    upload();
''';

MODE_DEBUG = False;


def DEBUG_PRINT(*strs):
    if(MODE_DEBUG):
#         print("\033[1;36;41m",end='');
        for str in strs:
            print(str, end=' ');
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


def QUICK_START(file_dir=DEFAULT_FILE_DIR , port=DEFAULT_PORT):
    global DEFAULT_PORT;
    global DEFAULT_FILE_DIR
    DEFAULT_PORT = port;
    DEFAULT_FILE_DIR = file_dir;

    try:
        os.makedirs(DEFAULT_FILE_DIR);
    except:
        pass;
    ss = socketserver.ThreadingTCPServer(('', port), EX_SimpleHTTPRequestHandler);
    print ("dir %s serving at port %s" % (file_dir, port));
    LISTENER = ServerListener();
    LISTENER.start();
    ss.serve_forever();


class EX_SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        http.server.SimpleHTTPRequestHandler.__init__(self=self, request=request, client_address=client_address, server=server); 

    def give_index(self):
        f = io.BytesIO();
        f.write(DEFAULT_ENC_INDEX)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % DEFAULT_ENC)
        self.send_header("Content-Length", str(len(DEFAULT_ENC_INDEX)))
        self.end_headers()
        return f
    
    def give_robots_txt(self):
        f = io.BytesIO();
        f.write(DEFAULT_ENC_ROBOTS_TXT)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/txt; charset=%s" % DEFAULT_ENC)
        self.send_header("Content-Length", str(len(DEFAULT_ROBOTS_TXT)))
        self.end_headers()
        return f
    
    def give_css(self):        
        f = io.BytesIO();
        f.write(DEFAULT_ENC_CSS)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/css; charset=%s" % DEFAULT_ENC)
        self.send_header("Content-Length", str(len(DEFAULT_ENC_CSS)))
        self.end_headers()
        return f
    
    def give_method_upload(self):        
        f = io.BytesIO();
        f.write(DEFAULT_ENC_METHOD_UPLOAD)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % DEFAULT_ENC)
        self.send_header("Content-Length", str(len(DEFAULT_ENC_METHOD_UPLOAD)))
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
        
        ENC_RETURNED_MESSAGE = RETURNED_MESSAGE.encode(DEFAULT_ENC, 'surrogateescape')
        
        f = io.BytesIO();
        f.write(ENC_RETURNED_MESSAGE);
        f.seek(0);
        self.send_response(200);
        self.send_header("Content-type", "text/html; charset=%s" % DEFAULT_ENC);
        self.send_header("Content-Length", str(len(ENC_RETURNED_MESSAGE)));
        self.end_headers();
        return f;

    def give_method_new_folder(self, path): 
        DEBUG_PRINT('new FOLDER:', path);
        RETURNED_MESSAGE = '';
        
        if(os.path.isdir(path)):
            RETURNED_MESSAGE = '''
            <html>
               <head/>
               <body>
                   <h3>ERROR!You had tried to creat an already-existed folder at:<br/>%s</h3>
               </body> 
            </html>
            ''' % (self.path[5:len(self.path) - len('method_new_folder')]);

        elif(os.path.isfile(path)):
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
        
        ENC_RETURNED_MESSAGE = RETURNED_MESSAGE.encode(DEFAULT_ENC, 'surrogateescape')
        
        f = io.BytesIO();
        f.write(ENC_RETURNED_MESSAGE);
        f.seek(0);
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % DEFAULT_ENC)
        self.send_header("Content-Length", str(len(ENC_RETURNED_MESSAGE)))
        self.end_headers()
        return f
        
    def give_method_down_all(self):
        DEBUG_PRINT('EMPTY here:');
        RETURNED_MESSAGE = DEFAULT_METHOD_PY % (0, str(CHEKEY, encoding=DEFAULT_ENC), os.path.dirname(self.path), DEFAULT_SERVER_IP, DEFAULT_LISTENER_PORT);
        ENC_RETURNED_MESSAGE = RETURNED_MESSAGE.encode(DEFAULT_ENC, 'surrogateescape')
        
        f = io.BytesIO();
        f.write(ENC_RETURNED_MESSAGE);
        f.seek(0);
        self.send_response(200);
        self.send_header("Content-type", "code/python3; charset=%s" % DEFAULT_ENC);
        self.send_header("Content-Length", str(len(ENC_RETURNED_MESSAGE)));
        self.end_headers();
        return f;
    
    def give_method_up_all(self):
        DEBUG_PRINT('EMPTY here:');
        RETURNED_MESSAGE = DEFAULT_METHOD_PY % (1, str(CHEKEY, encoding=DEFAULT_ENC), os.path.dirname(self.path), DEFAULT_SERVER_IP, DEFAULT_LISTENER_PORT);
        ENC_RETURNED_MESSAGE = RETURNED_MESSAGE.encode(DEFAULT_ENC, 'surrogateescape')
        
        f = io.BytesIO();
        f.write(ENC_RETURNED_MESSAGE);
        f.seek(0);
        self.send_response(200);
        self.send_header("Content-type", "code/python3; charset=%s" % DEFAULT_ENC);
        self.send_header("Content-Length", str(len(ENC_RETURNED_MESSAGE)));
        self.end_headers();
        return f;
    
    def give_ico(self):        
        f = io.BytesIO();
        f.write(DEFAULT_ICON)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "image/x-icon")
        self.send_header("Content-Length", str(len(DEFAULT_ICON)))
        self.end_headers()
        return f
    
    def _writeheaders(self):
        DEBUG_PRINT (self.path)
        DEBUG_PRINT (self.headers)
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
        self.printHeaders();
        
        f = self.send_head()
        if f:
            try:
                try:
                    g = gzip.GzipFile(mode="rb", fileobj=f);
#                     self.copyfile(g, self.wfile);
                    while 1:
                        buf = g.read(8388608)
                        if not buf:
                            break
                        self.wfile.write(buf)
                except OSError:
                    
                    f.seek(0);
#                     self.copyfile(f, self.wfile);
                    while 1:
                        buf = f.read(8388608)
                        if not buf:
                            break
                        self.wfile.write(buf)
            finally:
                g.close();
                f.close();
                
    def do_POST(self):
        
        self.printHeaders();
            
        path = self.translate_path(self.path);
        path = path[:len(path) - len("method_upload")];
        
        DEBUG_PRINT('RAW PATH:', self.path);
        DEBUG_PRINT('TRSLATED PATH:', path);
        onetime_bytes = 8388608;
        self._writeheaders();
        remain_bytes = int(self.headers.get('content-length'));
        
#         DEBUG_PRINT(self.headers.get('Content-Type').split('boundary=')[1])
        str_boundary = self.headers.get('Content-Type').split('boundary=')[1].strip('-');
        b_boundary = bytes(str_boundary, encoding=DEFAULT_ENC);
        
        DEBUG_PRINT(remain_bytes);
        DEBUG_PRINT(str_boundary);
#         index = self.headers.find('boundary=');
    
#-----------------------------9158069810016882161586011283\r\n         
        now_line = self.rfile.readline();
        remain_bytes -= len(now_line);
# Content-Disposition: form-data; name="image_file"; filename="1.txt"\r\n
        now_line = self.rfile.readline();
        remain_bytes -= len(now_line);
        
        DEBUG_PRINT("NAME_LINE");
        DEBUG_PRINT(now_line);
        str_filename = str(txt_wrap_by(b'filename="', b'"', now_line), encoding=DEFAULT_ENC);
# Content-Type: text/plain\r\n
        now_line = self.rfile.readline();
        remain_bytes -= len(now_line);
# \r\n
        now_line = self.rfile.readline();
        remain_bytes -= len(now_line);
        
        DEBUG_PRINT(path);
        DEBUG_PRINT(str_filename); 
        f = io.BufferedIOBase();
        global DEFAULT_GZIP;
        if(DEFAULT_GZIP == 1):
            f = gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=open(path + str_filename, 'wb'));
        else:
            f = open(path + str_filename, 'wb');
        
        while(remain_bytes > onetime_bytes * 2):        
            now_line = self.rfile.read(onetime_bytes);
            remain_bytes -= len(now_line);
            f.write(now_line);
            
        pre_line = self.rfile.readline();
        now_line = self.rfile.readline();
        while(not(b_boundary in now_line)):
            f.write(pre_line);
            pre_line = now_line;
            now_line = self.rfile.readline();
          
        DEBUG_PRINT(pre_line[:-2]);
        if(pre_line[-2:] == b'\r\n'):
            pre_line = pre_line[:len(pre_line) - len(b'\r\n')];
        
        DEBUG_PRINT(pre_line);
        
        f.write(pre_line);
        f.close();
        self.send_head();
        
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
        
        if(self.path == '/' or self.path == ''):
            return self.give_index();
#         if(self.path == '/index.html'):
#             return self.give_index();
        if(self.path == '/robots.txt' or self.path == '/robot.txt' ):
            return self.give_robots_txt();
        if(path.endswith('stylesheet.css')):
            return self.give_css();
        if(self.path == '/FILE/favicon.ico'):
            return self.give_ico();
        if(path.endswith('method_upload')):
            return self.give_method_upload();
        if(path.endswith('method_down_all.py')):
            return self.give_method_down_all();
        if(path.endswith('method_up_all.py')):
            return self.give_method_up_all();
        if(path.endswith('method_new_folder')):
            return self.give_method_new_folder(path=path[:len(path) - len('method_new_folder')]);
        
        f = None
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.end_headers()
                return None
#             for index in "index.html", "index.htm":
#                 index = os.path.join(path, index)
#                 if os.path.exists(index):
#                     path = index
#                     break
#             else:
            return self.list_directory(path)
        ctype = self.guess_type(path)
        
        if (not os.path.isfile(path)):
            if (not path.endswith('/')):
                path += '/';
            return self.empty_here(path);
        
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise
    
    def do_CONNECT(self):
        self.printHeaders();
    
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
#         r.append('<link type="text/css" rel="stylesheet" href="stylesheet.css"/>');
        r.append('<link rel="shortcut icon" type="image/x-icon" href="/FILE/favicon.ico" mce_href="/FILE/favicon.ico"/>');
        r.append(DEFAULT_CSS);
        r.append(DEFAULT_JSCRIPT);
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
        if(displaypath != '/FILE/'):
            
            fatherpath = None;
            for i in range(0, len(displaypath) - 1)[::-1]:
                if(displaypath[i] == '/'):
                    fatherpath = displaypath[:i + 1];
                    break;
            
#             DEBUG_PRINT('now user is in displaypath:', displaypath);
#             DEBUG_PRINT('user can go back fatherpath:', fatherpath);
            
            if(fatherpath != None):
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
                r.append('<li class = "file"><a class = "link_in_list" href="%s" target="_blank" >%s</a></li>'
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


class ServerListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False;
        global DEFAULT_LISTENER_PORT;
        while(1):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
                self.sock.bind(("0.0.0.0", DEFAULT_LISTENER_PORT));
                self.sock.listen(0);
                break;
            except:
                DEFAULT_LISTENER_PORT += 1;
        print("LISTENER:");
        print(DEFAULT_LISTENER_PORT);

    def run(self):
        while True:
            if(self.thread_stop == True):
                self.sock.close();
                return
            client, cltadd = self.sock.accept();
            ServerDealer(client=client, client_ip=cltadd , listener=self).start();


class ServerDealer(threading.Thread):

    def __init__(self, client, listener, client_ip):
        threading.Thread.__init__(self)
        self.client = client
        self.listener = listener
        self.client_ip = client_ip
        
    def run(self):
        try:     
            
            DEBUG_PRINT("here");
            chekey = self.client.recv(len(CHEKEY));
            
            DEBUG_PRINT(chekey);
            if(chekey != CHEKEY):
                return;
            messagetype = struct.unpack('I', self.client.recv(4))[0];
            
            DEBUG_PRINT(messagetype);
            
            rawpath_len = struct.unpack('I', self.client.recv(4))[0];
            
            DEBUG_PRINT(rawpath_len)
            rawpath = str(self.client.recv(rawpath_len), encoding=DEFAULT_ENC);
            
            DEBUG_PRINT(rawpath)
            
            realpath = translate_path(rawpath);
            
            DEBUG_PRINT("REQUEST_FOLDER");
            DEBUG_PRINT(realpath);
            
            if(messagetype == 0):
    #             download
                for each_path in os.walk(realpath):
                    for f in each_path[2]:
                        now_path = os.path.join(each_path[0], f);
                        now_path_name = now_path[len(realpath):len(now_path)];
                        
                        DEBUG_PRINT(now_path);
                        DEBUG_PRINT(now_path_name);
                        b_now_path_name = bytes(now_path_name, encoding=DEFAULT_ENC);
                        b_now_path_name_len = len(b_now_path_name);
                        self.client.send(struct.pack('i', b_now_path_name_len));
                        self.client.send(b_now_path_name);
                        
                        now_size = os.path.getsize(now_path);
                        
                        DEBUG_PRINT(now_size);
                        self.client.send(struct.pack('Q', now_size));
                        
                        now_file = open(now_path, 'rb');
                        
                        file_content = now_file.read(8388608);
                        while(file_content):
                            self.client.send(file_content);
                            file_content = now_file.read(8388608);
                        now_file.close();
                self.client.send(struct.pack('i', -1));
                       
            elif(messagetype == 1):
    #             upload     
                while(1):
                    b_now_path_len = struct.unpack('i', self.client.recv(4))[0];
                    
                    DEBUG_PRINT(b_now_path_len);
                    if(b_now_path_len == -1):
                        break;
                    b_now_path = self.client.recv(b_now_path_len);
                    now_path = str(b_now_path, encoding=DEFAULT_ENC);
                    
                    DEBUG_PRINT(now_path);
                    now_path = realpath + '/' + now_path;
                    now_dir = os.path.dirname(now_path);
                    
                    DEBUG_PRINT(now_dir);
                    try:
                        os.makedirs(now_dir);
                    except:
                        pass;
                    
                    now_size = struct.unpack('Q', self.client.recv(8))[0];
                    
                    DEBUG_PRINT(now_size);
                    now_file = open(now_path, 'wb');
                    
                    while(now_size > 8388608):
                        now_size -= 8388608;
                        now_file.write(self.client.recv(8388608));
                        
                    now_file.write(self.client.recv(now_size));
                    now_file.close();          
        
        except:
            pass;
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
    DEBUG_PRINT ("received commands:");
    for au in sys.argv:
        DEBUG_PRINT (au);
        au_num = -1;
        try:
            au_num = int(au);
        except:
            pass; 
        if(au_num != -1):
            DEFAULT_PORT = au_num;
        else:
            if(au[-len('.py'):] == '.py'):
                pass;
#                DEFAULT_FILE_DIR = os.path.dirname(au) + '/FILE';
            
            if(os.path.isdir(au)):
                DEFAULT_FILE_DIR = au;
            elif(au.startswith("dir=")):
                DEFAULT_FILE_DIR = au[-(len(au) - len("dir=")):];
            elif(au.startswith("dir:")):
                DEFAULT_FILE_DIR = au[-(len(au) - len("dir:")):];
            else:
                if(au == "no_gzip"):
                    DEFAULT_GZIP = 0;
                elif(au == "gzip_no"):
                    DEFAULT_GZIP = 0;
                elif(au == "gzip=0"):
                    DEFAULT_GZIP = 0;
                elif(au == "gzip:0"):
                    DEFAULT_GZIP = 0;                                  
                elif(au == "yes_gzip"):
                    DEFAULT_GZIP = 1;
                elif(au == "gzip_yes"):
                    DEFAULT_GZIP = 1;
                elif(au == "gzip=1"):
                    DEFAULT_GZIP = 1;
                elif(au == "gzip:1"):
                    DEFAULT_GZIP = 1;
                elif(au == "gzip"):
                    DEFAULT_GZIP = 1;
                elif(au == "debug"):
                    MODE_DEBUG = True;
                elif(au.startswith("port=")):
                    DEFAULT_PORT = int(au[-(len(au) - len("port=")):]);
                elif(au.startswith("port:")):
                    DEFAULT_PORT = int(au[-(len(au) - len("port:")):]);
                    
    if not os.path.isdir(DEFAULT_FILE_DIR):
        os.mkdir(DEFAULT_FILE_DIR);
    if not os.path.isdir(DEFAULT_FILE_DIR+ "/FILE/"): 
        os.mkdir(DEFAULT_FILE_DIR + "/FILE/");
#     print(DEFAULT_FILE_DIR);
    while(1):
        try:
            QUICK_START(DEFAULT_FILE_DIR, DEFAULT_PORT);
        except OSError:
            DEFAULT_PORT += 1;
            pass;
#     QUICK_START("/home/sfeq/FILES", 10001);

