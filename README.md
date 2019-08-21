# Novel Words Helper
这是一个自动整理外语文本词汇的脚本, 目的是为欲读原著但苦于外语的同学准备一份原著单词表, 目前仅支持英语

## 功能
- 提取单词(还原各种分词形式至原词)
- 过滤简单词
- 统计出现次数及真实词频
- 提供翻译 

## 演示
原文件
> Chapter 1 Mr. Sherlock Holmes  
> IN the year 1878 I took my degree of Doctor of Medicine of the University of London,  
> and proceeded to Netley to go through the course prescribed for surgeons in the army.  
> ...

转为单词表
> word [occurrence number, frequency]
>  
> misfortune [1, 0.000159%]    
> n. 不幸；灾祸，灾难  
> 
> enthusiast [1, 0.000618%]  
> n. 爱好者，热心家；热烈支持者；狂热者，基督教狂热分子  
> ..

## 用法
1.  将小说名作为文件夹包括小说各章节, 并放入novel文件夹.  
例:
    ```
    novel
    └── AStudyInScarlet
        ├── Chapter6.txt
        ├── Chapter7.txt
        ├── Chapter8.txt
        └── Chapter9.txt
    
    1 directory, 4 files
    ```
2. 运行words_report.py, 单词表作为"report_xxx"将被存入report文件夹.
    ```
    report
    └── AStudyInScarlet
        ├── report_Chapter6.txt
        ├── report_Chapter7.txt
        ├── report_Chapter8.txt
        └── report_Chapter9.txt
    
    1 directory, 4 files
    ```

## TODO
- [x] 查词优化
    - nltk词型还原
- [x] 小初高单词过滤
- [ ] 提供web界面, 提供友好的操作(手动过滤, 单词本等可能鸽)