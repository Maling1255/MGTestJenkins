* 开启Jenkins服务

```
$ brew services start jenkins
或者
$ jenkins
```


* 重启Jenkins服务

```
brew services restart jenkins
```

* 通过Url 来关闭/重启Jenkins

```
http://localhost:8080/restart    // 重启
http://localhost:8080/exit			// 关闭
```


* 设置开机启动
```
sudo launchctl load -w /Library/LaunchDaemons/org.jenkins-ci.plist 
```

* 取消开机启动
```
sudo launchctl unload -w /Library/LaunchDaemons/org.jenkins-ci.plist 
```



### 插件
* `Git Parameter` 添加git分支的参数

* 因为我们用的是GitLab来管理源代码，Jenkins本身并没有自带GitLab插件，所以我们需要依次选择 系统管理->管理插件，在*可选插件*中选中 `GitLab Plugin`和`Gitlab Hook Plugin`这两项，然后安装。

* 自动打包的job任务配置也需要添加钥匙串和描述文件, 需要安装`Keychains and Provisioning Profiles Management`插件，安装后在Jenkins首页点击系统管理会找到这个插件，点击进去。

* 如果项目git依赖了其他的项目git，需要添加`Multiple SCMs plugin`插件，可以添加多个git项目地址，（一般来说, Jenkins 一个项目只有一个 SCM, 但 multiple SCMs 这个插件, 允许在工作目录下的任意目录checkout另外的仓库, 这样就(在一定程度上)起到了和 git submodule 相同的作用.）
【这种方式后面的版本废弃，改用git下的Additional Behaviours添加】

* `Post build task` 允许用户根据构建日志输出执行shell/批处理任务, 构建完成后的可以上传到蒲公英之类的，发邮件之类的操作。

* `Xcode integration` 使用xcode 构建，即不是命令行xcodebuild 构建的， 其实底层调用的也是xcodebuild命令构建的

###### git库配置证书，秘钥

* 给远程库添加秘钥[Jenkins+Git源码管理（三）](https://www.cnblogs.com/h--d/p/7002291.html)

* 配置SSH证书。注意此时的ssh应该是切换到jenkins模式下的ssh。生成ssh要把公钥添加到git上，私钥放在jenkins上，jenkins添加证书流程 主页 -> Credentials -> System -> Global credentials(Unrestricted) -> Add Credentials 设置SSH的私钥，同时用cat的形式获取完整的私钥。包括begin 和 end [jenkins 配置](https://www.cnblogs.com/jisa/p/6808507.html)













# 打过过程遇到的问题

##### 1.FATAL: null

First time build. Skipping changelog.
FATAL: null
java.lang.NullPointerException
	at hudson.FilePath.isAbsolute(FilePath.java:309)
	at hudson.FilePath.resolvePathIfRelative(FilePath.java:294)
	at hudson.FilePath.<init>(FilePath.java:285)
	at com.sic.plugins.kpp.KPPKeychainsBuildWrapper.copyKeychainsToWorkspace(KPPKeychainsBuildWrapper.java:119)
	at com.sic.plugins.kpp.KPPKeychainsBuildWrapper.setUp(KPPKeychainsBuildWrapper.java:96)
	at hudson.model.Build$BuildExecution.doRun(Build.java:157)
	at hudson.model.AbstractBuild$AbstractBuildExecution.run(AbstractBuild.java:513)
	at hudson.model.Run.execute(Run.java:1907)
	at hudson.model.FreeStyleBuild.run(FreeStyleBuild.java:43)
	at hudson.model.ResourceController.execute(ResourceController.java:97)
	at hudson.model.Executor.run(Executor.java:429)
	
	
	
	##### 2.  问题

ERROR: Timeout after 10 minutes
ERROR: Error fetching remote repo 'origin'
	
	
	权限问题：1 修改了
	
	
	
Command line invocation:
    /Applications/Xcode.app/Contents/Developer/usr/bin/xcodebuild clean -workspace MGTestJenkinsBeta.xcworkspace -scheme MGTestJenkinsBeta -configuration release

xcodebuild: error: 'MGTestJenkinsBeta.xcworkspace' does not exist.