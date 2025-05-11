num_razors_per_pack = 4
price_per_pack = 4.00
num_packs = 2
coupon_value = 2.00
total_cost = price_per_pack * num_packs / 2 - coupon_value
total_razors = num_razors_per_pack * num_packs
cost_per_razor = total_cost / total_razors
cost_per_razor_cents = cost_per_razor * 100
answer = cost_per_razor_cents
print(f"The cost per razor is {answer} cents.")