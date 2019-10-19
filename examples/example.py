import sys
sys.path.insert(0, "/Users/kieran/Git/MonteCarlo/src")

import MonteCarlo as MC

types = ["int", "float"]
types2 = ["std::string"]

import itertools

cart_prod_types = itertools.product(types)
other_headers = ["maths.h"]
"""
MC.template(MC.template_getMax, cart_prod_types, [], other_headers)

print(MC.Templates.getMax(1,2))

MC.template(MC.template_getMax, 
            itertools.product(types+types2), ["string"], other_headers)

print(MC.Templates.getMax(1,2))
print(MC.Templates.getMax(1.1,2.2))"""

MC.template(MC.template_Stack, cart_prod_types, [], other_headers)

string_stack = MC.Templates.Stack_1()
string_stack.push(1)
string_stack.push(2)
string_stack.push(3)

for i in range(3):
    print(f"iterating i = {i}")
    print("peek", string_stack.peek())
    print("pop", string_stack.pop())
    print("peek after pop", string_stack.peek())
