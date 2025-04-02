import argparse
import json
from tqdm import tqdm
from utils.openai_api import call_gpt35_api, call_gpt4_api

def generate_kp(input_file, output_file, domain, flag_from_beginning=True, start_idx=0):
    """
    Generate knowledge units
    
    Parameters:
        input_file: Raw text file path
        output_file: Knowledge unit output path
        domain: Domain name (e.g., legal-theory)
        flag_from_beginning: Whether to process from file beginning
        start_idx: Starting processing index
    """
    
    flag = flag_from_beginning
    idx_ = 0
    with open(input_file, 'r') as f:
        for line in tqdm(f):
            # data = json.loads(line)
            # text = data["text"]
            text = line.strip()
            if idx == idx_ or flag:
                # print(text)
                flag = True
            if flag:
                kp_data = {
                    "knowledge_unit": get_kp(text, domain),
                    "text": text
                }
                with open(output_file, 'a', encoding='utf-8') as fi:
                    fi.write(json.dumps(kp_data, ensure_ascii=False) + '\n')

            idx_ += 1



def get_kp(text, domain, api_op='gpt35'):
    instruct = 'You are a assistant for generating a short knowledge unit name of a passage, with a keyword and a brief description. ' \
               'The words of the knowledge unit should be limited within 20 words.' \
               'Here is an example:\n' \
               'The input passage is "The evolution of Earth-Moon system is described by the dark matter fieldfluid model proposed in the Meeting of Division of Particle and Field 2004,American Physical Society. The current behavior of the Earth-Moon system agreeswith this model very well and the general pattern of the evolution of theMoon-Earth system described by this model agrees with geological and fossilevidence. The closest distance of the Moon to Earth was about 259000 km at 4.5billion years ago, which is far beyond the Roche\'s limit. The result suggeststhat the tidal friction may not be the primary cause for the evolution of theEarth-Moon system. The average dark matter field fluid constant derived fromEarth-Moon system data is 4.39 x 10^(-22) s^(-1)m^(-1). This model predictsthat the Mars\'s rotation is also slowing with the angular acceleration rateabout -4.38 x 10^(-22) rad s^(-2)."\n' \
               'then the output is {\"knowledge unit\": \"The evolution of the Earth-Moon system —— based on the dark matter field fluid model\"}'
    inputs = \
        "The following is a {} related description:\n".format(domain) + text + \
        "\nThe form of the output should be: " \
        "{\"knowledge unit\": \"xxxxx\"}" \
        "\nPlease output the answer according to the output format in one line. The xxxxx should be a knowledge unit or NONE without any other information"

    if api_op == 'gpt35':
        r = call_gpt35_api(inst=instruct, inputs=inputs)
    elif api_op == 'gpt4':
        r = call_gpt4_api(inst=instruct, inputs=inputs)
    else:
        r = ''
    if r == 'ATTENTION' or r == 'NONE':
        print('0:' + r)
        return r
    try:
        print('1: ' + str(json.loads(r.strip())))
        knowledge_unit = json.loads(r.strip())["knowledge unit"]
        print(knowledge_unit)
        return knowledge_unit
    except Exception as e:
        knowledge_unit = 'NONE'
        print('2: ' + r)
        print(knowledge_unit)
        return knowledge_unit


def regenerate_kp(kp_text_file, new_kp_text_file, flag_from_beginning, domain, split_passage=''):
    flag = flag_from_beginning
    with open(kp_text_file, 'r') as f:
        for line in tqdm(f):
            data = json.loads(line)
            if data["text"] == split_passage or flag:
                flag = True
            if flag:
                if data["knowledge_unit"] == "NONE" or data["knowledge_unit"] == "ATTENTION":
                    kp_data = {
                        "knowledge_unit": get_kp(data["text"], domain),
                        "text": data["text"]
                    }
                else:
                    kp_data = data
                with open(new_kp_text_file, 'a', encoding='utf-8') as fi:
                    fi.write(json.dumps(kp_data, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract knowledge units from text')
    parser.add_argument('--input', type=str, default='../data/text/legal.txt', help='Input file path')
    parser.add_argument('--output', type=str, default='../data/kps/legal_v1_step1.jsonl', 
                       help='Output file path')
    parser.add_argument('--domain', type=str, default='legal-theory', help='Domain name')
    parser.add_argument('--api', choices=['gpt35', 'gpt4'], default='gpt35', 
                       help='API version to use')
    args = parser.parse_args()

    generate_kp(args.input, args.output, args.domain, api_op=args.api)