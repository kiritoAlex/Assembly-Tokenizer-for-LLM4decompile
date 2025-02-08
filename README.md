# Assembly-Tokenizer-for-LLM4decompile

## 工作流程
### 扩充词表
Clone AnghaBench from github

``git clone https://github.com/brenocfg/AnghaBench.git``

Compile AnghaBench to get assembly instructions for training(datsets)

```
cd scripts
python compile.py --root ../AnghaBench --output ../assembly_instruction.jsonl
```

由于sentencepiece不能直接使用jsonl格式的文件进行训练，需要转化为txt格式的文本，文件格式为每行一条汇编指令

`python clean_and_transfer.py`

利用汇编指令数据集结合sentencepiece训练得到assembly_sp.model

`spm_train   --input=../assembly_instruction.txt   --model_prefix=../Assembly-tokenizer   --vocab_size=2000   --character_coverage=1   --model_type=bpe   --add_dummy_prefix=false   --input_sentence_size=10000000   --shuffle_input_sentence=1   --train_extremely_large_corpus=1   --num_threads=8`
* --input: 训练数据路径
* --model_prefix: 模型名称，这里是Assembly-tokenizer.model
* --vocab_size: 扩充词表的大小
* --character_coverage: 模型覆盖的字符数量,对于英文训练语料默认为1即可
* --model_type: 训练方法
* --add_dummy_prefix: Sentencepiece训练时默认每行开头有空格并转义为_，这样训练出来的token也会带有空格，例如mov会被训练为_mov，因此需要add_dummy_prefix=false来忽略每行开头的空格
* --input_sentence_size: 个人PC性能有限，因此从语料库中抽取10000000条训练数据
* --shuffle_input_sentence: 打乱训练数据顺序
* --train_extremely_large_corpus: 启用大语料库模式优化内存
* --num_treads: 限制线程数

训练之后得到Assembly-tokenizer.model，将该模型和yahma/llama-7b-hf的tokenizer合并

`python merge_tokenizers.py `

yahma/llama-7b-hf的tokenizer共有32000个tokens，与具有2000个tokens的Assembly-tokenizer.model合并后，新的tokenizer去除重复tokens后共有32821个tokens，模型分别以huggingface格式和sentencepiece格式保存在Assembly——tokenizer文件夹下

### 模型训练(Todo)

LoRA预训练获得LoRA权重参数

将LoRA权重与基础模型deepseek-coder合并

指令精调得到新的LoRA权重

再次进行合并，得到更适用于处理汇编指令的基础模型

### Decompile微调(Todo)

在重新预训练之后的deepseek-coder模型的基础上再进行Decompile微调

## Evaluation of Assembly-Tokenizer

扩充词表后的tokenizer在分词效率和质量上有较大提升

`python evaluation.py`

从分词质量上看，扩充后的tokenizer可以将"endbr","callq"等指令完整识别出来，而LLM4Binary的tokenizer会将其分别识别为"end","br"和"call","q"，由此可见扩充后的tokenizer更有利于保持文本的正确语义

从分词效率上看，evaluation选取了1000000条指令分别做分词，结果如下：

LLM4Binary的分词器: 12799198 tokens
扩充词表后的分词器: 9351474 tokens
扩充词表带来的效率提升: 26.94%

由此可见扩充后的tokenizer也有效提升了分词效率