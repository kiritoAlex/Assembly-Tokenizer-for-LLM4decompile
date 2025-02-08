import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"]="python"
from transformers import LlamaTokenizer
from sentencepiece import sentencepiece_model_pb2 as sp_pb2_model
import sentencepiece as spm
from tokenizers import SentencePieceBPETokenizer

assembly_sp_model_file = '../Assembly-tokenizer.model'

# load
llama_tokenizer = LlamaTokenizer.from_pretrained("yahma/llama-7b-hf")
print(llama_tokenizer)
assembly_sp_model = spm.SentencePieceProcessor()
assembly_sp_model.Load(assembly_sp_model_file)

llama_spm = sp_pb2_model.ModelProto()
llama_spm.ParseFromString(llama_tokenizer.sp_model.serialized_model_proto())
assembly_spm = sp_pb2_model.ModelProto()
assembly_spm.ParseFromString(assembly_sp_model.serialized_model_proto())

# print number of tokens
print(len(llama_tokenizer),len(assembly_sp_model))
print(llama_tokenizer.all_special_tokens)
print(llama_tokenizer.all_special_ids)
print(llama_tokenizer.special_tokens_map)

## Add assembly tokens to LLaMA tokenizer
llama_spm_tokens_set=set(p.piece for p in llama_spm.pieces)
print(len(llama_spm_tokens_set))
print(f"Before:{len(llama_spm_tokens_set)}")
for p in assembly_spm.pieces:
    piece = p.piece
    if piece not in llama_spm_tokens_set:
        new_p = sp_pb2_model.ModelProto().SentencePiece()
        new_p.piece = piece
        new_p.score = 0
        llama_spm.pieces.append(new_p)
print(f"New model pieces: {len(llama_spm.pieces)}")

## Save
output_sp_dir = '../Assembly_tokenizer/merged_tokenizer_sp'
output_hf_dir = '../Assembly_tokenizer/merged_tokenizer_hf'
os.makedirs(output_sp_dir,exist_ok=True)
with open(output_sp_dir+'/assembly.model', 'wb') as f:
    f.write(llama_spm.SerializeToString())
tokenizer = LlamaTokenizer(vocab_file=output_sp_dir+'/assembly.model')
tokenizer.save_pretrained(output_hf_dir)
