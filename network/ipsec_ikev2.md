IKEv2协商，两次交换4个数据包  
第一次交换：IKE_SA_INIT，交换IKE_SA的加密和哈希算法，DH公共值和随机数，这两个包是明文，交换过后第一阶段完成产生IKE_SA    
第二次交换：IKE_AUTH，这两个包被IKE_SA保护，交换身份信息，交换CHILD_SA的加密和哈希算法，协商tunnel mode还是transport mode，交换感兴趣流，交换过后第二阶段完成产生第一个CHILD_SA

以下两种情况会进行一次额外的交换：CREAT_CHILD_SA，
发送CHILD_SA密钥更新通告，交换IKE/CHILD_SA的proposal，交换DH公共值和随机数(启用PFS)，交换感兴趣流  
- 如果有其他感兴趣流，会进行CREAT_CHILD_SA交换来产生另一个CHILD_SA
- 老的CHILD_SA的lifetime到期需进行一次CREAT_CHILD_SA交换来产生新的CHILD_SA

```
ikev2 crypto map配置
crypto ikev2 proposal kavo-ikev2-proposal           proposal不用配，系统有默认的，show crypto ikev2 proposal可以看到
 encryption aes-cbc-128 aes-cbc-256
 integrity sha256 sha512
 group 2 5

crypto ikev2 policy kavo-ikev2-policy               policy也不用配，系统有默认的，show crypto ikev2 policy可以看到
 proposal kavo-ikev2-proposal
 					
crypto ikev2 keyring kavo-keyring
 peer fwr-suz-cn-mdf-1
  address 122.1.1.32
  pre-shared-key Bechtel1234

crypto ikev2 profile kavo-ikev2-profile
 match identity remote address 122.1.1.32 255.255.255.255
 identity local address 120.1.1.30
 authentication remote pre-share
 authentication local pre-share
 keyring local kavo-keyring

crypto ipsec transform-set kavo-trans1 esp-des esp-md5-hmac         transform-set也不用配，系统有默认的，show crypto ipsec transform-set可以看到，默认是transport，如果需要tunnel mode才能通，两边也会自动协商成tunnel mode
 mode tunnel
crypto ipsec transform-set kavo-trans2 esp-aes esp-sha-hmac
 mode tunnel

ip access-list extended kavo-vpn-traffic
 10 permit ip 10.249.68.0 0.0.0.255 10.249.90.0 0.0.0.255

crypto map kavo-crypto-map 10 ipsec-isakmp
 set peer 122.1.1.32
 set transform-set kavo-trans1 kavo-trans2          调用transform-set也不用配，系统默认调用了默认的transform-set，show crypto map可以看到
 set ikev2-profile kavo-ikev2-profile
 match address kavo-vpn-traffic

interface GigabitEthernet1
 crypto map kavo-crypto-map

clear crypto ikev2 sa
clear crypto sa

show crypto session
show crypto ikev2 sa
show crypto ipsec sa
```

NAT-T  
- 由于IKEv2天生支持NAT-T，所以peer双方不需要探测对方是否支持NAT-T
- 第一次交换1，2个包，peer双方通过NAT-D探测中间是否有NAT
- 如果探测到中间有NAT存在，第二次交换3，4个包，和后续的ESP包都被封装到UDP4500端口

```
ikev2 SVTI配置
crypto ikev2 keyring kavo-keyring
 peer fwr-suz-cn-mdf-1
  address 122.1.1.32
  pre-shared-key Bechtel1234

crypto ikev2 profile kavo-ikev2-profile
 match identity remote address 122.1.1.32 255.255.255.255
 identity local address 120.1.1.30
 authentication remote pre-share
 authentication local pre-share
 keyring local kavo-keyring

crypto ipsec profile kavo-ipsec-profile
 set ikev2-profile kavo-ikev2-profile           ipsec profile下要调用ikev2-profile和transform-set, transform-set可以省掉，因为默认调用了系统默认的transform-set，show crypto ipsec profile可以看到

interface Tunnel10
 ip address 172.16.1.1 255.255.255.0
 tunnel source GigabitEthernet1
 tunnel mode ipsec ipv4
 tunnel destination 122.1.1.32
 tunnel protection ipsec profile kavo-ipsec-profile

注1：tunnel接口下有tunnel mode ipsec ipv4这句话就是SVTI，没有这句话就是gre over ipsec，还有个区别是gre over ipsec推荐是transport mode，SVTI必须是tunnel mode，虽然默认的transform-set是transport，但两边会自动协商成tunnel
注2：在tunnel接口下敲上tunnel protection ipsec profile这句话，立刻会去找对端协商ipsec，tunnel接口shutdown/no shutdown也会去找对端协商ipsec
```

```
VRF感知的gre over ipsec配置
crypto ikev2 proposal kavo-ikev2-proposal
 encryption aes-cbc-256
 integrity sha512
 group 19

crypto ikev2 policy kavo-ikev2-policy
 match fvrf Front                       proposal和policy都可以省掉不配，但是如果配了，policy下面就必须有match fvrf这句话
 proposal kavo-ikev2-proposal

crypto ikev2 keyring kavo-keyring
 peer fwr-suz-cn-mdf-1
  address 122.1.1.32
  pre-shared-key Bechtel1234

crypto ikev2 profile kavo-ikev2-profile
 match fvrf Front
 match identity remote address 122.1.1.32 255.255.255.255
 identity local address 120.1.1.30
 authentication remote pre-share
 authentication local pre-share
 keyring local kavo-keyring
 dpd 30 3 periodic                      默认启用on-demand DPD
 nat keepalive 30                       默认没有启用，仅当S2S VPN中间有PAT并且不跑动态路由协议的情况下需要配nat keepalive

crypto ipsec profile kavo-ipsec-profile
 set ikev2-profile kavo-ikev2-profile

interface Tunnel10
 ip address 172.16.1.1 255.255.255.0
 tunnel source GigabitEthernet1
 tunnel destination 122.1.1.32
 tunnel vrf Front
 tunnel protection ipsec profile kavo-ipsec-profile
```

```
DMVPN的组件
1. MGRE
2. NHRP
3. 动态路由协议
4. IPSec

VRF感知的DMVPN配置
IKEv2配置
crypto ikev2 keyring kavo-keyring
 peer all-peers
  address 0.0.0.0 0.0.0.0
  pre-shared-key Bechtel1234

crypto ikev2 profile kavo-ikev2-profile
 match fvrf Front
 match identity remote address 0.0.0.0
 identity local address x.x.x.x
 authentication remote pre-share
 authentication local pre-share
 keyring local kavo-keyring

crypto ipsec profile kavo-ipsec-profile
 set ikev2-profile kavo-ikev2-profile

tunnel接口配置
HUB1
interface Tunnel10
 ip address 172.16.1.1 255.255.255.0
 ip nhrp authentication 12345
 ip nhrp map multicast dynamic
 ip nhrp map 172.16.1.2 121.1.1.31
 ip nhrp network-id 10
 ip nhrp holdtime 1800
 ip nhrp registration timeout 300
 tunnel source GigabitEthernet1
 tunnel mode gre multipoint
 tunnel key 10
 tunnel vrf Front
 tunnel protection ipsec profile kavo-ipsec-profile
命令解释：
ip nhrp authentication 12345
可选配置，启用NHRP认证
ip nhrp map multicast dynamic
配置组播转单播，dynamic意思是单播地址现在还不知道，等spoke注册上来，就动态生成组播转单播映射，这条命令是默认的，敲了也不显示，跑BGP不需要这个配置
ip nhrp map 172.16.1.2 121.1.1.31
配置HUB2的NHRP静态映射，否则HUB1没有HUB2的NHRP解析，不会建立隧道，这是因为在HUB上没有ip nhrp nhs这条命令，所以HUB不会去询问未知IP地址的NHRP解析，所以HUB之间要通，就要静态配置对方的NHRP映射(两个HUB在两个不同site的情况要互指，如果两个HUB都是在同一个site就不用互指，因为同一个site的两个HUB建立MGRE隧道没有意义)
ip nhrp network-id 10
激活NHRP，同一个NHRP域敲一样的id(实际上乱打也无所谓)
ip nhrp holdtime 1800
配置NHRP本地映射条目的有效时间为1800秒，HUB超过1800秒没有收到spoke的注册请求，则条目超时失效，spoke上的条目在holdtime超时前，不会主动向nhs查询NHRP解析
ip nhrp registration timeout 300
配置spoke每300秒发送NHRP注册请求到nhs，不配的话默认是holdtime的三分之一
tunnel mode gre multipoint
tunnel模式是MGRE
tunnel key 10
详见下文tunnel key实验总结

HUB2
interface Tunnel10
 ip address 172.16.1.2 255.255.255.0
 ip nhrp authentication 12345
 ip nhrp map multicast dynamic
 ip nhrp map 172.16.1.1 120.1.1.30
 ip nhrp network-id 10
 ip nhrp holdtime 1800
 ip nhrp registration timeout 300
 tunnel source GigabitEthernet1
 tunnel mode gre multipoint
 tunnel key 10
 tunnel vrf Front
 tunnel protection ipsec profile kavo-ipsec-profile

SPOKE
interface Tunnel10
 ip address 172.16.1.100 255.255.255.0
 ip nhrp authentication 12345
 ip nhrp map 172.16.1.1 120.1.1.30
 ip nhrp map multicast 120.1.1.30
 ip nhrp map 172.16.1.2 121.1.1.31
 ip nhrp map multicast 121.1.1.31
 ip nhrp network-id 10
 ip nhrp nhs 172.16.1.1
 ip nhrp nhs 172.16.1.2
 ip nhrp holdtime 1800
 ip nhrp registration timeout 300
 tunnel source GigabitEthernet1
 tunnel mode gre multipoint
 tunnel key 10
 tunnel vrf Front
 tunnel protection ipsec profile kavo-ipsec-profile
命令解释：
ip nhrp map multicast 120.1.1.30
静态映射组播到单播，跑BGP不需要这个配置
ip nhrp nhs 172.16.1.1
spoke周期性发送NHRP注册请求到nhs，当spoke需要解析未知IP地址时发送NHRP解析请求给nhs

show ip nhrp
show dmvpn

clear ip nhrp
```
tunnel key实验    
实验细节：  
路由器A和B用相同的源目global地址建了2个GRE tunnel，tunnel 10和tunnel 20，用ipsec保护(2个tunnel接口调用同一个ipsec profile)，A的内网为10.1.1.0/24，B的内网为10.1.2.0/24，A和B上都配了静态路由去往对方的内网出接口为tunnel 10，所有配置敲完后，ipsec协商成功，show crypto ipsec sa可以看到t10和t20有相同的inbound/outbond spi
1. 两边的t10和t20都不敲tunnel key，通过ping和show interfaces tunnel nn stats发现：去包路径是A:t10——B:t10，回包路径是B:t10——A:t10
2. 尝试把A的t10和B的t20关联起来：A的t10和B的t20配tunnel key 10，A和B都clear counters，通过ping和show interfaces tunnel nn stats发现：去包路径是A:t10——B:t20，回包路径是B:t10——A:t20
3. A的t10和B的t20把tunnel key 10的配置去掉，A和B都clear counters，通过ping和show interfaces tunnel nn stats发现：去包路径是A:t10——B:t20，回包路径是B:t10——A:t10

实验总结：  
在有多个tunnel接口基于同一个源物理接口的情况下，如果所有tunnel接口都不敲tunnel key，那么在IPSec解密以后，明文数据包送到哪个tunnel接口处理几乎是随机的，如果需要保证明文流量从某个tunnel口进来(比如tunnel接口上有配置ACL过滤明文流量)，那就必须配置tunnel key来关联两边的tunnel接口，所以best practice是只要有多个tunnel接口基于同一个源物理接口，就应该配tunnel key  

tunnel key总结：  
tunnel key是GRE头部中的一个字段，路由器通过tunnel key来决定把明文数据包送到哪个tunnel接口处理  

补充说明：    
1. 如果两边的t10都敲tunnel mode ipsec ipv4，这样封装就没有GRE头部了，也就没有地方放tunnel key了，tunnel key随便乱配都能通，可见tunnel key对SVTI的tunnel不起任何作用
2. 后来又做了DMVPN的实验，HUB如果配了两个tunnel接口基于同一个源物理接口，那就必须配tunnel key，否则NHRP不工作，实验证明没有配tunnel key的话，spoke发NHRP注册请求到HUB，HUB不回应，HUB上也不会建立spoke的NHRP映射

NHRP实验  
1. tunnel没有调用ipsec-profile：  
   初始状态spoke1和spoke2都没有彼此的NHRP解析，开始抓包，从spoke1 ping spoke2
   - 观察ping包  
   前2个echo request是spoke1发到HUB，HUB转发到spoke2，echo reply是spoke2发到HUB，HUB转发到spoke1，第3个echo request依然是spoke1发到HUB，HUB转发到spoke2，这时spoke2因为已经收到了spoke1的NHRP解析请求，有了spoke1的NHRP解析，第3个echo reply是spoke2直接发往spoke1，由于spoke2在收到spoke1的NHRP解析请求后给spoke1发了NHRP解析回应，spoke1也有了spoke2的NHRP解析，后续流量就在spoke1和spoke2之间直通
   - 观察NHRP包  
   spoke1在收到第1个echo reply后发NHRP解析请求给HUB，HUB收到后立即转发给spoke2，spoke2在发出第2个echo reply后收到HUB转发来的NHRP解析请求，然后在收到第3个echo request之后，发出NHRP解析回应给spoke1，spoke1在发出第3个echo request还没收到第3个echo reply之前，收到spoke2发来的NHRP解析回应
   
   2022-09-18又做了同样的实验，软件版本：CSR1000V 17.03.04a  
   抓包看从spoke1 ping spoke2  
   spoke1没有把第一个ping包发给HUB，而是直接发NHRP解析请求到HUB，HUB收到解析请求直接转发到spoke2，spoke2收到HUB转发的NHRP解析请求，直接给spoke1发NHRP解析回应，之后ping包在spoke1和spoke2之间直通，第一个ping包掉包了

2. tunnel调用ipsec-profile：  
   从spoke1的身后网络 ping spoke2的身后网络   
   spoke1收到数据包查路由发现下一跳是spoke2的tunnel接口地址，则spoke1先查spoke2的tunnel接口IP的NHRP映射发现没有，spoke1直接向HUB发NHRP解析请求，HUB收到解析请求直接转发给spoke2，spoke2收到HUB转发的NHRP解析请求，发现是spoke1发来的，则创建spoke1的NHRP映射，然后spoke2主动发起和spoke1的ipsec协商，协商完成后建立spoke1和spoke2的ipsec sa，之后spoke2通过直通隧道给spoke1发NHRP解析回应，这样spoke1也有了spoke2的NHRP解析，之后的流量就在spoke1和spoke2之间直通
   
NHRP和ipsec总结：
1. 有对端的NHRP解析，tunnel没有调用ipsec-profile：  
   流量抵达隧道口直接封装GRE和外层IP，GRE隧道就通了
2. 有对端的NHRP解析，tunnel调用了ipsec-profile：  
   本路由器会主动找对方协商ipsec sa，协商完就既有对端的NHRP解析，又有ipsec sa，流量抵达隧道口直接封装GRE和外层IP，并加密插入ESP头部发走
3. 有ipsec sa，但是没有对端的NHRP解析：  
   这种情况发生在HUB1静态配了HUB2的NHRP映射，但是HUB2没有静态指HUB1，由于HUB1会主动找HUB2协商建立ipsec sa，HUB2就有了到HUB1的ipsec sa，但HUB2却没有HUB1的NHRP映射，没有NHRP映射意味着根本无法封装外层IP

DMVPN+eBGP实验总结：  
HUB一个AS，每个SPOKE一个AS，SPOKE1和SPOKE2分别和HUB建eBGP邻居，SPOKE1和SPOKE2之间没有eBGP邻居，SPOKE1和SPOKE2分别network自己身后的网络，所有的配置完成后，在SPOKE1上show ip bgp可以看到SPOKE2身后网络的下一跳是SPOKE2的tunnel接口地址，中间的MA网络天生就优化了路由，HUB和SPOKE也不需要配ip nhrp redirect和ip nhrp shortcut  

Q&A  
1. DMVPN网络拓扑：spoke1-HUB-spoke2，spoke1向HUB询问spoke2的公网IP和隧道口IP的映射，然后会有映射存到本地，holdtime为2小时    
问1：holdtime超时之前每次spoke1和spoke2要通信，是否都需要询问HUB关于spoke2的映射？  
答1：否，spoke在holdtime超时之前不会询问HUB，而是根据本地映射和其他spoke通信  
问2：如果不询问，而是spoke1和spoke2直接通信，如果holdtime超时之前，spoke2的公网IP变了，spoke1如何获悉？  
答2：当spoke2的公网IP发生变化，spoke2会重新去HUB注册，HUB更新spoke2的动态映射，然而spoke1在本地条目的holdtime超时之前无法获悉，只有等holdtime超时才会发NHRP解析请求，或者手动clear ip nhrp，然后重新发起流量来触发NHRP解析请求
2. 问：两个站点建Site-to-Site VPN不跑动态路由协议，tunnel接口有没有必要配IP地址？  
答：实验证明tunnel接口必须配IP地址，否则tunnel不工作，如果静态路由配置下一跳为出接口，那IP地址可以乱敲，不需要两边IP同网段，只要有IP地址就能工作
3. 问：Site-to-Site VPN或者DMVPN，如果跑动态路由协议，DPD还有没有必要？  
答：DPD的目的是为了及时更新SA状态，IKEv2默认启用on-demand DPD，只要其中一边的tunnel接口down，立马会发informational信息通知对端把SA删掉，如果两边都不发包，那DPD包也不发
4. 问：Site-to-Site VPN和DMVPN，不跑动态路由协议，中间有PAT，NAT-T keepalive有没有必要？  
答：实验发现S2S VPN两边在ipsec隧道起来之后是可能一个包都不发的，这样的话等中间设备的PAT条目超时删除后，另一边再发起流量抵达中间设备，由于没有PAT条目就丢包了，所以NAT-T keepalive有必要配，DMVPN没有做实验，DMVPN会周期性的发送NHRP消息，所以我估计不需要

Tips  
1. 当奇怪的问题发生时，有个终极解决方法，把所有HUB和SPOKE的tunnel接口全部shutdown，再从HUB开始依次no shutdown
2. 如果某一个SPOKE起不来，把该SPOKE的所有的tunnel配置和ipsec配置全清掉，再重新配ipsec和tunnel(测试过先配ipsec再配tunnel可以解决问题，先配tunnel再配ipsec还没测)

```
DMVPN模拟SDWAN的配置
网络拓扑：一个HUB两个SPOKE，每个site都有两条internet circuit

HUB
ip vrf Front1
ip vrf Front2

crypto ikev2 keyring hub-keyring
 peer all-peers
  address 0.0.0.0 0.0.0.0
  pre-shared-key Bechtel1234

crypto ikev2 profile t10-t30-ikev2-profile
 match fvrf Front1
 match identity remote address 0.0.0.0
 identity local address 10.1.1.41
 authentication remote pre-share
 authentication local pre-share
 keyring local hub-keyring

crypto ikev2 profile t20-t40-ikev2-profile
 match fvrf Front2
 match identity remote address 0.0.0.0
 identity local address 11.1.1.41
 authentication remote pre-share
 authentication local pre-share
 keyring local hub-keyring

crypto ipsec profile t10-t30-ipsec-profile
 set ikev2-profile t10-t30-ikev2-profile

crypto ipsec profile t20-t40-ipsec-profile
 set ikev2-profile t20-t40-ikev2-profile

interface Loopback192
 ip address 192.168.41.1 255.255.255.0

interface Tunnel10
 ip address 172.16.1.1 255.255.255.0
 ip nhrp network-id 10
 tunnel source GigabitEthernet1
 tunnel mode gre multipoint
 tunnel key 10
 tunnel vrf Front1
 tunnel protection ipsec profile t10-t30-ipsec-profile shared

interface Tunnel20
 ip address 172.16.2.1 255.255.255.0
 ip nhrp network-id 20
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 20
 tunnel vrf Front2
 tunnel protection ipsec profile t20-t40-ipsec-profile shared

interface Tunnel30
 ip address 172.16.3.1 255.255.255.0
 ip nhrp network-id 30
 tunnel source GigabitEthernet1
 tunnel mode gre multipoint
 tunnel key 30
 tunnel vrf Front1
 tunnel protection ipsec profile t10-t30-ipsec-profile shared

interface Tunnel40
 ip address 172.16.4.1 255.255.255.0
 ip nhrp network-id 40
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 40
 tunnel vrf Front2
 tunnel protection ipsec profile t20-t40-ipsec-profile shared

interface GigabitEthernet1
 ip vrf forwarding Front1
 ip address 10.1.1.41 255.255.255.0

interface GigabitEthernet2
 ip vrf forwarding Front2
 ip address 11.1.1.41 255.255.255.0

router bgp 64512
 no bgp default ipv4-unicast
 neighbor 172.16.1.2 remote-as 64513
 neighbor 172.16.1.3 remote-as 64514
 neighbor 172.16.2.2 remote-as 64513
 neighbor 172.16.2.3 remote-as 64514
 neighbor 172.16.3.2 remote-as 64513
 neighbor 172.16.3.3 remote-as 64514
 neighbor 172.16.4.2 remote-as 64513
 neighbor 172.16.4.3 remote-as 64514

 address-family ipv4
  network 192.168.41.0
  neighbor 172.16.1.2 activate
  neighbor 172.16.1.3 activate
  neighbor 172.16.2.2 activate
  neighbor 172.16.2.3 activate
  neighbor 172.16.3.2 activate
  neighbor 172.16.3.3 activate
  neighbor 172.16.4.2 activate
  neighbor 172.16.4.3 activate

ip route 192.168.41.0 255.255.255.0 Null0
ip route vrf Front1 0.0.0.0 0.0.0.0 10.1.1.45
ip route vrf Front2 0.0.0.0 0.0.0.0 11.1.1.45

SPOKE1
ip vrf Front1
ip vrf Front2

crypto ikev2 keyring spoke-keyring
 peer all-peers
  address 0.0.0.0 0.0.0.0
  pre-shared-key Bechtel1234

crypto ikev2 profile t10-t20-ikev2-profile
 match fvrf Front1
 match identity remote address 0.0.0.0
 identity local address 20.1.1.42
 authentication remote pre-share
 authentication local pre-share
 keyring local spoke-keyring

crypto ikev2 profile t30-t40-ikev2-profile
 match fvrf Front2
 match identity remote address 0.0.0.0
 identity local address 21.1.1.42
 authentication remote pre-share
 authentication local pre-share
 keyring local spoke-keyring

crypto ipsec profile t10-t20-ipsec-profile
 set ikev2-profile t10-t20-ikev2-profile

crypto ipsec profile t30-t40-ipsec-profile
 set ikev2-profile t30-t40-ikev2-profile

interface Loopback192
 ip address 192.168.42.1 255.255.255.0

interface Tunnel10
 ip address 172.16.1.2 255.255.255.0
 ip nhrp map 172.16.1.1 10.1.1.41
 ip nhrp network-id 10
 ip nhrp nhs 172.16.1.1
 tunnel source GigabitEthernet1
 tunnel mode gre multipoint
 tunnel key 10
 tunnel vrf Front1
 tunnel protection ipsec profile t10-t20-ipsec-profile shared

interface Tunnel20
 ip address 172.16.2.2 255.255.255.0
 ip nhrp map 172.16.2.1 11.1.1.41
 ip nhrp network-id 20
 ip nhrp nhs 172.16.2.1
 tunnel source GigabitEthernet1
 tunnel mode gre multipoint
 tunnel key 20
 tunnel vrf Front1
 tunnel protection ipsec profile t10-t20-ipsec-profile shared

interface Tunnel30
 ip address 172.16.3.2 255.255.255.0
 ip nhrp map 172.16.3.1 10.1.1.41
 ip nhrp network-id 30
 ip nhrp nhs 172.16.3.1
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 30
 tunnel vrf Front2
 tunnel protection ipsec profile t30-t40-ipsec-profile shared

interface Tunnel40
 ip address 172.16.4.2 255.255.255.0
 ip nhrp map 172.16.4.1 11.1.1.41
 ip nhrp network-id 40
 ip nhrp nhs 172.16.4.1
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 40
 tunnel vrf Front2
 tunnel protection ipsec profile t30-t40-ipsec-profile shared

interface GigabitEthernet1
 ip vrf forwarding Front1
 ip address 20.1.1.42 255.255.255.0

interface GigabitEthernet2
 ip vrf forwarding Front2
 ip address 21.1.1.42 255.255.255.0

router bgp 64513
 no bgp default ipv4-unicast
 neighbor 172.16.1.1 remote-as 64512
 neighbor 172.16.2.1 remote-as 64512
 neighbor 172.16.3.1 remote-as 64512
 neighbor 172.16.4.1 remote-as 64512

 address-family ipv4
  network 192.168.42.0
  neighbor 172.16.1.1 activate
  neighbor 172.16.2.1 activate
  neighbor 172.16.3.1 activate
  neighbor 172.16.4.1 activate

ip route 192.168.42.0 255.255.255.0 Null0
ip route vrf Front1 0.0.0.0 0.0.0.0 20.1.1.45
ip route vrf Front2 0.0.0.0 0.0.0.0 21.1.1.45

SPOKE2
ip vrf Front1
ip vrf Front2

crypto ikev2 keyring spoke-keyring
 peer all-peers
  address 0.0.0.0 0.0.0.0
  pre-shared-key Bechtel1234

crypto ikev2 profile t10-t20-ikev2-profile
 match fvrf Front1
 match identity remote address 0.0.0.0
 identity local address 30.1.1.43
 authentication remote pre-share
 authentication local pre-share
 keyring local spoke-keyring

crypto ikev2 profile t30-t40-ikev2-profile
 match fvrf Front2
 match identity remote address 0.0.0.0
 identity local address 31.1.1.43
 authentication remote pre-share
 authentication local pre-share
 keyring local spoke-keyring

crypto ipsec profile t10-t20-ipsec-profile
 set ikev2-profile t10-t20-ikev2-profile

crypto ipsec profile t30-t40-ipsec-profile
 set ikev2-profile t30-t40-ikev2-profile

interface Loopback192
 ip address 192.168.43.1 255.255.255.0

interface Tunnel10
 ip address 172.16.1.3 255.255.255.0
 ip nhrp map 172.16.1.1 10.1.1.41
 ip nhrp network-id 10
 ip nhrp nhs 172.16.1.1
 tunnel source GigabitEthernet1
 tunnel mode gre multipoint
 tunnel key 10
 tunnel vrf Front1
 tunnel protection ipsec profile t10-t20-ipsec-profile shared

interface Tunnel20
 ip address 172.16.2.3 255.255.255.0
 ip nhrp map 172.16.2.1 11.1.1.41
 ip nhrp network-id 20
 ip nhrp nhs 172.16.2.1
 tunnel source GigabitEthernet1
 tunnel mode gre multipoint
 tunnel key 20
 tunnel vrf Front1
 tunnel protection ipsec profile t10-t20-ipsec-profile shared

interface Tunnel30
 ip address 172.16.3.3 255.255.255.0
 ip nhrp map 172.16.3.1 10.1.1.41
 ip nhrp network-id 30
 ip nhrp nhs 172.16.3.1
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 30
 tunnel vrf Front2
 tunnel protection ipsec profile t30-t40-ipsec-profile shared

interface Tunnel40
 ip address 172.16.4.3 255.255.255.0
 ip nhrp map 172.16.4.1 11.1.1.41
 ip nhrp network-id 40
 ip nhrp nhs 172.16.4.1
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 40
 tunnel vrf Front2
 tunnel protection ipsec profile t30-t40-ipsec-profile shared

interface GigabitEthernet1
 ip vrf forwarding Front1
 ip address 30.1.1.43 255.255.255.0

interface GigabitEthernet2
 ip vrf forwarding Front2
 ip address 31.1.1.43 255.255.255.0

router bgp 64514
 no bgp default ipv4-unicast
 neighbor 172.16.1.1 remote-as 64512
 neighbor 172.16.2.1 remote-as 64512
 neighbor 172.16.3.1 remote-as 64512
 neighbor 172.16.4.1 remote-as 64512

 address-family ipv4
  network 192.168.43.0
  neighbor 172.16.1.1 activate
  neighbor 172.16.2.1 activate
  neighbor 172.16.3.1 activate
  neighbor 172.16.4.1 activate

ip route 192.168.43.0 255.255.255.0 Null0
ip route vrf Front1 0.0.0.0 0.0.0.0 30.1.1.45
ip route vrf Front2 0.0.0.0 0.0.0.0 31.1.1.45
```
