from typing import Any
from transformers import AutoModelForCausalLM, AutoModel, AutoTokenizer
from ray import serve
from postprocess import decode
import re

@serve.deployment(num_replicas=1, ray_actor_options={"num_gpus": 1})
class MuPT:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("m-a-p/MuPT_v1_8192_1.3B",
                                                    trust_remote_code=True,
                                                    use_fast=False)
        self.model = AutoModelForCausalLM.from_pretrained("m-a-p/MuPT_v1_8192_1.3B").eval().half().cuda()

    def to_abc_format(self,s):
        s=re.sub("<n>","\n",s)
        s=re.sub("<eos>","",s)
        return s
    
    async def __call__(self, request) -> Any:
        r = await request.json()
        inputs = self.tokenizer(r["prompt"], return_tensors="pt").to(self.model.device)
        max_length = r["tokens_to_generate"]
        outputs = self.model.generate(
            inputs.input_ids,
            max_length=max_length
        )
        outputs = self.tokenizer.decode(outputs[0])
        outputs = decode(outputs)
        outputs = self.to_abc_format(outputs)
        return outputs
    
app = MuPT.bind()
serve.run(app, route_prefix="/")
