### Preamble
I've been doing some additional research - to answer the task of Lesson 10. And I came across an LLM Agent architectured that stunned me. Actually I was looking to 'invent' exactly this architecture.  
Essentially this approach is both simple an universal. Husky can be treated as a "Smart Router" Action Generator and the 4 Agents' Expert Models: `[code]`, `[math]`, `[search]` and `[commonsense]`
Thus it makes the architecture work a bit like human brain - with right and left hemispheres being responsible for exact (`[math]`, `[search]`) and creative (`[commonsense]`, `[code]`).
This architecture can be given more models, for other "modes of thinking" and/or "memories". 

## HUSKY
A work was published at [https://arxiv.org/pdf/2406.06469](https://arxiv.org/pdf/2406.06469)

![Figure 1](https://github.com/alexb7373/ai_course/blob/master/husky01.png "Figure 1")
> As shown in Figure 1, **HUSKY** iterates between the two stages until it arrives at a terminal state. The first module in HUSKY is the *action generator*. Given the input question and the solution generated so far, the action generator jointly predicts the next high-level step to take and the associated tool. The tools forming the ontology of our actions are `[code]`, `[math]`, `[search]` and `[commonsense]`. If the final answer to the question has been reached in the solution history, then the action generator returns the answer. Based on the tool assigned by the action generator, HUSKY calls the corresponding tool, executes the tool and re-writes the tool outputs optionally into natural language. Each tool is associated with an expert model - a code generator for *`[code]`*, a math reasoner for *`[math]`*, a query generator for *`[search]`* and a commonsense reasoner for *`[commonsense]`*.

![Figure 2](https://github.com/alexb7373/ai_course/blob/master/husky02.png "Figure 2")
> We introduce HUSKY, with its overview shown in Figure 2. HUSKY is a language agent which solves complex, multi-step reasoning tasks by iterating between two stages: 1) predicting the next action to take, and 2) executing the action with the designated expert model. This process is repeated by HUSKY until the agent arrives at a terminal state. During the first stage, the action generator \( A \) jointly predicts each step \( s \) and tool \( t \) for solving the task, with \( t \) represented by special tokens as summarized in Table 1. The second stage involves executing each step with an expert model, which is either 1) a model that directly generates the output to each step ([math], [commonsense]), or 2) a model that generates the inputs to be executed by the actual tools ([code], [search]). The terminal state is recognized by \( A \) which returns the final answer if it is found in the solution history.

