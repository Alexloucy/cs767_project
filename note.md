# Experiment Notes

## Problems during experiment

1. google has cap for request per min, limiting the efficiency of the experiment, total entries reduced to save time
2. using few-shot learning alone might not be enough for LLM to perform the tool selection task, in some cases, LLM attempts to solve the question rater than outputing the right tool
   1. question:
      1. Heather's razors come 4 to a pack and cost $4
      2. Jonathan was sad to learn he needed 2 more toy
   2. tried setting temperature to 0, didn't work
   3. adjust few-shot example?
      1. tool correctly identified, yet still tried to solve the problem, reason unclear
   4. fixed by adding a short description at the top of examples, saying below are the examples and answer format
      1. why not used in prior papers, self-refine and critic?
3. one instance of Answer: Search Engine instead of Search Engine
   1. reason also unclear
4. calling MCP tool
   1. changes in the API, hinger long-term usage
5. code execution doesn't work with structured output
   1. use examples to help format output
6. few-shot learning makes Gemini not execute code
   1. break down into two parts, writing code and reflection, remove few-shot learning from execution phase
7. smithery constantly changes it's API, making integration inefficient and unsuitable for long-term usage
