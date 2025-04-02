import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


save_dir = "/home/models/PMC_LLaMA_13B"
tokenizer = AutoTokenizer.from_pretrained(save_dir, unk_token="<unk>",
                                          bos_token="<s>",
                                          eos_token="</s>")

model = AutoModelForCausalLM.from_pretrained(save_dir,
                                             torch_dtype=torch.float16,
                                             low_cpu_mem_usage=True,
                                             trust_remote_code=True,
                                             revision='main',
                                             device_map='auto')


def generate(prompt):
    batch = tokenizer(
        prompt,
        return_tensors="pt",
        add_special_tokens=False
    )

    with torch.no_grad():
        generated = model.generate(inputs=batch["input_ids"].to('cuda'), max_length=2000, do_sample=True, top_k=5)

    answer = tokenizer.decode(generated[0])
    if answer.find('Your answer is:') > -1:
        answer = answer.split('Your answer is:')[-1]
    answer.replace('</s><s>', '')
    return answer


if __name__ == '__main__':
    prompt = "How do factors such as maternal obesity, smoking, methadone use, and supplementation with iron-folic acid (IFA) affect fetal and neonatal outcomes including birth weight, gestational age, neonatal mortalities, psychomotor development, breastfeeding initiation and duration, and the occurrence of conditions like Hypoplastic Left Heart Syndrome (HPS), macrosomia, and body composition measurements at birth? Then tell me what else you know about these." \
             "Your answer is: "

    print("***************")
    print(generate(prompt))

    prompt = \
        "How does acute and chronic exercise influence blood pressure levels in individuals with diabetes mellitus, metabolic syndrome patients, and subjects with hypertension, taking into consideration the impact of factors such as myocardial stiffness, plasma ascorbic acid levels, and dietary acid load on blood pressure regulation? Then tell me what else you know about these."\
        "Your answer is: "

    print("***************")
    print(generate(prompt))

    prompt = \
        "Can you describe what Interventional Pain Management is and how it is practiced in the USA to alleviate pain? Then tell me what else you know about these."\
        "Your answer is: "

    print("***************")
    print(generate(prompt))


