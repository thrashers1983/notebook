eve-ng上安装velocloud三大组件  
https://www.eve-ng.net/index.php/documentation/howtos/vm-ware-velocloud-sd-wan/

cloud-init参考现有的几个文件，生成cdrom.iso，启动镜像即可

用户名密码：  
VCO  
console: vcadmin/Velocloud123  
GUI: super@velocloud.net/vcadm!n

VCG  
console: vcadmin/Velocloud123

VCE  
console: root/Velocloud123

VCO URL:  
https://192.168.1.248/operator  
https://192.168.1.248/ui/operator  
https://192.168.1.248/  
https://192.168.1.248/ui

VCO初始化配置任务：  
https://docs.vmware.com/en/VMware-SD-WAN/5.0/sd-wan-orchestrator-deployment-and-monitoring-guide/GUID-A89C796C-5C72-40DF-B93A-3D5AA591C305.html 
- Configure System Properties  
详见以下链接：  
https://docs.vmware.com/en/VMware-SD-WAN/5.0/sd-wan-orchestrator-deployment-and-monitoring-guide/GUID-D4160743-8286-43F6-A3F8-54401CAAE1A9.html
  - System Name     
  把network.public.address的值改成VCO的FQDN或者管理IP
  ![](images/Screen%20Shot%202022-06-18%20at%2009.46.30.png)
  - Google Maps
  - Twilio
  - MaxMind
  - Email  
- Set up initial operator profile  
  创建一个新的operator profile，起名字，选Segment Based
  ![](images/Screen%20Shot%202022-06-18%20at%2010.10.20.png)
- Set up operator accounts  
  有需要可以创建operator账户
- Create gateways  
  ![](images/Screen%20Shot%202022-06-19%20at%2016.38.10.png)
  创建完会生成一串activation key，后期可以通过手动激活(登录到VCG的console：sudo /opt/vc/bin/activate.py -i -s 192.168.1.248 ZWZ6-KGW6-6LQ7-DFLS)，或者把这串key贴到user-data，VCG启动找到VCO自动激活(VCG开机的时候VCO必须已经启动完成并正常运行)
  ![](images/Screen%20Shot%202022-06-19%20at%2017.13.04.png)
  VCG安装完成后，建议执行以下命令：  
  1. 确认VCG已经激活：  
  /opt/vc/bin/is_activated.py  
  2. 禁用cloud-init，以后每次启动就不会执行cloud-init：  
  sudo touch /etc/cloud/cloud-init.disabled
- Setup gateway pools  
  为每个客户创建一个gateway pool 
  ![](images/Screen%20Shot%202022-06-19%20at%2017.12.20.png)
- Create customer account / partner account  
  创建客户，填带*的(公司名，用户名，密码，分配operator profile，Service Access勾SD-WAN，分配gateway pool，添加license)
  ![](images/Screen%20Shot%202022-06-20%20at%2022.11.04.png)
  创建完新的客户会自动重定向到Customer Configuration页面，也可以在operator portal里点Manage Customers，点击客户链接，进入到customer/enterprise portal，点击Configure > Customer
  ![](images/Screen%20Shot%202022-06-22%20at%2000.08.04.png)

至此初始化配置完成，接下来可以用租户的管理员账号登陆到enterprise portal进行配置

租户配置：  
- 创建一个新的Edge，起名字，选model，选profile，选license，勾上HA
  ![](images/Screen%20Shot%202022-06-22%20at%2008.14.43.png)
  创建完会生成一串activation key，后期可以通过发送email激活，vEdge的话把这串key贴到user-data，vEdge启动会找到VCO自动激活
  ![](images/Screen%20Shot%202022-06-22%20at%2008.20.19.png)
  HA配置：连接第一台vEdge的WAN，先启动第一台vEdge(第二台保持关机)，等第一台激活成功，然后连接第二台vEdge的GE1到第一台vEdge的GE1(仅连接GE1，不要连接其他接口)，等第二台激活成功，HA状态显示正常后，再连接第二台vEdge的WAN  
  注意：vEdge激活后，及时删除cloud-init的iso文件，实验发现在已经激活的vEdge再次启动的时候，如果读取到cloud-init的配置是其他vEdge的配置，会有奇怪的现象

- 创建新的profile，起名字
![](images/Screen%20Shot%202022-06-25%20at%2013.51.38.png)

- 配置profile的Device tab  
Device tab有上下两个部分  
上面这部分是segment可感知的配置
![](images/Screen%20Shot%202022-06-25%20at%2014.29.18.png)
下面这部分是通用配置应用到多个segment(截图不全，下面还有配置)
![](images/Screen%20Shot%202022-06-25%20at%2014.38.05.png)
  - Assign Segments in Profile  
  目前只有Global Segment
  ![](images/Screen%20Shot%202022-06-25%20at%2014.44.18.png)
- Configure Authentication Settings  
  配置登陆Edge的认证
  ![](images/Screen%20Shot%202022-06-25%20at%2014.46.18.png)
