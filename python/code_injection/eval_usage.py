from flask import Flask, request
import pickle
import os

app = Flask(__name__)


# VULN NEW: code injection via eval on user input (Critical) - PR gateway test
@app.route("/pr-gate/eval")
def pr_gate_eval():
    expr = request.args.get("expr", "")
    return str(eval(expr))


# VULN NEW: insecure deserialization on user data (Critical) - PR gateway test
@app.route("/pr-gate/unpickle", methods=["POST"])
def pr_gate_unpickle():
    return str(pickle.loads(request.data))


# VULN NEW: command injection via os.system on user input (Critical) - PR gateway test
@app.route("/pr-gate/ping")
def pr_gate_ping():
    host = request.args.get("host", "")
    os.system("ping -c 1 " + host)
    return "ok"



# VULN 1: eval() on user-supplied discount formula - arbitrary code execution
@app.route("/cart/apply-discount", methods=["POST"])
def apply_discount():
    formula = request.json.get("formula")  # e.g., "price * 0.9"
    price = float(request.json.get("price", 0))
    result = eval(formula)
    return {"discounted_price": result}


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
