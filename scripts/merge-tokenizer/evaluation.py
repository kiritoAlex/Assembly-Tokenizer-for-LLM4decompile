from transformers import AutoTokenizer
from sentencepiece import sentencepiece_model_pb2 as sp_pb2_model
import sentencepiece as spm
from tokenizers import SentencePieceBPETokenizer

#Load tokenizers
LLM4Binary_tokenizer = AutoTokenizer.from_pretrained("../../LLM4Binary_tokenizer")
Assembly_tokenizer = AutoTokenizer.from_pretrained("../../Assembly_tokenizer/merged_tokenizer_hf")
#Test tokenizers with sample
sample="""<sch311x_wdt_get_status>:
endbr64
push   %rbp
mov    %rsp,%rbp
sub    $0x20,%rsp
mov    %rdi,-0x18(%rbp)
mov    -0x18(%rbp),%rax
movl   $0x0,(%rax)
lea    0x0(%rip),%rdi
callq  26 <sch311x_wdt_get_status+0x26>
mov    0x0(%rip),%rdx
mov    0x0(%rip),%rax
add    %rdx,%rax
mov    %rax,%rdi
callq  3f <sch311x_wdt_get_status+0x3f>
mov    %al,-0x1(%rbp)
movzbl -0x1(%rbp),%eax
and    $0x1,%eax
test   %eax,%eax
je     61 <sch311x_wdt_get_status+0x61>
mov    -0x18(%rbp),%rax
mov    (%rax),%edx
mov    0x0(%rip),%eax
or     %eax,%edx
mov    -0x18(%rbp),%rax
mov    %edx,(%rax)
lea    0x0(%rip),%rdi
callq  6d <sch311x_wdt_get_status+0x6d>
nop
leaveq
retq"""

with open("./llm4_tokenizer.txt","w") as f:
    for i in LLM4Binary_tokenizer.tokenize(sample):
        f.write(f"{i}\n")

with open("./assembly_tokenizer.txt","w") as f:
    for i in Assembly_tokenizer.tokenize(sample):
        f.write(f"{i}\n") 

with open("../../data/assembly_instruction.txt", "r", encoding="utf-8") as f:
    text = [f.readline() for _ in range(1000000)]
    text = ' '.join(text)

LLM4Binary_tokens = LLM4Binary_tokenizer.tokenize(text)
print("LLM4Binary的分词器: " + str(len(LLM4Binary_tokens)))

Assembly_tokens = Assembly_tokenizer.tokenize(text)
print("扩充词表后的分词器: "+ str(len(Assembly_tokens)))

print("扩充词表带来的效率提升: "+ str((len(LLM4Binary_tokens)-len(Assembly_tokens))/len(LLM4Binary_tokens)))


