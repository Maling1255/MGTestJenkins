# coding=utf-8

import time
import urllib2
import time
import json
import mimetypes
import os
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

import json
import sys
reload(sys)

sys.setdefaultencoding('utf-8')

#蒲公英应用上传地址
url = 'https://www.pgyer.com/apiv2/app/upload'
#蒲公英提供的 用户Key
userKey = '62b171113265556b695b736b74d904ad'
#蒲公英提供的 API Key
_api_key = '2fc0b3fd44198c558ab8110602552737'
#安装应用时需要输入的密码，这个可不填
installPassword = '1'
_buildInstallType = '2'


# 运行时环境变量字典
environsDict = os.environ
print environsDict

#此次 jenkins 构建版本号
jenkins_build_number = environsDict['BUILD_TAG']
jenkins_build_path = environsDict['WORKSPACE']
jenkins_job_name = environsDict['JOB_NAME']
project_scheme = environsDict['environment']
# jenkins_build_number = 'jenkins-Face2FaceStudent-iOS-812'
# jenkins_build_path = '/Users/open-ci/.jenkins/workspace/Face2FaceStudent-iOS'
# jenkins_job_name = '123456'
# project_scheme = 'FaceTraningForStudentBeta'

print jenkins_build_number

#IPA_PATH="$WORKSPACE/build/${BUILD_TAG}"
#获取 ipa 文件路径
def get_ipa_file_path():
    #工作目录下面的 ipa 文件
    ipa_file_workspace_path = jenkins_build_path + '/build/' + jenkins_build_number + '/' + project_scheme + '.ipa'
    print ipa_file_workspace_path

    if os.path.exists(ipa_file_workspace_path):
        return ipa_file_workspace_path

# while get_ipa_file_path() is None:
#     time.sleep(5)

#ipa 文件路径
ipa_file_path = get_ipa_file_path()
print ipa_file_path

#请求字典编码
def _encode_multipart(params_dict):
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in params_dict.items():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            filename = getattr(v, 'name', '')
            content = v.read()
            decoded_content = content.decode('ISO-8859-1')
            data.append('Content-Disposition: form-data; name="%s"; filename="%s.ipa"' % (k,jenkins_job_name))
            data.append('Content-Type: application/octet-stream\r\n')
            data.append(decoded_content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v if isinstance(v, str) else v.decode('utf-8'))
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary


#处理 蒲公英 上传结果
def handle_resule(result):
    print '*******文件上传成功****'
    json_result = json.loads(result)
    # print (json_result)
    if json_result['code'] is 0:
        print '*******上传返回解析成功****'
        print  json_result
        send_Email(json_result)

#发送邮件
def send_Email(json_result):
    print '*******开始发送邮件****'
    appName = json_result['data']['buildName']
    appKey = json_result['data']['buildKey']
    appVersion = json_result['data']['buildVersion']
    appBuildVersion = json_result['data']['buildBuildVersion']
    appShortcutUrl = json_result['data']['buildShortcutUrl']
    appQRCodeURL = json_result['data']['buildQRCodeURL']
    
    #邮件接受者
    mail_receiver = ['3179769613@qq.com', 'malgee@163.com']
                        
    #根据不同邮箱配置 host，user，和pwd
    mail_host = 'smtp.qq.com'
    mail_port = 25
    mail_user = '951684507@qq.com'
    mail_pwd = 'ubbtqklyrscdbdhc'
    mail_to = ','.join(mail_receiver)
    
    
    environsString = '<h3>本次打包相关信息</h3><p>'
    environsString = '<p><img src="' + appQRCodeURL + '" style="width:150px;height:150px"></p>'
    # environsString += '<p>ipa 包下载地址 : ' + 'wudizhi' + '<p>'
    environsString += '<p>你可从蒲公英网站在线安装 : ' + 'http://www.pgyer.com/' + str(appShortcutUrl) + '   密码 : ' + installPassword + '<p>'
    environsString += '<li><a target="_blank" href="itms-services://?action=download-manifest&url=https://ssl.pgyer.com/app/plist/' + str(appKey) + '">点我直接安装</a></li>'
    message = environsString
    
    # 构建邮件信息
    body = MIMEText(message, _subtype='html', _charset='utf-8')

    msg = MIMEMultipart()
    msg.attach(body)
    msg['subject'] = '最新' + appName + '打包文件:' + jenkins_build_number + '版本号:'+ appVersion
    msg['from'] = mail_user
    msg['To'] = mail_to
    
    try:
        # 发送邮件库
        s = smtplib.SMTP()
        # 设置为调试模式，就是在会话过程中会有输出信息
        s.set_debuglevel(1)
        s.connect(mail_host)
        s.login(mail_user, mail_pwd)
        
        s.sendmail(mail_user, mail_receiver, msg.as_string())
        s.close()
        
        print '*******邮件发送成功****'
    except Exception, e:
        print e

#############################################################
#请求参数字典
params = {
    'userKey': userKey,                 # 用户Key，用来标识当前用户的身份
    '_api_key': _api_key,               # API Key，用来识别API调用者的身份
    'file': open(ipa_file_path, 'rb'),  # 需要上传的ipa或者apk文件
    #'publishRange': '2',
    'buildInstallDate': '2'             # 是否设置安装有效期，值为：1 设置有效时间， 2 长期有效，如果不填写不修改上一次的设置
    'buildPassword': installPassword,   # 设置App安装密码，密码为空时默认公开安装
    'buildInstallType': _buildInstallType #应用安装方式，值为(1,2,3，默认为1 公开安装)。1：公开安装，2：密码安装，3：邀请安装
}

coded_params, boundary = _encode_multipart(params)
req = urllib2.Request(url, coded_params.encode('ISO-8859-1'))
req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
try:
    print '*******开始文件上传****'
    resp = urllib2.urlopen(req)
    body = resp.read().decode('utf-8')
    handle_resule(body)

except urllib2.HTTPError as e:
    print(e.fp.read())

