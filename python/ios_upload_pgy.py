# coding=utf-8

import time
import urllib2
import time
import json
import mimetypes
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_ipa_file_path():
    # 工作目录下面的 ipa 文件
    ipa_file_workspace_path = jenkins_build_path + '/build/' + \
        jenkins_build_number + '/' + project_scheme + '.ipa'
    print ipa_file_workspace_path

    if os.path.exists(ipa_file_workspace_path):
        return ipa_file_workspace_path

# 请求字典编码
def _encode_multipart(params_dict):
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in params_dict.items():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            filename = getattr(v, 'name', '')
            content = v.read()
            decoded_content = content.decode('ISO-8859-1')
            data.append(
                'Content-Disposition: form-data; name="%s"; filename="%s.ipa"' % (k, jenkins_job_name))
            data.append('Content-Type: application/octet-stream\r\n')
            data.append(decoded_content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v if isinstance(v, str) else v.decode('utf-8'))
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary


# 处理 蒲公英 上传结果
def handle_resule(result):
    print '*******文件上传成功****'
    json_result = json.loads(result)
    # print (json_result)
    if json_result['code'] is 0:
        print '*******上传返回解析成功****'
        print json_result
        sendRobot(json_result)


def sendRobot(json_result):
    appName = json_result['data']['buildName']
    appKey = json_result['data']['buildKey']
    appVersion = json_result['data']['buildVersion']
    appBuildVersion = json_result['data']['buildBuildVersion']
    appShortcutUrl = json_result['data']['buildShortcutUrl']
    appQRCodeURL = json_result['data']['buildQRCodeURL']
    buildUpdated = json_result['data']['buildUpdated']
    buildFileSize = round(
        int(json_result['data']['buildFileSize'])/1024.0/1024.0, 1)
    buildFileSize = str(buildFileSize)+"mb"

    gitLogs = ""
    # 获取git log
    with os.popen("git log --oneline -n 5") as l:
        output = l.read()
        gitLogs = "\n>"+output.replace("\n", "\n>")

    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    # 向上2个目录找消息文件
    commnadFile = str(os.path.abspath(os.path.join(os.path.dirname(
        os.path.dirname(dirname)), "f2fRobot.py")))
    msg = msgTemplate.format(
        appName, project_scheme, appVersion, appQRCodeURL, "http://www.pgyer.com/" +
        str(appShortcutUrl), str(
            installPassword), buildUpdated, buildFileSize, git_branches, gitLogs
    )
    msgCommand = commnadFile + " -m \""+msg+"\" -o "+sendOrg+" -t 2"

    print("尝试执行命令："+msgCommand)

    with os.popen("python "+msgCommand) as s:
        print(s.read())


msgTemplate = "### <font color=\"warning\">{}-有新版本发布</font>\n环　　　境：<font color=\"info\">{}</font>\n版　　　本：<font color=\"info\">{}</font>\n二维码地址：[点击打开二维码]({})\n下 载 地 址 ：[点击打开下载页]({})\n安 装 密 码 ：<font color=\"comment\">{}</font>\n上 传 时 间 ：<font color=\"comment\">{}</font>\n文 件 大 小 ：<font color=\"comment\">{}</font>\ngitBranches：<font color=\"comment\">{}</font>\nCommit Logs：\n{}"

# 蒲公英应用上传地址
url = 'https://www.pgyer.com/apiv2/app/upload'
# 蒲公英提供的 用户Key
uKey = '529dac4adaeb7c813c0e3d5399f579d9'
# 蒲公英提供的 API Key
_api_key = 'c12ad62cd793ce1096452b9eed43d4fc'
# 安装应用时需要输入的密码，这个可不填
installPassword = '1'
_buildInstallType = '2'


# 运行时环境变量字典
environsDict = os.environ
print("\n\n↓↓↓↓↓↓↓↓↓↓Jenkins 环境变量↓↓↓↓↓↓↓↓↓↓\n\n")
print environsDict
print("\n\n↑↑↑↑↑↑↑↑↑↑Jenkins 环境变量 ↑↑↑↑↑↑↑↑↑↑\n\n")


# 此次 jenkins 构建版本号
jenkins_build_number = environsDict['BUILD_TAG']
# 根
jenkins_build_path = environsDict['WORKSPACE']
# Job
jenkins_job_name = environsDict['JOB_NAME']
# 环境
project_scheme = environsDict['environment']
# 分支
git_branches = environsDict['git_branches']
# 发送侧
sendOrg = environsDict['sendOrg']

# ipa 文件路径
ipa_file_path = get_ipa_file_path()
#############################################################


# 请求参数字典
params = {
    'uKey': uKey,
    '_api_key': _api_key,
    'file': open(ipa_file_path, 'rb'),
    'publishRange': '2',
    'buildPassword': installPassword,
    'buildInstallType': _buildInstallType
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
