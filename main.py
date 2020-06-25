import requests


def add_prefix_to_output(prefix, output):
    if not output["ingressRules"]:
        output["ingressRules"].append({
            "priority": 1,
            "action": "ALLOW",
            "sourceRange": prefix["ip_prefix"],
            "description": "AWS API Gateway"
        })
    else:
        output["ingressRules"].append({
            "priority": output["ingressRules"][-1]["priority"] + 1,
            "action": "ALLOW",
            "sourceRange": prefix["ip_prefix"],
            "description": "AWS API Gateway"
        })


def main():
    prefixes = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json").json()["prefixes"]

    final_prefix_output = {"ingressRules": []}

    for prefix in prefixes:
        if prefix["service"] == "API_GATEWAY":
            add_prefix_to_output(prefix, final_prefix_output)

    with open("final_prefix_output.json", "w") as final_json:
        final_json.write(str(final_prefix_output).replace("'", "\""))


if __name__ == '__main__':
    main()
