# Merkle Tree 学习

## Merkle Tree 概念
   
   Merkle Tree，通常也被称作Hash Tree，顾名思义，就是存储hash值的一棵树。Merkle树的叶子是数据块(例如，文件或者文件的集合)的hash值。非叶节点是其对应子节点串联字符串的hash。

   在点对点网络中作数据传输的时候，会同时从多个机器上下载数据，而且很多机器可以认为是不稳定或者不可信的。为了校验数据的完整性，更好的办法是把大的文件分割成小的数据块（例如，把分割成2K为单位的数据块）。这样的好处是，如果小块数据在传输过程中损坏了，那么只要重新下载这一快数据就行了，不用重新下载整个文件。

-- 2. Hash List  

   怎么确定小的数据块没有损坏哪？只需要为每个数据块做Hash。BT下载的时候，在下载到真正数据之前，我们会先下载一个Hash列表。那么问题又来了，怎么确定这个Hash列表本事是正确的哪？答案是把每个小块数据的Hash值拼到一起，然后对这个长字符串在作一次Hash运算，这样就得到Hash列表的根Hash(Top Hash or Root Hash)。下载数据的时候，首先从可信的数据源得到正确的根Hash，就可以用它来校验Hash列表了，然后通过校验后的Hash列表校验数据块。

-- 3. Merkle Tree
    
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



## 参考
http://www.cnblogs.com/fengzhiwu/p/5524324.html
