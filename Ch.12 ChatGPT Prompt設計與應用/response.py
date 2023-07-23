from sentence_transformers import util
import openai
def creat_few_shot_pormpting(model, dialog, QA_list):
    init_prompt = '接下來的問題都要使用zh-tw回答。\n你是一個經濟部智慧財產局的客服人員，你需要根據以下的一些提示來回答用戶的問題:'
    
   
    # 相似度檢測
    QA_emb = model.encode(QA_list)
    dialog_emb = model.encode([dialog])
    cos_sim = util.cos_sim(QA_emb, dialog_emb)
    combo = [[cos_sim[i], i] for i in range(len(cos_sim))]
    combo = sorted(combo, key=lambda x: x[0], reverse=True)
    
    few_shot = [QA_list[i] for _, i in combo[:5]]
    few_shot = '\n'.join(few_shot)
    
    msg = init_prompt + '\n' + few_shot
    
    return {"role": "system", "content": msg}
    

def GPT(model, dialog, QA_list, gpt_version):
    
    dialog[0] = creat_few_shot_pormpting(model, dialog[-1], QA_list)
    
    response = openai.ChatCompletion.create(
        engine=gpt_version, 
        messages=dialog
    )
    
    return response.choices[0].message.content
