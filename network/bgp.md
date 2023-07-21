BGP是一个Inter-AS的路由协议，一个路由条目在同一个AS内部传递的时候，其所携带的所有属性都保持不变，在不同AS之间传递的过程中会带上沿途经过的AS号，AS号有2个作用，一是用于eBGP防环，二是用于选路

BGP是TCP封装，单播更新，目标端口179

BGP只增量更新，触发更新

iBGP的AD为200  
eBGP的AD为20

公有ASN: 1-64511  
私有ASN: 64512-65534  
保留ASN: 0和65535

AS类型
- single-homed    
  one link to an external peer
  ![](../images/Screen%20Shot%202022-07-05%20at%2009.10.31.png)
- multi-homed  
  multiple links to one or more external peers
  ![](../images/Screen%20Shot%202022-07-05%20at%2009.11.03.png)
- stub  
  all packets entering the AS are to destinations in the AS  
  all packets leaving the AS are from sources in the AS  
- transit  
  packets entering the AS can be to destinations in another AS, i.e. packets are passing through transit AS
  ![](../images/Screen%20Shot%202022-07-05%20at%2009.17.35.png)

BGP Messages
1. Open  
   TCP连接建立后发送Open消息，Open消息包含：BGP版本号，本地AS号(如果AS号不匹配就协商失败)，hold time(默认180s，如果两边hold time配置不一样，以小的为准)，BGP Identifier(就是BGP router-ID，router-ID是唯一的，必须不能相同)，Optional parameters(包括支持的协议族: ipv4/6，vpnv4/6，l2vpn等等，是否支持route-refresh等等能力)
2. Keepalive   
   BGP session建立后周期性发送Keepalive(默认60s)
3. Update  
   发送路由更新(NLRI)，Withdrawn routes
4. Notification  
   当检测到错误的时候发送Notification断开TCP连接(比如Open消息协商失败，或者邻居发送大量的路由超过本地承载能力，就发Notification断开TCP连接)
5. Route Refresh  
   请求邻居发送路由更新

BGP States
1. Idle  
   BGP初始状态，当在配置中指了邻居以后，就进入Idle状态，开始查找本地路由表有没有去往邻居的路由，当错误发生(Notification消息)，总是会切换到Idle状态
2. Connect  
   如果本地查到去往邻居的路由(必须不能是默认路由)，就进入connect状态，尝试主动建立TCP三次握手
3. Active  
   卡在这个状态表示一直在主动尝试和邻居建立TCP连接，比如两边认证不通过就会卡在Active状态
4. OpenSent  
   TCP建立成功进入OpenSent状态，发送Open消息，并等待邻居的Open消息到来(Idle和Connect状态不一定是两边同步，但是OpenSent状态一定是两边同时进入，因为建立了TCP连接)
5. OpenConfirm  
   收到邻居的Open消息，检查BGP会话参数，匹配通过发送Keepalive进行确认，然后进入到OpenConfirm状态，开始等待自己发送的Open消息被确认，如果参数不匹配，发送Notification断开TCP连接，进入Idle状态
6. Established  
   当收到邻居的Keepalive确认，BGP session建立，进入Established状态

这几个状态中，停留在Idle和Active说明有问题，看到Established就对了，Connect, OpenSent, OpenConfirm都是瞬时状态，瞬间就过去了，几乎看不到这三种状态

BGP防环机制：  
eBGP loop avoidance  
从eBGP邻居收到的路由的AS_PATH中，如果其中有本AS的AS号，则这条路由被丢弃  
iBGP loop avoidance  
从iBGP邻居收到的路由不会发给其他iBGP邻居

```
基本配置：
BGP可以承载多种协议族，也就是address-family，默认开启的address-family是IPv4 unicast，建议配置的时候先关掉默认的IPv4 unicast，在要用的时候再配置
router bgp xxx				                    配置本地AS号
 bgp router-id x.x.x.x			                router-id通常是loopback接口地址
 bgp cluster-id x.x.x.x			                如果本路由器是RR，可以手动配置cluster-id
 no bgp default ipv4-unicast	                关掉默认的IPv4 unicast协议族
 neighbor x.x.x.x remote-as xxx		            指邻居，eBGP通常用直连接口建邻居，iBGP建议用loopback接口建邻居，指对方的loopback接口地址
 neighbor x.x.x.x update-source loopback 0	    指定自己的loopback接口为更新源(指定发起TCP连接的源地址为loopback接口地址)
 neighbor x.x.x.x password xxx                  BGP支持MD5认证，在建立邻居和路由更新的时候都会做认证，MD5值存放在TCP头部的option 19
 neighbor x.x.x.x ebgp-multihop x		        如果eBGP也是用loopback接口建的，或者eBGP peer之间不是直连的，那么要加这条命令指定Outgoing TTL，eBGP邻居默认的Outgoing TTL=1
 neighbor x.x.x.x ttl-security hops x           x限定最大跳数，假设是2，这条命令设置Outgoing TTL=255，Mininum incoming TTL=253(255-2)，也就是说收到的eBGP数据包必须TTL>=253才可以被接收处理(限定了eBGP邻居在距离2跳以内)，这是为了抵御恶意eBGP数据包的攻击(攻击者通常设Outgoing TTL=255，往外发eBGP数据包，由于默认Mininum incoming TTL=0，所以只要收到的eBGP数据包TTL>=0都会被接收处理)，这条命令必须要在两边eBGP邻居都敲上才能生效，且ttl-security和ebgp-multihop是互斥的，两条命令只能敲一条
 neighbor x.x.x.x shutdown			            shutdown邻居
 
 address-family ipv4 unicast			        进入IPv4 unicast协议族
  neighbor x.x.x.x activate			            激活邻居
  neighbor x.x.x.x route-reflector-client	    指定邻居是自己的RR client
  neighbor x.x.x.x next-hop-self			    告诉iBGP邻居下一跳是我(因为BGP是Inter-AS的路由协议，路由条目的属性在iBGP邻居之间传递时不会变，下一跳永远是eBGP邻居)
  neighbor x.x.x.x soft-reconfiguration inbound 向邻居发送route-refresh，请求邻居重新发送一次路由更新，并存储来自这个邻居的路由更新(在所有入方向策略生效之前的路由更新)
  network x.x.x.x mask x.x.x.x			        通告路由，只要路由表里有的路由(包括直连，静态，通过IGP学到的)都可以通告进BGP
  redistribute static                           重分布静态
  redistribute connected                        重分布直连
```

```
show命令：
show ip bgp neighbors
show bgp ipv4 unicast neighbors
show ip bgp summary
show bgp ipv4 unicast summary
show ip bgp
show bgp ipv4 unicast
show ip bgp x.x.x.x
show bgp ipv4 unicast x.x.x.x
show ip bgp neighbors x.x.x.x advertised-routes	显示通告给邻居的路由(在出方向的prefix-list和filter-list生效之后的路由，在出方向的route-map生效之前的路由)
show ip bgp neighbors x.x.x.x received-routes	显示从邻居收到的路由(在所有入方向策略生效之前的路由)
show ip bgp neighbors x.x.x.x routes		    显示从邻居收到的路由(在所有入方向策略生效之后的路由，这些路由已经被放进了本地BGP表)

R1#show bgp ipv4 unicast summary
BGP router identifier 192.168.1.1, local AS number 65501
BGP table version is 1, main routing table version 1

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
192.168.1.2     4        64950      44      44        1    0    0 00:37:00        0

TblVer是邻居的BGP表版本，同一个AS内部所有的iBGP邻居的版本号一致则说明收敛完毕
State显示为空表示进入Established状态
PfxRcd显示从邻居收到的路由条目数

R1#show bgp ipv4 unicast
BGP table version is 26, local router ID is 10.1.255.1
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
              x best-external, a additional-path, c RIB-compressed,
              t secondary path, L long-lived-stale,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.5.0.0/16      10.3.1.2                 0             0 65520 ?
 *>i  10.18.0.0/16     10.1.255.2               0    100      0 65501 i
 *>i  172.16.5.0/24    10.1.255.2               0    100      0 65501 i
 *>   192.168.1.0      10.3.1.2                 0             0 65520 ?
 *>i  192.168.20.0     10.1.255.2               0    100      0 65501 i

*代表这个路由条目是有效的(无效的有：s代表被抑制，h代表历史，r是加表失败)
>代表这个路由条目是最优的，可以放进路由表，并且通告给邻居(如果路由条目不是最优的，则不会放进本地路由表，也不会通告给邻居)，满足最优的条件：下一跳可达
如果一个目标网络从多条路径学到，且都满足最优条件，则必须通过BGP选路原则选出一条最优的路径，放进路由表并通告给邻居
前面的i代表这个条目是从iBGP学到的，前面没有i代表这个条目是从eBGP学到的，后面的i代表这个条目是通过network命令通告的，后面的?代表这个条目是重分布进BGP的
前面的r代表这个条目加入路由表失败(比如这条路由同时从iBGP和IGP学到，由于iBGP的AD为200，高于EIGRP的90和OSPF的110，所以路由器会选择从EIGRP或者OSPF学到的路由，就导致了这条BGP路由加表失败)
```
```
clear ip bgp详解：
在做了一些路由策略(比如route-map)之后，必须clear一下，策略才能生效
clear ip bgp *			        硬清所有邻居，邻居关系会down掉然后重新开始建立邻居
clear ip bgp x.x.x.x		    硬清某一个邻居
clear ip bgp * soft			    软清所有邻居，邻居关系保持，只是重新交换路由更新		
clear ip bgp x.x.x.x soft		软清某一个邻居
clear ip bgp * soft out		    邻居关系保持，只是重新发送一次路由更新给所有邻居，通常是当改变出方向策略的时候，需要软清out方向来触发策略生效
clear ip bgp x.x.x.x soft out	邻居关系保持，只是重新发送一次路由更新给某个邻居
clear ip bgp * soft in			邻居关系保持，向所有邻居发送route-refresh，请求邻居重新发送一次路由更新，通常是当改变入方向策略的时候，需要软清in方向来触发策略生效
clear ip bgp x.x.x.x soft in	邻居关系保持，向某个邻居发送route-refresh，请求邻居重新发送一次路由更新(如果这个邻居配置了soft-reconfiguration inbound，那实际上不会真的发送route-refresh，而是直接从soft-reconfiguration数据库中取出路由条目来重新过一遍策略)
```
```
路由汇总：
有2种做路由汇总的方法：
1. 先写一条静态汇总路由指向null0(这是为了让本地路由表里有这条路由)，再在BGP进程中通告这条汇总路由，假设本地有三条明细路由：100.1.1.0/24，100.1.2.0/24，100.1.3.0/24
ip route 100.1.0.0 255.255.252.0 null0		                    
router bgp xxx
 address-family ipv4 unicast
  network 100.1.0.0 mask 255.255.252.0

2. 用aggregate-address命令来做汇总，前提条件：BGP表中至少存在一条明细路由，aggregate-address命令才能生效，假设本地有三条明细路由：100.1.1.0/24，100.1.2.0/24，100.1.3.0/24
router bgp xxx
 address-family ipv4 unicast
  aggregate-address 100.1.0.0 255.255.252.0			            通告汇总路由，保留明细路由，邻居会收到汇总路由和明细路由
  aggregate-address 100.1.0.0 255.255.252.0 summary-only		通告汇总路由，抑制明细路由，邻居将只能收到汇总路由
  aggregate-address 100.1.0.0 255.255.252.0 suppress-map sup	通告汇总路由，只有被suppress-map匹配到的路由条目会被抑制，其他明细路由保留
  aggregate-address 100.1.0.0 255.255.252.0 advertise-map adv	只有当被advertise-map匹配到的明细路由在BGP表中存在时，才会生成并通告这条汇总路由
  aggregate-address 100.1.0.0 255.255.252.0 as-set			    让汇总路由带上明细路由的AS_PATH(默认汇总路由不携带明细路由的AS_PATH属性)，如果明细路由的AS_PATH不一样，比如A明细携带100，B明细携带100 200，C明细携带300，则汇总路由会携带{100,200,300}，在计算AS_PATH长短的时候，{}算一个AS，as-set用于eBGP防环
  aggregate-address 100.1.0.0 255.255.252.0 attribute-map attri	为这条汇总路由设置一些属性

access-list 10 permit 100.1.3.0 0.0.0.255							
access-list 20 permit 100.1.1.0 0.0.0.255				

route-map sup permit 10 
 match ip address 10

route-map adv permit 10 
 match ip address 20

route-map attri permit 10 
 set weight 100

注：一般在明细路由的起源本地做汇总用第1种方法，在路由传递途中做汇总用第2种方法
```

BGP属性
![](../images/Screen%20Shot%202022-07-11%20at%2012.18.09.png)

BGP选路  
BGP默认不做负载均衡，必须通过路径属性选出最佳路由  
重要知识点1：如果有多条路径比较，是以BGP表从上至下两两之间比较的方式进行，比如有3条路由，先比1和2，优胜者再和3比  
重要知识点2：BGP表中路由条目的排列顺序是按路由存在时间长短来排列，最新学到的路由总是排在最上面

1. 优选更高的WEIGHT(本路由器选路)
2. 优选更高的LOCAL_PREF(本AS选路)
3. 优选起源于本地的路由(NEXT_HOP = 0.0.0.0)
4. 优选更短的AS_PATH
5. 比较ORIGIN，IGP优先于incomplete
6. 优选更低的MED
7. eBGP路由优先于iBGP路由
8. 优选最近(IGP cost最小)的BGP邻居
9. 如果配置了maximum-paths，可以在本地负载均衡
10. 如果两条都是eBGP路由，优选最老的路由
11. 如果两条都是iBGP路由，优选邻居的Router ID更小的(有RR的应用场景中，优选ORIGINATOR_ID更小的)
12. 优选更短的CLUSTER_LIST
13. 优选RR的邻居IP地址更小的

BGP RIB
![](../images/Screen%20Shot%202022-07-11%20at%2014.19.28.png)

三个做路由策略的工具：  
Prefix Filter  
AS_PATH Filter  
Route-map

```
Prefix Filter
从上到下匹配，直到有一条匹配到即停止向下匹配，末尾有一条隐含条目拒绝所有

ip prefix-list NAME permit 172.16.0.0/22 ge 24 le 24
/22表示前22位必须相同
ge 24, 掩码大于等于24
le 24, 掩码小于等于24
缺省ge, ge=前缀长度
缺省le, le=32
缺省ge和le, ge=le=前缀长度

上面这个例子前22位固定，并且掩码是24位，那就有2位是可变的，可以匹配2的2次方=4条路由，可能的条目有：
172.16.000000 00.0/24
172.16.000000 01.0/24
172.16.000000 10.0/24
172.16.000000 11.0/24
亦即：
172.16.0.0/24
172.16.1.0/24
172.16.2.0/24
172.16.3.0/24

ip prefix-list NAME permit 172.16.0.0/22 ge 26 le 26
固定前22位，掩码是26位，那就有4位是可变的，可以匹配2的4次方=16条路由
172.16.0.0/26
172.16.0.64/26
172.16.0.128/26
172.16.0.192/26
172.16.1.[0,64,128,192]/26
172.16.2.[0,64,128,192]/26
172.16.3.[0,64,128,192]/26

ip prefix-list NAME permit 172.16.0.0/22
缺省ge和le，ge=le=22，精确匹配172.16.0.0/22这一条路由

ip prefix-list NAME permit 172.16.0.0/22 ge 25 le 26
掩码25位的有2的3次方=8条，掩码26位的有2的4次方=16条，加起来可以匹配24条
25位掩码：
172.16.0.0/25
172.16.0.128/25
172.16.1.0/25
172.16.1.128/25
172.16.2.0/25
172.16.2.128/25
172.16.3.0/25
172.16.3.128/25
26位掩码：
172.16.0.[0,64,128,192]/26
172.16.1.[0,64,128,192]/26
172.16.2.[0,64,128,192]/26
172.16.3.[0,64,128,192]/26

特殊路由条目：
ip prefix-list NAME permit 0.0.0.0/0 ge 32         匹配所有主机路由
ip prefix-list NAME permit 0.0.0.0/0 le 32         匹配所有路由
ip prefix-list NAME permit 0.0.0.0/0               匹配默认路由
ip prefix-list NAME permit 10.0.0.0/8 le 32        匹配10/8私有地址
ip prefix-list NAME permit 172.16.0.0/12 le 32     匹配172.16/12私有地址
ip prefix-list NAME permit 192.168.0.0/16 le 32    匹配192.168/16私有地址

prefix-list可以直接在邻居的in或out方向调用，也可以在route-map中调用(见route-map部分)
router bgp xxx
 address-family ipv4 unicast
  neighbor x.x.x.x prefix-list NAME in
  neighbor x.x.x.x prefix-list NAME out

show ip prefix-list
show ip prefix-list NAME
```

AS_PATH Filter  
正则表达式
![](../images/Screen%20Shot%202022-07-14%20at%2022.46.15.png)
```
as-path-access-list从上到下匹配，直到有一条匹配到即停止向下匹配，末尾有一条隐含条目拒绝所有

ip as-path access-list 1 deny .*                    匹配所有，包括空AS和所有非空AS
ip as-path access-list 2 deny ^65501_               匹配AS_PATH中第一个AS为65501的路由，亦即从邻居AS65501传来的路由(路由条目每经过一个AS，AS号加在AS_PATH的最前面)，该路由之前有没有经过其他AS并不关心，可以有也可以没有
ip as-path access-list 3 deny _65501$               匹配AS_PATH中最后一个AS为65501的路由，亦即起源于AS65501的路由，该路由之后有没有经过其他AS并不关心，可以有也可以没有
ip as-path access-list 4 deny ^65501$               匹配AS_PATH中只有65501这一个AS的路由，亦即该路由起源于AS65501，并且AS65501是相邻AS
ip as-path access-list 5 deny _65501_               匹配AS_PATH中包含65501的路由，65501可以在任何位置，该路由可以是起源于AS65501，或者穿越AS65501
ip as-path access-list 6 permit ^$                  匹配AS_PATH为空的路由，亦即起源于本AS的路由(仅当一个AS的边界路由器向eBGP邻居通告路由的时候才会加上本AS的AS号)
ip as-path access-list 7 deny ^65501 64950 251$     匹配AS_PATH中只有65501 64950 251这3个AS的路由
ip as-path access-list 8 permit ^(65501)?$          匹配AS_PATH为空，或者只有65501的路由
ip as-path access-list 9 deny _(65501)|(65515)_     匹配AS_PATH中包含65501或者65515的路由
ip as-path access-list 10 permit ^65501 [0-9]+$     匹配AS_PATH中包含2个AS号，第一个是65501，第二个任意的路由
ip as-path access-list 11 permit ^([0-9]+)( \1)*$   匹配AS_PATH中任意AS号重复出现1次或多次的路由

as-path-access-list可以直接在邻居的in或out方向调用，也可以在route-map中调用(见route-map部分)
router bgp xxx
 address-family ipv4 unicast
  neighbor x.x.x.x filter-list 10 in
  neighbor x.x.x.x filter-list 10 out

show ip as-path-access-list
show ip as-path-access-list 10
show ip bgp filter-list 10
show ip bgp regexp _65520$
```

Route-map  
Match Criteria
![](../images/Screen%20Shot%202022-07-17%20at%2012.25.17.png)
Set Actions
![](../images/Screen%20Shot%202022-07-17%20at%2012.28.21.png)
```
route-map从上到下匹配，直到有一条匹配到即停止向下匹配，末尾有一条隐含条目拒绝所有
不写match就是match所有，不写set就是什么都不set

route-map NAME permit 10
 match as-path 10
 set weight 500
 set origin igp
route-map NAME permit 20
 match ip address prefix-list NAME
 set as-path prepend last-as 2
route-map NAME deny 30
 match ip address prefix-list NAME
route-map NAME permit 100

router bgp xxx
 address-family ipv4
  neighbor x.x.x.x route-map NAME in
  neighbor x.x.x.x route-map NAME out
  network x.x.x.x route-map NAME        route-map可以直接挂在network命令上来做策略

show route-map
show route-map NAME
```

Weight  
思科私有属性，优选weight值大的路由(取值范围0-65535)，weight只在本地有效，只影响本路由器的选路，weight属性不会传给邻居，所以从邻居学到的路由weight=0，从本路由器通告/重分布/汇总的路由的weight=32768，weight只能配置在eBGP邻居和iBGP邻居的in方向，不能配置在out方向，用以指导本路由器的选路
```
配置举例：
router bgp xxx
 address-family ipv4 unicast
  neighbor x.x.x.x weight 1000			从某邻居处收到的所有路由weight都设成1000
  neighbor x.x.x.x route-map WEI in		只能是in方向

ip prefix-list TEST seq 5 permit 100.1.0.0/22

route-map WEI permit 10
 match ip address prefix-list TEST
 set weight 1000
route-map WEI permit 100
```

LOCAL_PREF  
优选LOCAL_PREF值大的路由(取值范围0-2^32-1)，LOCAL_PREF属性只在iBGP邻居之间传递，不会传给eBGP邻居，所以LOCAL_PREF只能作用于AS内，使用场景：本AS有多个边界路由器都收到了同一个路由条目，可以通过LOCAL_PREF来选择从哪个边界路由器出去去往该目的地，LOCAL_PREF默认值为100(show ip bgp看到LocPrf显示为空的，其实也是100，show ip bgp x.x.x.x可以看到)，可以通过命令bgp default local-preference修改默认值(只对eBGP学到的和本地产生的路由有效，对iBGP学到的路由无效)，LOCAL_PREF可以配置在eBGP邻居和iBGP邻居的in方向，也可以配置在iBGP邻居的out方向，不能配置在eBGP邻居的out方向
```
配置举例：
local-preference通常是配置在eBGP邻居的in方向
router bgp xxx
 address-family ipv4 unicast
  neighbor x.x.x.x route-map LOCPRF in

ip prefix-list TEST seq 5 permit 100.1.0.0/22

route-map LOCPRF permit 10
 match ip address prefix-list TEST
 set local-preference 200
route-map LOCPRF permit 100
```

MED(Multi Exit Discriminator)  
优选MED更小的路由(取值范围0-2^32-1)，使用场景：本AS和某个邻居AS之间有多条连接，可以通告MED给邻居AS来影响邻居AS到本AS的选路，MED默认值为0，MED属性在eBGP邻居和iBGP邻居之间都会传递，但只能在两个相邻AS之间传递，也就是说，从eBGP邻居收到的路由的MED属性，会传给iBGP邻居，但不会传出本AS  
重点：假设本AS从多个边界路由器学到同一个路由条目，默认情况下，只有当这条路由是从同一个相邻AS学到时(AS_PATH的第一个AS相同)，才比较MED，也就是说，如果本AS从两个不同的相邻AS学到同一条路由，是不比较MED的，可以通过命令bgp always-compare-med来改变这个默认行为  
注：MED基本上被弃用，从本地AS去影响其他AS选路倾向于用AS_PATH Prepending
```
配置举例：
边界路由器1
router bgp xxx
 address-family ipv4 unicast
    neighbor x.x.x.x route-map MED out

ip prefix-list TEST seq 5 permit 100.1.0.0/22

route-map MED permit 10 
 match ip address prefix-list TEST
 set metric 10
route-map MED permit 100 

边界路由器2
router bgp xxx
 address-family ipv4 unicast
    neighbor x.x.x.x route-map MED out

ip prefix-list TEST seq 5 permit 100.1.0.0/22

route-map MED permit 10 
 match ip address prefix-list TEST
 set metric 20
route-map MED permit 100

实验证明：
MED除了配置在eBGP邻居的out方向，其配置在eBGP邻居的in方向和iBGP邻居的in/out方向都能生效
```

AS_PATH Prepending  
优选AS_PATH更短的路由，应用场景：本AS和邻居AS(同一个邻居AS或不同邻居AS)之间有多条连接的情况下，通过对出方向eBGP路由更新prepend一个或多个AS号来改变AS_PATH的长度，从而影响外部AS到本AS的选路，AS_PATH属性在eBGP邻居和iBGP邻居之间都会传递，并且可以传遍整个网络  
注：可以通过命令bgp bestpath as-path ignore来跳过AS_PATH选路原则
```
配置举例：
router bgp xxx
 address-family ipv4 unicast
  neighbor x.x.x.x route-map AS_PREPEND out

ip prefix-list TEST seq 5 permit 100.1.0.0/22

route-map AS_PREPEND permit 10
 match ip address prefix-list TEST
 set as-path prepend xxx xxx		
 set as-path prepend last-as x			重复增加最后一个AS号N次，这个配置如果在out方向的route-map配，那得这条路由在离开本AS之前就已经携带了AS号才有用，因为仅当路由在离开本AS的时候(在route-map处理之后)才会携带本AS的AS号，所以如果一条路由是本AS生成的，其在离开本AS之前是不携带AS号的，也就没有所谓的last-as
route-map AS_PREPEND permit 100

Best Rractice: 
1. 只prepend本AS的AS号
2. 不要prepend太多AS号(大多数情况下prepend2-3个AS号就能达到目的，prepend太多显得很不专业)

实验证明：
AS_PATH Prepending除了可以配置在eBGP邻居的out方向，也可以配置在eBGP邻居的in方向，不能配置在iBGP邻居之间(命令可以敲，但是敲了没用)
out方向增加的AS号加在本AS号的右边，in方向增加的AS号加在AS_PATH的最左边(AS_PATH选路只看AS_PATH长短，不看AS顺序，所以加在哪里没有实际意义，知道下即可)
```

BGP Communities  
BGP Community是一个32位的值，格式为：16位AS号:16位自定义，community的作用就是给一个路由条目打上一个tag，通过community-list匹配community来做策略，应用场景：本AS是一个Transit AS，连了很多Stub AS和其他Transit AS，可以在每个邻居的in方向给所有收到的路由条目打上community(本AS号:自定义)，然后基于community来做策略，community可以配置在eBGP邻居和iBGP邻居的in/out方向
```
配置举例：
路由器1，在eBGP邻居的out方向匹配路由条目打上community
router bgp xxx
 address-family ipv4 unicast
  neighbor x.x.x.x route-map COMM out	
  neighbor x.x.x.x send-community 		    community默认不随路由条目一起传递，需要敲这条命令来发送community给邻居，默认发送标准community
  neighbor x.x.x.x send-community extended  发送扩展community
    		
ip bgp-community new-format			        用aa:nn的格式显示community

ip prefix-list TEST1 seq 5 permit 100.1.0.0/22
ip prefix-list TEST2 seq 5 permit 100.1.4.0/22

route-map COMM permit 10
 match ip address prefix-list TEST1
 set community 65501:100
route-map COMM permit 20
 match ip address prefix-list TEST2
 set community 65501:100 65501:200
route-map COMM permit 100

路由器2，用community-list匹配community来做策略
router bgp xxx
 address-family ipv4 unicast
  neighbor x.x.x.x route-map COMM in

ip bgp-community new-format

ip community-list standard TEST1 permit 65501:100
ip community-list standard TEST2 permit 65501:100 65501:200
ip community-list standard TEST3 permit 65501:100
ip community-list standard TEST3 permit 65501:100 65501:200

route-map COMM permit 10
 match community TEST1              如果这样match，那么只要community里有65501:100就能匹配上，本例中100.1.0.0/22和100.1.4.0/22都能匹配上
 match community TEST1 exact-match	exact-match表示精确匹配(community里只能有65501:100)，本例中只能匹配中100.1.0.0/22
 match community TEST2			    TEST2匹配65501:100 65501:200，本例中只能匹配中100.1.4.0/22
 match community TEST3			    TEST3有两条语句分别匹配65501:100和65501:100 65501:200，本例中100.1.0.0/22和100.1.4.0/22都能匹配上	
 set community 65501:300            默认是用新的community覆盖原来携带的community
 set community 65501:300 additive   追加一个community
 set comm-list TEST1 delete         删除被community-list匹配到的特定community
 set community none                 删除所有community
route-map COMM permit 100

四个标准community
set community no-advertise		不传给任何BGP邻居
set community local-AS			不传给eBGP邻居(有联邦的环境下，不传出联邦)	
set community no-export		    不传给真正的eBGP邻居(联邦和联邦之间可以传递)
set community internet			任意传，所有的路由条目默认携带internet这个community(用ip community-list standard NAME permit internet可以匹配到所有路由)

show ip bgp community           列出所有携带community的路由条目
show ip bgp community aa:nn
show ip bgp community local-AS
show ip bgp community no-advertise
show ip bgp community no-export
```

Session Templates
![](../images/Screen%20Shot%202022-08-07%20at%2009.10.28.png)
session template的继承是线性的，即一个子template只能直接继承自一个父template，BGP邻居可以调用任何一个session template
![](../images/Screen%20Shot%202022-08-07%20at%2012.51.15.png)
session template配置举例
![](../images/Screen%20Shot%202022-08-08%20at%2012.08.31.png)

Policy Templates
![](../images/Screen%20Shot%202022-08-08%20at%2012.13.28.png)
policy template的继承是非线性的，即一个子template可以直接继承自多个父template，BGP邻居可以调用任何一个policy template
![](../images/Screen%20Shot%202022-08-10%20at%2008.13.59.png)
policy template配置举例
![](../images/Screen%20Shot%202022-08-10%20at%2008.20.31.png)

移除私有AS号  
neighbor x.x.x.x remove-private-as，这条命令的作用是在通告路由条目给eBGP邻居之前移除路由条目中携带的私有AS号，使用场景：某大型企业有一个backbone网络是公有AS号，连接了internet，backbone也连接了企业的各个分支机构的网络，分支机构都是私有AS号，这些分支机构都通过eBGP连接到backbone并把各自的路由条目通告给backbone，在backbone连接internet的边界路由器上，可以用这条命令在通告路由条目给internet之前移除路由条目携带的私有AS号

Route Reflector  
一个RR cluster由一个RR和他的client组成，Cluster ID默认是RR的Router ID，在RR cluster内部，所有的RR client仅和RR建立iBGP邻居，在RR cluster以外，RR和其他非client建立full mesh iBGP邻居
![](../images/Screen%20Shot%202022-08-11%20at%2015.49.05.png)

部署了RR的网络中的路由传递
![](../images/Screen%20Shot%202022-08-11%20at%2016.04.24.png)
- 普通BGP路由器从iBGP邻居收到的路由不会传给其他iBGP邻居，可以传给eBGP邻居
- 普通BGP路由器从eBGP邻居收到的路由会传递给所有BGP邻居(包括iBGP邻居和eBGP邻居)
- RR从client收到的路由反射给所有BGP邻居(包括client，非client，和eBGP邻居)
- RR从非client收到的路由反射给所有的client和eBGP邻居，不会反射给其他非client
- RR从eBGP邻居收到的路由反射给所有BGP邻居(包括client，非client，和eBGP邻居)

冗余RR部署  
![](../images/Screen%20Shot%202022-08-11%20at%2016.37.51.png)

大型iBGP网络中的多层次RR部署
![](../images/Screen%20Shot%202022-08-11%20at%2016.32.59.png)

多RR网络中的iBGP防环机制  
当RR反射一条从iBGP邻居学到的路由的时候，会为这条路由生成两个BGP属性，ORIGINATOR_ID和CLUSTER_LIST，ORIGINATOR_ID是这条路由的起源路由器的Router ID，CLUSTER_LIST列出了这条路由在到达目的地前经过的所有RR的Cluster ID，也就是说这条路由每一次被RR反射，那台RR的Cluster ID就会加入到CLUSTER_LIST中，这里描述的是RR在反射从iBGP邻居学到的路由时的行为，RR在反射(确切讲应该是传递，因为反射只是针对iBGP路由的术语)从eBGP邻居学到的路由时没有以上行为  
- 当一个普通BGP路由器从iBGP邻居收到一条路由，发现路由属性中的ORIGINATOR_ID是他自己的Router ID，则拒收这条路由  
- 当一个RR从iBGP邻居收到一条路由，发现路由属性中的CLUSTER_LIST中有自己的Cluster ID，则拒收这条路由

RR配置举例
![](../images/Screen%20Shot%202022-08-11%20at%2017.51.10.png)

其他的选路原则： 
- 优选起源于本地的路由(选路规则3)  
在本路由器通告/重分布/汇总一条路由，同时这条路由也从BGP邻居学到，优选起源于本地的路由(这条规则对Cisco没有意义，Cisco路由器从本路由器通告/重分布/汇总的路由的weight=32768，所以直接就通过weight优选了)  
注：在BGP进程中用network通告一条路由的时候(这条路由一定是在路由表中存在的，或者是本地直连，或者是静态，或者是通过IGP学到)，所生成的BGP路由条目会携带该路由在路由表中的下一跳和metric  

- Origin Codes(选路规则5)  
起源代码i(IGP)代表是通过network/aggregate-address产生的路由，起源代码?(incomplete)代表是重分布产生的路由，优选i，起源代码属性在所有BGP邻居之间都会传递，可以配置在所有BGP邻居的in和out方向
```
配置举例：
router bgp xxx
 address-family ipv4 unicast
  neighbor x.x.x.x route-map ORIGIN in

ip prefix-list TEST seq 5 permit 100.1.0.0/22

route-map ORIGIN permit 10
 match ip address prefix-list TEST
 set origin incomplete
route-map ORIGIN permit 100
```

- 优选eBGP路由(选路规则7)  
如果一条路由同时从iBGP邻居和eBGP邻居学到，优选eBGP路由

- 优选最近的BGP邻居(选路规则8)  
这条规则对eBGP邻居和iBGP邻居都有效，eBGP邻居和eBGP邻居比，iBGP邻居和iBGP邻居比，eBGP邻居一般是直连，metric为0，iBGP邻居之间比的其实就是底层IGP路由的metric

- 负载均衡(选路规则9)  
当前面8条规则都选不出最优路由的时候，可以配置maximum-paths命令实现负载均衡，默认是对eBGP路由负载均衡，还可以使用命令maximum-paths ibgp对iBGP路由负载均衡，但是负载均衡只在配置了maximum-paths的路由器本地生效，这台路由器依然会根据第8条后面的选路原则选出最优路由传给其他邻居

- 优选存在时间最长的eBGP路由(选路规则10)  
这条规则只对eBGP路由有效，且比的是学习到路由的时间长短，不是指邻居up的时间长短，如果不想用这条规则来选路，可以配置命令bgp bestpath compare-routerid来跳过这条规则，直接比较邻居的Router ID

- 优选小的BGP Router ID(选路规则11)  
iBGP选路不看第10条规则，如果第8条规则选不出来，就直接到第11条规则比Router ID，优选邻居Router ID更小的，eBGP选路可以配置bgp bestpath compare-routerid来跳过第10条规则，也用第11条规则选路    
注：在有RR的环境下的说明：
   - 单RR环境：  
   如果一条路由从多个边界路由器学到并被RR反射，则比较路由的ORIGINATOR_ID，优选小的ORIGINATOR_ID，如果一条路由只从一个边界路由器学到，那就不存在选路问题了
   - 多RR环境：  
   如果一条路由从多个边界路由器学到并被多个RR反射，则比较路由的ORIGINATOR_ID，优选小的ORIGINATOR_ID，然后继续用第12，13条规则选路，如果一条路由只从一个边界路由器学到并被多个RR反射，则跳过第11条规则，直接用第12，13条规则选路

- 优选更短的CLUSTER_LIST(选路规则12)  
在多RR环境下，如果从多个RR收到同一条路由(ORIGINATOR_ID也一样)，则比较CLUSTER_LIST的长短，优选CLUSTER_LIST长度短的

- 优选RR的邻居IP地址更小的(选路规则13)  
如果CLUSTER_LIST长短也一样，优选RR邻居IP地址更小的

misc.  
1. 实验中的发现：route-map如果match的prefix-list不存在，就会match所有的路由
2. 在vpnv4 address-family里面，iBGP邻居的next-hope-self是自动生成的
3. How to identify the BGP server and client while initiating TCP session  
Ok, let me put it in another phrase, any TCP session relies on a Client Server like ideology, were one end initiates the TCP session to the other end, in the case of BGP each router though of itself as a client and try to initiate a TCP session to the other router to port 179 as destination and random high port number as source. The whole idea here is, it could happen that both routers has initiated TCP sessions to each other, and since two routers should have only one BGP session between them, and since the "router-ID" value is exchanged when establishing BGP, if two parallel sessions are detected only the session initiated by the router having the higher router ID will be retained, and the other will be dropped.

以下知识用不到，没记笔记  
peer group  
confederations  
route dampening  

做一个大型实验：包含MPLS VPN，RR cluster这两个技术，RR cluster来反射客户路由，部署RR的主要思想是把路由控制层面和数据转发层面分离，减少BGP peering
