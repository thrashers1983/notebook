vswitch的工作原理：
1. vswitch和物理交换机一个最重要的不同点：vswitch不学习MAC地址，vswitch天生知道所有VM的MAC地址，uplink接口也不学习MAC地址，所以物理交换机上接的设备的MAC地址对于vswitch来说都是未知MAC

2. vswitch不运行STP，不发BPDU，也不收BPDU  
注：接ESXi的物理交换机接口建议配置bpduguard和spanning-tree portfast/portfast trunk

3. 当vswitch有多条uplink接到物理交换机，怎么防止环路：  
   - 从一条uplink收到的包不会从其他uplink发出去
   - 从一条uplink发出去的广播/组播/未知单播，会被物理交换机泛洪，从而从其他uplink又收回来，这时候vswitch会检查数据包的源MAC，如果源MAC是某一个VM的MAC地址，则丢弃该数据包

4. vswitch对广播/组播的处理：
   - 从一个VM发出的广播/组播，会发送到属于同VLAN的port group内的所有VM，也会发送到某一条uplink(不会向所有的uplink泛洪，保证物理交换机只收到一份广播/组播的拷贝)
   - 从一条uplink收到的广播/组播，会发送到属于同VLAN的port group内的所有VM，不会从其他uplink发出去(这里没有讨论从多条uplink同时收到广播/组播的情况，首先可以肯定的是，这些广播/组播不会又从uplink传回去，但是VM会不会收到重复的广播/组播？)

5. vswitch对未知单播的处理：
   - 从一个VM发出的未知单播，只会发送到某一条uplink(不会向所有的uplink泛洪)，也不会在vlan内泛洪
   - 从uplink收到的未知单播，直接丢弃

6. vswitch的uplink会给每个发出去的数据帧打上vlan tag
   - 如果对端物理交换机接口是access口，access口收到打tag的帧，只要vlan ID和接口vlan一样，就可以正常收，如果收到打tag的帧的vlan ID和接口vlan不一样就丢弃
   - 如果对端物理交换机接口是trunk，也能正常工作，但是有一个注意点：不能给port group分配和物理交换机trunk的native vlan一样的vlan ID，因为：   
     - 物理交换机的trunk接口如果收到一个打tag的帧，vlan ID和native vlan一样，则丢弃
     - 物理交换机trunk上发出的native vlan的帧是不打tag的，vswitch收到不打tag的帧，就会送到vlan ID为0的port group

7. port group的vlan配置：  
   - vlan ID范围: 1-4094    
   - vlan ID 0: 配置该端口组不打tag  
   - vlan ID 4095: 配置该端口组为trunk  

    两个端口组如果配置了一样的vlan ID(或者都配0，或者都配4095，或者一个配0一个配4095)，这两个端口组内的VM可以相互通信，要想两个端口组二层隔离，必须两个端口组配不同的vlan ID

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
  基于源目IP负载，物理交换机接口要配port-channel
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
