from flask import Flask, request

app = Flask(__name__)


# VULN 1: eval() on user-supplied discount formula - arbitrary code execution
@app.route("/cart/apply-discount", methods=["POST"])
def apply_discount():
    formula = request.json.get("formula")  # e.g., "price * 0.9"
    price = float(request.json.get("price", 0))
    result = eval(formula)
    return {"discounted_price": result}


# VULN NEW: PR gate retry — code injection via eval on user input (Critical)
@app.route("/pr-gate/retry-eval")
def pr_gate_retry_eval():
    return str(eval(request.args.get("expr", "")))


# VULN 2: exec() on user-controlled shipping rule script
@app.route("/admin/shipping-rules", methods=["POST"])
def update_shipping_rules():
    rule_code = request.json.get("rule")
    exec(rule_code)
    return {"status": "rules updated"}


# VULN 3: eval() in product filter expression - user controls filter logic
@app.route("/products/filter")
def filter_products():
    filter_expr = request.args.get("filter")
    products = get_all_products()
    filtered = [p for p in products if eval(filter_expr, {"p": p})]
    return {"products": filtered}


def get_all_products():
    return []
