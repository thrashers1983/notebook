vswitch的工作原理：
1. vswitch和物理交换机一个最重要的不同点：vswitch不学习MAC地址，vswitch天生知道所有VM的MAC地址，uplink接口也不学习MAC地址，所以物理交换机上接的设备的MAC地址对于vswitch来说都是未知MAC

2. vswitch不运行STP，不发BPDU，也不收BPDU  
注：接ESXi的物理交换机接口建议配置bpduguard和spanning-tree portfast/portfast trunk

3. 当vswitch有多条uplink接到物理交换机，怎么防止环路：  
   - 从一条uplink收到的包不会从其他uplink发出去
   - 从一条uplink发出去的广播/组播/未知单播，会被物理交换机泛洪，从而从其他uplink又收回来，这时候vswitch会检查数据包的源MAC，如果源MAC是某一个VM的MAC地址，则丢弃该数据包

4. vswitch对广播/组播的处理：
   - 从一个VM发出的广播/组播，会发送到属于同VLAN的port group内的所有VM，也会发送到某一条uplink(不会向所有的uplink泛洪，保证物理交换机只收到一份广播/组播的拷贝)
   - 从一条uplink收到的广播/组播，会发送到属于同VLAN的port group内的所有VM，不会从其他uplink发出去(如果从多条uplink同时收到相同的广播/组播，GPT4说这种情况下vswitch有工作机制可以确保VM只会收到一份广播/组播，我做过实验也证明了这点)

5. vswitch对未知单播的处理：
   - 从一个VM发出的未知单播，只会发送到某一条uplink(不会向所有的uplink泛洪)，也不会在vlan内泛洪(除非开启杂合模式)
   - 从uplink收到的未知单播，直接丢弃(除非开启杂合模式)

6. port group的vlan配置：
   - Virtual Switch Tagging(VST): vlan ID 1-4094
     - 这个模式就相当于传统交换机的access接口配了vlan 
     - 配了相同vlan ID的port group内的VM可以互相通信
     - 从uplink发出去的数据帧会打上vlan tag
     - 从trunk port group发出去的数据帧会打上vlan tag
   - External Switch Tagging(EST): vlan ID 0
     - 这个模式就相当于传统交换机的access接口没有配vlan
     - 配了vlan ID为0的port group内的VM可以互相通信
     - 从uplink发出去的数据帧不打vlan tag
     - 从trunk port group发出去的数据帧不打vlan tag
   - Virtual Guest Tagging(VGT): vlan ID 4095
     - 这个模式就相当于传统交换机配了trunk
     - VGT的port group内的VM可以和同vlan的VST/EST/VGT的port group内的VM互相通信
     - 从uplink发出去的数据帧会打上vlan tag
     - 从其他trunk port group发出去的数据帧会打上vlan tag
  
     要想两个端口组二层隔离，需满足以下条件：
     - 两个VST的port group配了不同的vlan ID
     - 一个是VST的port group，一个是EST的port group

7. 关于vswitch的uplink的对端物理交换机接口：
   - 如果对端物理交换机接口是access口：
     - 收到不打tag的帧(对应EST的port group发出的帧)，则直接进入接口所属vlan，回包也能抵达EST的port group，收发都正常
     - 收到打tag的帧(对应VST和VGT的port group发出的帧)的vlan ID和接口vlan一样，可以正常接收，但是回包由于不打tag会送到EST的port group，因此无法正常工作
     - 收到打tag的帧的vlan ID和接口vlan不一样直接丢弃
  
     总结：物理交换机access接口只能配合EST的port group使用，也就是vlan直通

   - 如果对端物理交换机接口是trunk：   
     - 收到一个不打tag的帧(对应EST的port group发出的帧)，则进入native vlan，回包也不打tag，也能抵达EST的port group，收发都正常
     - 收到一个打tag的帧(对应VST和VGT的port group发出的帧)的vlan ID和native vlan不一样，则进入相应的vlan，回包也能抵达对应的VST和VGT的port group，收发都正常
     - 收到一个打tag的帧(对应VST和VGT的port group发出的帧)的vlan ID和native vlan一样，直接丢弃
  
     总结：不能给port group分配和物理交换机trunk的native vlan一样的vlan ID
    
    注：以上关于第7条的总结也适用于trunk port group接虚拟交换机的场景

### Security
杂合模式  
开启了杂合模式的port group中的VM，会收到该port group所在vlan的所有流量，相当于开启了杂合模式的port group变成了一个集线器，该vlan的所有流量会在这个port group里广播

MAC address changes and forged transmits

Every virtual machine has two MAC addresses by definition. The MAC address that is assigned to the vNIC of a virtual machine when the vNIC gets created is called the initial MAC address. The MAC address that a guest operating system configures for the network interface it detects is called the effective MAC address. The effective MAC address should generally match the initial MAC address (which is actual MAC on NIC):

MAC address changes apply to the traffic entering a virtual machine from the virtual switch. If MAC address changes are set to Accept, then it means that you allow the virtual machine to receive traffic originally intended for another VM, by impersonating the other VM's MAC address. For example, if VM-A wanted to receive traffic intended for VM-B, then VM-A will need to present itself with a MAC address belonging to VM-B. This is usually achieved by changing the effective MAC address (OS level). Such a VM's initial MAC address will remain unchanged. With MAC address changes set to Accept, the virtual switch will allow the effective MAC address to be different from the initial MAC address. With MAC address changes set to Reject, the port/dvPort to which the vNIC is connected will be blocked, consequently the VM will stop receiving any traffic.

The Forged transmits setting applies to the traffic leaving a virtual machine and entering a virtual switch. If set to Accept, it allows source MAC address spoofing, meaning, a virtual machine will be allowed to send out frames with a source MAC address that is different from the initial/effective MAC address. With the option set to Reject, the virtual switch will drop the frame with a MAC address that does not match the initial/effective MAC address.

Both MAC address changes and Forged transmits are set to Reject by default.

杂合模式和伪传输应用场景：  
比如VM是eve-ng，eve-ng还配了桥接，那eve-ng所在的port group要打开杂合模式和伪传输  
对于vswitch来说，eve-ng里面的设备的MAC地址都是未知MAC(因为vswitch不学习MAC地址，他只知道eve-ng本身的网卡MAC)，因此去往eve-ng里面的设备的流量，对于vswitch来说都是未知单播，默认未知单播在vlan内部被直接丢弃，port group开启了杂合模式后，该vlan的所有流量会在这个port group里广播，eve-ng里面的设备就能收到返回的流量，而从eve-ng里面的设备发出来的流量，其源MAC和eve-ng网卡的MAC地址(initial MAC)不一样，默认不允许，所以必须启用伪传输

### NIC teaming
#### Load balancing
- Route based on originating port ID  
  默认模式，也是推荐配置，基于vNIC来负载，一个vNIC绑定一个物理网卡，假设vswitch有2个物理网卡，那么，vNIC1-pNIC1，vNIC2-pNIC2，vNIC3-pNIC1，以此类推，物理交换机接口就配单独的access或者trunk
- Route based on source MAC hash  
  基于源MAC负载，如果从某个vNIC发出的流量有很多不同的源MAC，那么这个负载效果就比基于vNIC的要更加均衡，物理交换机接口就配单独的access或者trunk
- Route based on IP hash  
  基于源目IP哈希负载，物理交换机接口要配port-channel(为什么要port channel？因为IP哈希会导致一个源MAC地址的流量从不同的uplink出去，会造成物理交换机MAC地址表翻动，所以必须port-channel，前面两种负载方式一个源MAC地址总是和某一条uplink绑定所以不需要port-channel，另外：vss不支持LACP，物理交换机那头要配channel-group mode on)
- Use explicit failover order  
  这个策略不是负载均衡，先使用Failover order列表里的Active uplink里的第一个，如果Active uplink都失效了，再使用Standby uplink
#### Network failover detection
- Link status only  
  默认模式，可以探测到网线断了或者物理交换机挂了，无法探测到物理交换机接口VLAN配错了或者接口被STP block了
- Beacon only  
  选这个模式推荐有3条以上的uplink接到不同的物理交换机才能正常工作
#### Notify switches
当有VM开机，或者发生了uplink failover，vswitch会主动发RARP给物理交换机通知其更新MAC address-table
#### Failback
当Active uplink挂了，Stanby uplink会变成Active，之后那条Active uplink又恢复了，他会抢占Active角色，Standby uplink还是切到standby
