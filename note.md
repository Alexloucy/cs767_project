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
8. Code feedback: ['The provided code directly outputs 25, which is incorrect. The problem requires calculating the cost per razor after applying a buy-one-get-one-free discount and a coupon. The correct calculation involves determining the total cost of two packs of razors after the discount and coupon, then dividing by the total number of razors to find the cost per razor in cents.', "The original code incorrectly calculates the cost after the buy-one-get-one-free discount and coupon. It only considers the price of one pack before applying the coupon, and it doesn't account for buying two packs to utilize the BOGO deal effectively. The coupon should be subtracted from the total cost of the packs involved in the BOGO deal. The corrected code addresses these issues by calculating the initial cost of two packs, applying the BOGO discount, subtracting the coupon value, and then calculating the cost per razor in cents.", 'The code has a logical error in calculating the total cost after the buy-one-get-one-free discount. Since Heather buys 2 packs, she gets one free, so she only pays for one pack. The coupon is then applied to this cost. The number of razors is calculated correctly. However, the final cost per razor calculation is incorrect due to the initial error in calculating the cost after the discount and coupon. The correct answer should be 37.5, which rounds to 38.']
9. original few-shot examples too long, model might not output everything under free tier, summarized using gemini 2.5 pro
