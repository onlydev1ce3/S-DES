# S-DES
根据S-DES算法，来编程实现加、解密程序。

![image](https://github.com/onlydev1ce3/S-DES/assets/145557897/cac49b40-c998-4c7e-a05b-6916afdaa74f)


第1关：基本测试       
根据S-DES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是8bit的数据和10bit的密钥，输出是8bit的密文。 

![image](https://github.com/onlydev1ce3/S-DES/assets/145557897/dd622aa2-6ff1-42b7-b286-5daddb5e55cc)
![image](https://github.com/onlydev1ce3/S-DES/assets/145557897/5506c6b0-e753-4c48-9709-00758e5dbc83)

第2关：交叉测试考虑到是算法标准，所有人在编写程序的时候需要使用相同算法流程和转换单元(P-Box、S-Box等)，以保证算法和程序在异构的系统或平台上都可以正常运行。设有A和B两组位同学(选择相同的密钥K)；则A、B组同学编写的程序对明文P进行加密得到相同的密文C；或者B组同学接收到A组程序加密的密文C，使用B组程序进行解密可得到与A相同的P。

通过✔

第3关：扩展功能考虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为1 Byte)，对应地输出也可以是ACII字符串(很可能是乱码)。

![image](https://github.com/onlydev1ce3/S-DES/assets/145557897/25a9e60a-eb10-4879-998d-227114510f05)
![image](https://github.com/onlydev1ce3/S-DES/assets/145557897/cb8d8274-57dd-47e7-8f90-7a2366c3a085)



第4关：暴力破解假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用暴力破解的方法找到正确的密钥Key。在编写程序时，你也可以考虑使用多线程的方式提升破解的效率。请设定时间戳，用视频或动图展示你在多长时间内完成了暴力破解。

![image](https://github.com/onlydev1ce3/S-DES/assets/145557897/5bb957a4-8dd5-439a-bd1d-2f66f990b57e)
![image](https://github.com/onlydev1ce3/S-DES/assets/145557897/c98e0b02-aa88-4206-a7bc-17e75fd8fb62)

第5关：封闭测试根据第4关的结果，进一步分析，对于你随机选择的一个明密文对，是不是有不止一个密钥Key？进一步扩展，对应明文空间任意给定的明文分组P_{n}，是否会出现选择不同的密钥K_{i}\ne K_{j}加密得到相同密文C_n的情况？

![image](https://github.com/onlydev1ce3/S-DES/assets/145557897/dac618ce-c327-4fee-b1ac-49935de481c7)


