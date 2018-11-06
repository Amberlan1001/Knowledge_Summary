# Merkle Tree 详解

## Merkle Tree 概念
   
   Merkle Tree，通常也被称作Hash Tree，顾名思义，就是存储hash值的一棵树。Merkle树的叶子是数据块(例如，文件或者文件的集合)的hash值。非叶节点是其对应子节点串联字符串的hash。

   在点对点网络中作数据传输的时候，会同时从多个机器上下载数据，而且很多机器可以认为是不稳定或者不可信的。为了校验数据的完整性，更好的办法是把大的文件分割成小的数据块（例如，把分割成2K为单位的数据块）。这样的好处是，如果小块数据在传输过程中损坏了，那么只要重新下载这一快数据就行了，不用重新下载整个文件。

2. Hash List  

   怎么确定小的数据块没有损坏哪？只需要为每个数据块做Hash。BT下载的时候，在下载到真正数据之前，我们会先下载一个Hash列表。那么问题又来了，怎么确定这个Hash列表本事是正确的哪？答案是把每个小块数据的Hash值拼到一起，然后对这个长字符串在作一次Hash运算，这样就得到Hash列表的根Hash(Top Hash or Root Hash)。下载数据的时候，首先从可信的数据源得到正确的根Hash，就可以用它来校验Hash列表了，然后通过校验后的Hash列表校验数据块。

3. Merkle Tree
    
   Merkle Tree可以看做Hash List的泛化（Hash List可以看作一种特殊的Merkle Tree，即树高为2的多叉Merkle Tree）。
在最底层，和哈希列表一样，我们把数据分成小的数据块，有相应地哈希和它对应。但是往上走，并不是直接去运算根哈希，而是把相邻的两个哈希合并成一个字符串，然后运算这个字符串的哈希，这样每两个哈希就结婚生子，得到了一个”子哈希“。如果最底层的哈希总数是单数，那到最后必然出现一个单身哈希，这种情况就直接对它进行哈希运算，所以也能得到它的子哈希。于是往上推，依然是一样的方式，可以得到数目更少的新一级哈希，最终必然形成一棵倒挂的树，到了树根的这个位置，这一代就剩下一个根哈希了，我们把它叫做 Merkle Root[3]。

   在p2p网络下载网络之前，先从可信的源获得文件的Merkle Tree树根。一旦获得了树根，就可以从其他从不可信的源获取Merkle tree。通过可信的树根来检查接受到的Merkle Tree。如果Merkle Tree是损坏的或者虚假的，就从其他源获得另一个Merkle Tree，直到获得一个与可信树根匹配的Merkle Tree。
  
   Merkle Tree和Hash List的主要区别是，可以直接下载并立即验证Merkle Tree的一个分支。因为可以将文件切分成小的数据块，这样如果有一块数据损坏，仅仅重新下载这个数据块就行了。如果文件非常大，那么Merkle tree和Hash list都很到，但是Merkle tree可以一次下载一个分支，然后立即验证这个分支，如果分支验证通过，就可以下载数据了。而Hash list只有下载整个hash list才能验证。

<p align="center">
<img src="https://github.com/Amberlan1001/Knowledge_Summary/blob/master/pic/MerkleTree.png" width="500" height="400" align="center"/>
</p> 

## Merkle Tree的特点

1. MT是一种树，大多数是二叉树，也可以多叉树，无论是几叉树，它都具有树结构的所有特点；
2. Merkle Tree的叶子节点的value是数据集合的单元数据或者单元数据HASH。
3. 非叶子节点的value是根据它下面所有的叶子节点值，然后按照Hash算法计算而得出的。

  通常，加密的hash方法像SHA-2和MD5用来做hash。但如果仅仅防止数据不是蓄意的损坏或篡改，可以改用一些安全性低但效率高的校验和算法，如CRC。

   Second Preimage Attack: Merkle tree的树根并不表示树的深度，这可能会导致second-preimage attack，即攻击者创建一个具有相同Merkle树根的虚假文档。一个简单的解决方法在Certificate Transparency中定义：当计算叶节点的hash时，在hash数据前加0x00。当计算内部节点是，在前面加0x01。另外一些实现限制hash tree的根，通过在hash值前面加深度前缀。因此，前缀每一步会减少，只有当到达叶子时前缀依然为正，提取的hash链才被定义为有效。

## Merkle Tree的操作

1. 创建Merckle Tree

    加入最底层有9个数据块。

    step1:（红色线）对数据块做hash运算，Node0i = hash(Data0i), i=1,2,…,9   
    step2:（橙色线）相邻两个hash块串联，然后做hash运算，Node1((i+1)/2) = hash(Node0i+Node0(i+1)), i=1,3,5,7;对于i=9, Node1((i+1)/2) =        hash(Node0i)   
    step3:（黄色线）重复step2   
    step4:（绿色线）重复step2   
    step5:（蓝色线）重复step2，生成Merkle Tree Root  

<p align="center">
<img src="https://github.com/Amberlan1001/Knowledge_Summary/blob/master/pic/MerkleTreeOpt.png" width="550" height="400" align="center"/>
</p> 

易得，创建Merkle Tree是O(n)复杂度(这里指O(n)次hash运算)，n是数据块的大小。得到Merkle Tree的树高是log(n)+1。

2. 检索数据块

   为了更好理解，我们假设有A和B两台机器，A需要与B相同目录下有8个文件，文件分别是f1 f2 f3 ....f8。这个时候我们就可以通过Merkle Tree来进行快速比较。假设我们在文件创建的时候每个机器都构建了一个Merkle Tree。具体如下图:
   
<p align="center">
<img src="https://github.com/Amberlan1001/Knowledge_Summary/blob/master/pic/merkletree_f.png" width="500" height="200" align="center"/>
</p> 

  从上图可得知，叶子节点node7的value = hash(f1),是f1文件的HASH;而其父亲节点node3的value = hash(v7, v8)，也就是其子节点node7 node8的值得HASH。就是这样表示一个层级运算关系。root节点的value其实是所有叶子节点的value的唯一特征。

  假如A上的文件5与B上的不一样。我们怎么通过两个机器的merkle treee信息找到不相同的文件? 这个比较检索过程如下:
    
    Step1. 首先比较v0是否相同,如果不同，检索其孩子node1和node2.
    Step2. v1 相同，v2不同。检索node2的孩子node5 node6;
    Step3. v5不同，v6相同，检索比较node5的孩子node 11 和node 12
    Step4. v11不同，v12相同。node 11为叶子节点，获取其目录信息。
    Step5. 检索比较完毕。

## BitCoin和Ethereum
Bitcoin的Blockchain利用Merkle proofs来存储每个区块的交易。   
而这样做的好处，也就是中本聪描述到的“简化支付验证”（Simplified Payment Verification，SPV）的概念:一个“轻客户端”（light client）可以仅下载链的区块头即每个区块中的80byte的数据块，仅包含五个元素，而不是下载每一笔交易以及每一个区块：

<p align="center">
<img src="https://github.com/Amberlan1001/Knowledge_Summary/blob/master/pic/BitCoinMerkle.png" width="600" height="350" align="center"/>
</p> 

* 上一区块头的哈希值
* 时间戳
* 挖矿难度值
* 工作量证明随机数（nonce）
* 包含该区块交易的Merkle Tree的根哈希

　　如果客户端想要确认一个交易的状态，它只需简单的发起一个Merkle proof请求，这个请求显示出这个特定的交易在Merkle trees的一个之中，而且这个Merkle Tree的树根在主链的一个区块头中。

　　但是Bitcoin的轻客户端有它的局限。一个局限是，尽管它可以证明包含的交易，但是它不能进行涉及当前状态的证明（如数字资产的持有，名称注册，金融合约的状态等）。

　　Bitcoin如何查询你当前有多少币？一个比特币轻客户端，可以使用一种协议，它涉及查询多个节点，并相信其中至少会有一个节点会通知你，关于你的地址中任何特定的交易支出，而这可以让你实现更多的应用。但对于其他更为复杂的应用而言，这些远远是不够的。一笔交易影响的确切性质（precise nature），可以取决于此前的几笔交易，而这些交易本身则依赖于更为前面的交易，所以最终你可以验证整个链上的每一笔交易。为了解决这个问题，Ethereum的Merkle Tree的概念，会更进一步。
  
### Ethereum的Merkle Proof

　　每个以太坊区块头不是包括一个Merkle树，而是为三种对象设计的三棵树：

* 交易Transaction
* 收据Receipts(本质上是显示每个交易影响的多块数据)
* 状态State

<p align="center">
<img src="https://github.com/Amberlan1001/Knowledge_Summary/blob/master/pic/EthereumMerkel.png" width="500" height="300" align="center"/>
</p> 

这使得一个非常先进的轻客户端协议成为了可能，它允许轻客户端轻松地进行并核实以下类型的查询答案：

    * 这笔交易被包含在特定的区块中了么？
    * 告诉我这个地址在过去30天中，发出X类型事件的所有实例（例如，一个众筹合约完成了它的目标）
    * 目前我的账户余额是多少？
    * 这个账户是否存在？
    * 假如在这个合约中运行这笔交易，它的输出会是什么？

　　第一种是由交易树（transaction tree）来处理的；第三和第四种则是由状态树（state tree）负责处理，第二种则由收据树（receipt tree）处理。计算前四个查询任务是相当简单的。服务器简单地找到对象，获取Merkle分支，并通过分支来回复轻客户端。

　　第五种查询任务同样也是由状态树处理，但它的计算方式会比较复杂。这里，我们需要构建一个Merkle状态转变证明（Merkle state transition proof）。从本质上来讲，这样的证明也就是在说“如果你在根S的状态树上运行交易T，其结果状态树将是根为S'，log为L，输出为O” （“输出”作为存在于以太坊的一种概念，因为每一笔交易都是一个函数调用；它在理论上并不是必要的）。

　　为了推断这个证明，服务器在本地创建了一个假的区块，将状态设为 S，并在请求这笔交易时假装是一个轻客户端。也就是说，如果请求这笔交易的过程，需要客户端确定一个账户的余额，这个轻客户端(由服务器模拟的)会发出一个余额查询请求。如果需要轻客户端在特点某个合约的存储中查询特定的条目，这个轻客户端就会发出这样的请求。也就是说服务器(通过模拟一个轻客户端)正确回应所有自己的请求，但服务器也会跟踪它所有发回的数据。

　　然后，服务器从上述的这些请求中把数据合并并把数据以一个证明的方式发送给客户端。

　　然后，客户端会进行相同的步骤，但会将服务器提供的证明作为一个数据库来使用。如果客户端进行步骤的结果和服务器提供的是一样的话，客户端就接受这个证明。
  
###  MPT(Merkle Patricia Trees)

　　前面我们提到，最为简单的一种Merkle Tree大多数情况下都是一棵二叉树。然而，Ethereum所使用的Merkle Tree则更为复杂，我们称之为“梅克尔.帕特里夏树”（Merkle Patricia tree）。

　　对于验证属于list格式（本质上来讲，它就是一系列前后相连的数据块）的信息而言，二叉Merkle Tree是非常好的数据结构。对于交易树来说，它们也同样是不错的，因为一旦树已经建立，花多少时间来编辑这棵树并不重要，树一旦建立了，它就会永远存在并且不会改变。

　　但是，对于状态树，情况会更复杂些。以太坊中的状态树基本上包含了一个键值映射，其中的键是地址，而值包括账户的声明、余额、随机数nounce、代码以及每一个账户的存储（其中存储本身就是一颗树）。例如，摩登测试网络（the Morden testnet ）的创始状态如下所示：
  
<p align="center">
<img src="https://github.com/Amberlan1001/Knowledge_Summary/blob/master/pic/MPT.png" width="500" height="300" align="center"/>
</p> 

   然而，不同于交易历史记录，状态树需要经常地进行更新：账户余额和账户的随机数nonce经常会更变，更重要的是，新的账户会频繁地插入，存储的键（ key）也会经常被插入以及删除。我们需要这样的数据结构，它能在一次插入、更新、删除操作后快速计算到树根，而不需要重新计算整个树的Hash。这种数据结构同样得包括两个非常好的第二特征：

* 树的深度是有限制的，即使考虑攻击者会故意地制造一些交易，使得这颗树尽可能地深。不然，攻击者可以通过操纵树的深度，执行拒绝服务攻击（DOS attack），使得更新变得极其缓慢。
* 树的根只取决于数据，和其中的更新顺序无关。换个顺序进行更新，甚至重新从头计算树，并不会改变根。

　　MPT是最接近同时满足上面的性质的的数据结构。MPT的工作原理的最简单的解释是，值通过键来存储，键被编码到搜索树必须要经过的路径中。每个节点有16个孩子，因此路径又16进制的编码决定：例如，键‘dog’的16进制编码是6 4 6 15 6 7，所以从root开始到第六个分支，然后到第四个，再到第六个，再到第十五个，这样依次进行到达树的叶子。

　　在实践中，当树稀少时也会有一些额外的优化，我们会使过程更为有效，但这是基本的原则。

  
## 参考。  
[1]http://www.cnblogs.com/fengzhiwu/p/5524324.html.     
[2]https://www.weusecoins.com/what-is-a-merkle-tree/.      
[3]http://www.8btc.com/merkling-in-ethereum. 
