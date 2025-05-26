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
10. both service unreliable, down time significant
11. code feedback summary: ["The code's logic is flawed in the final calculation: it either incorrectly includes extra costs when determining additional movies or fails to account for the initial movie already planned.\n", 'The code incorrectly calculates the total pyramid height by summing individual heights instead of layering them, and it may not consider all members or their specific arrangement within the structure.\n', 'The code accurately performs calculations, but the interpretation of ambiguous language ("well over") could be improved to better reflect the problem\'s intent.\n']
12. search feedback summary: 'Multiple potential answers exist based on initial search results, but further research is required to determine the definitive answer and confirm the earliest instance.\n', 'Initial findings suggest a connection between the provided information and a common concept, but further investigation is needed to confirm the most accurate and widely accepted terminology.\n', 'Initial research confirms a problem affects multiple plants, with one being specifically mentioned, but further investigation is needed to determine prevalence among them.\n', 'Insufficient information exists within the provided context to definitively answer the question; further research is required to provide a conclusive response.\n'
13. Question 2 (razor buy 1 get 1 free): feedback says need improvement despite correct output
    code: cost_per_pack = 4.00
    packs_bought = 2
    coupon = 2.00
    razors_per_pack = 4

total*cost_before_discount = cost_per_pack * packs*bought
cost_after_bogo = cost_per_pack
cost_after_coupon = cost_after_bogo - coupon
total_razors = packs_bought * razors_per_pack
cost_per_razor = cost_after_coupon / total_razors
cost_per_razor_cents = cost_per_razor \* 100

print(cost_per_razor_cents)

Feedback: The original code incorrectly calculates the cost per razor. It only considers the cost of one pack after the buy-one-get-one-free deal and then subtracts the coupon. The coupon should be subtracted from the total cost of the packs. The correct calculation involves considering the total cost after the BOGO deal and coupon, then dividing by the total number of razors.
Result: 25.0

code: total_cost_before_coupon = 4.00
coupon_value = 2.00
total_razors = 8
final_cost = total_cost_before_coupon - coupon_value
cost_per_razor = final_cost / total_razors
cost_per_razor_in_cents = cost_per_razor \* 100
print(int(cost_per_razor_in_cents))

Feedback: The code calculates the cost per razor after applying a coupon but fails to account for the buy-one-get-one-free discount. The total cost should be for one pack since the second is free. The calculation should divide the cost of one pack minus the coupon by the total number of razors in two packs. The current code is missing the buy one get one free discount.
Result: 25

code: pack_cost = 4.00
coupon = 2.00
razors_per_pack = 4
num_packs = 2

cost*after_bogo = pack_cost
cost_after_coupon = cost_after_bogo - coupon
total_razors = num_packs * razors*per_pack
cost_per_razor = cost_after_coupon / total_razors
cost_per_razor_cents = cost_per_razor * 100

print(round(cost_per_razor_cents))

Feedback: The code calculates the cost per razor after applying the buy-one-get-one-free discount and a coupon. However, the buy-one-get-one-free discount is not correctly applied when buying two packs. The coupon should be subtracted from the total cost of two packs after the BOGO discount. The current code only considers the cost of one pack before applying the coupon.
Result: 25 14. Search Question Metrics:
Strict Exact Match Score: 79.00%
Semantic Match Score: 94.00% 15. Code Execution Metrics:
Strict Exact Match Score: 50.00%
Semantic Match Score: 92.00% 16. 16. code feedback summary 1. feedback summary: ['Calculations lacking context hinder understanding and error detection; clearly showing the origin of each number is crucial for accurate problem-solving and verification.\n', 'The code incorrectly used the calculated number of shelves instead of the given number of books in a formula, leading to an inaccurate result.\n', 'The problem requires calculating a total value based on given parameters, but the provided solution is incorrect due to a miscalculation or misunderstanding of the input values.\n', 'Carefully review all provided information and calculations to ensure accuracy, as overlooking details can lead to incorrect results.\n', 'Calculating a discounted total involves finding the discount amount, subtracting it from the original price to get the discounted price, and then multiplying by the quantity.\n', 'The solution involves identifying missing information, performing basic calculations based on given values, and then finding the difference to arrive at the correct answer.\n']

Questions worse off without long term memory: 27, 61, 62, 138, 192
85, 114, 144

no mem code question: Strict Exact Match Score: 84.00%
Semantic Match Score: 95.00%

no mem search: Strict Exact Match Score: 83.00%
Semantic Match Score: 93.00%

mem search: Strict Exact Match Score: 86.00%
Semantic Match Score: 95.00%

mem search v2: Strict Exact Match Score: 86.00%
Semantic Match Score: 97.00%
