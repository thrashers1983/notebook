```
aaa new-model

aaa group server tacacs+ TACACS_MGMT
 server-private 10.247.163.12 key 2>:$Rynr'K75ZDf$92lh:15l@M
 server-private 10.246.3.12 key 2>:$Rynr'K75ZDf$92lh:15l@M
 ip tacacs source-interface Vlan5

test aaa group TACACS_MGMT yf.sys Kavosybron54321 new-code

aaa authentication login default local group TACACS_MGMT
aaa authorization config-commands
aaa authorization exec default local group TACACS_MGMT 
aaa authorization commands 1 default local group TACACS_MGMT if-authenticated 
aaa authorization commands 15 default local group TACACS_MGMT if-authenticated 
aaa accounting exec default start-stop group TACACS_MGMT
aaa accounting commands 1 default start-stop group TACACS_MGMT
aaa accounting commands 15 default start-stop group TACACS_MGMT
```
- tacacs服务器配好后，建议先测一把，测通了再继续其他配置

- 名字叫default的认证策略和授权策略都已经被默认调用到了vty  
名字叫default的认证策略被默认调用到了console，但是名字叫default的授权策略默认没有调用到console，如果要调用default授权策略到console（不建议这么做，容易被锁在外面），敲这个命令：aaa authorization console

- 默认在configure模式下的命令不做命令授权，也就是说只要进到configure terminal模式下，所有的命令默认都能敲，可以用aaa authorization config-commands这条命令启用configure模式下的命令授权

- 授权的套路：
tacacs授权套路是一问一答，认证过了以后，如果不问，就啥授权都没有，举个例子：  
如果aaa authorization exec不配，就不会主动去询问exec授权，那么如果登录成功（不管是本地用户还是AAA用户），就是1级（哪怕本地用户配了privilege 15，哪怕AAA服务器上的用户授权了15级，都没用，因为NAS没问），只能通过enable进入15级  
如果aaa authorization exec配了，aaa authorization commands没配，那登录成功后，如果是本地用户就找local要exec授权，如果是AAA用户就找tacacs服务器要exec授权，敲命令的时候不会主动去询问命令的授权，当前用户是几级的就能敲几级的命令  
如果aaa authorization commands也配了，那每敲一条命令，都会主动去询问命令授权，本地用户找local询问命令授权，AAA用户找tacacs服务器询问命令授权（前提是这条命令在当前用户等级能敲，如果一个1级用户试图敲15级命令，本来就没权限，就不会询问授权）

- authentication和authorization命令中关于local和tacacs配置的先后顺序：  
如果local在前，先找local，local没有再找tacacs  
如果tacacs在前，先找tacacs，tacacs没有就认证失败/授权失败，不会找local，只有当tacacs不可达，才会找local  
实验1：  
aaa authentication login default local group TACACS_MGMT  
aaa authorization exec default group TACACS_MGMT local  
用本地用户登录会显示授权失败登不进去（因为exec授权的时候会先找tacacs，tacacs找不到就授权失败，根本不会找local）    
实验2：  
aaa authentication login default local group TACACS_MGMT  
aaa authorization exec default local group TACACS_MGMT   
aaa authorization commands 15 default group TACACS_MGMT local  
本地15级用户可以登录成功，但敲命令显示授权失败（因为commands授权的时候会先找tacacs，tacacs找不到就授权失败，根本不会找local）  

- 1级命令和15级命令要做命令授权，其他级别命令不做授权可以随便敲（默认只有0,1,15级有命令，2-14级是用户自定义级别）

- if-authenticated的作用：  
假设已经用AAA用户登录成功正在配置设备，这时候tacacs服务器因为某种原因变得不可达，由于敲的每条命令都要找tacacs服务器询问授权，这时候就授权失败了，敲了if-authenticated意思就是哪怕tacacs服务器不可达，也能授权成功

- aaa accounting exec的start-stop记录登录和退出的时间  
aaa accounting commands的start-stop不知道什么意思

- 1级命令和15级命令要做审计，其他级别命令不做审计
