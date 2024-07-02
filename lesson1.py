#!/usr/bin/env python
# coding: utf-8

# In[27]:


import langchain
from langchain.llms import Ollama
from langchain_openai import ChatOpenAI
import json, re


# In[2]:


# https://levelup.gitconnected.com/introduction-to-ollama-part-1-1156f9563b8d
# https://levelup.gitconnected.com/introduction-to-ollama-part-2-e8516105f600
# https://ollama.com/library
# https://stackoverflow.com/questions/77550506/what-is-the-right-way-to-do-system-prompting-with-ollama-in-langchain-using-pyth
# https://python.langchain.com/v0.2/docs/integrations/chat/openai/


# In[3]:


# ollama list
# NAME            ID              SIZE    MODIFIED
# aya:latest      7ef8c4942023    4.8 GB  3 hours ago
# phi3:latest     64c1188f2485    2.4 GB  3 hours ago
# llama3:latest   365c0bd3c000    4.7 GB  3 hours ago
# mistral:latest  2ae6f6dd7a3d    4.1 GB  4 hours ago


# In[4]:


SYSTEM_PROMPT = 'You are a student in IT learning AI'


# In[5]:


llm = None
model = None


# In[6]:


with open('../../openai_api_key.txt') as f:
    openai_api_key = f.read()


# In[ ]:





# In[7]:


def get_response(model_, prompt):
    global model, llm
    is_gpt =  model_.startswith('gpt')
    
    if model_ == model \
            and llm is not None \
            and model is not None:
        pass 
    else: # initialize llm only if new model is passd
        model = model_
        if is_gpt:
            llm = ChatOpenAI(
            model=model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=openai_api_key
            )
        else:
            llm = Ollama(
            verbose=True,
            model=model
            )
            
    messages = [
    ("system", SYSTEM_PROMPT ),
    ("human", prompt) ]
    
    response = llm.invoke(input=messages)

    try:
        response = response.content
    except:
    	pass
        
    return response 


# In[8]:


models = ['aya','mistral','llama3','phi3','gpt-4o','gpt-4-turbo','gpt-3.5-turbo-0125']


# In[9]:


tasks = ['Jak by mohlo zavedení univerzálního základního příjmu ovlivnit ekonomickou disparitu v regionech s vysokými a nízkými příjmy?',
         'Mohl byste nastínit metodu syntézy nové sloučeniny, která by mohla potenciálně absorbovat více sluneční energie než současné fotovoltaické materiály?',
         'Vytvořte pohádku pro mé dva kluky (3 a 5 let) s želvími ninji v Praze. Příběh by měl mít 15 minut na přečtení.']


# In[10]:


results = []


# In[11]:


for m in models[:]:
    for task_id, prompt in enumerate(tasks):
        print(m, task_id, '>>>')
        res = get_response(m, prompt)
        print(llm)
        print(res, end='\n<<<\n')
        results.append((m, str(llm), task_id, res))


# In[14]:


keys = ['model','llm_str','task_id','response']


# In[19]:


pre_json = [{k:v for k,v in zip(keys, r)} for r in results]


# In[20]:


with open('answers_lesson01.json', 'wt+') as f:
    json.dump(pre_json, f)


# In[28]:


def json_to_md(dict_list):
    # Parse the JSON string
    data = dict_list

    # Initialize a list to hold the Markdown strings
    md_lines = []

    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)

    # Loop through each dictionary in the JSON array
    for item in data:
        # Extract fields from the dictionary
        model = item.get("model", "")
        llm_str = item.get("llm_str", "")
        task_id = item.get("task_id", "")
        response = item.get("response", "")

        llm_str_cleaned = ansi_escape.sub('', llm_str)


        # Format the Markdown string
        md_lines.append(f"# Model: {model}")
        md_lines.append(f"## Task ID: {task_id}")
        # md_lines.append(f"**Model:** {model}")
        # md_lines.append(f"**LLM String:** {llm_str}")
        md_lines.append("**LLM String:**")
        md_lines.append(f"```\n{llm_str_cleaned}\n```")
        md_lines.append("\n**Response:**")
        md_lines.append(response)
        md_lines.append("\n---\n")

    # Join the list into a single string with newlines
    md_content = "\n".join(md_lines)

    return md_content


# In[29]:


with open('ANSWERS_LESSON01.md', 'wt+') as f:
    f.write(json_to_md(pre_json))


# In[ ]:




