这是配置导出ipa包的plist文件配置， 在这个plist文件中可以配置多个导出参数

1. 可以手动打一个包导出的就有ExportOptions.plist 文件配置

1.1 路径要放到 /Users/maling/.jenkins/workspace/MGTestJenkins/ExportPlist/下面，（ExportPlist自己创建的路径）而且要和jenkins【配置】导出-exportOptionsPlist 的路径一样
eg: -exportOptionsPlist ExportPlist/${ExportOptionsPList}

2. 或者自己创建一个, plist的内容使用xml格式显示如下：
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>compileBitcode</key>
	<true/>
	<key>method</key>
	<string>development</string>
	<key>provisioningProfiles</key>
	<dict>
		<key>com.xingshulin.abc</key>
		<string>abc_dev</string>
		<key>com.xingshulin.abc.NotificationServiceExtension</key>
		<string>abc-Notification-dev</string>
	</dict>
	<key>signingCertificate</key>
	<string>iPhone Developer</string>
	<key>signingStyle</key>
	<string>manual</string>
	<key>stripSwiftSymbols</key>
	<true/>
	<key>teamID</key>
	<string>yourTeamID</string>
	<key>thinning</key>
	<string><none></string>
</dict>
</plist>
