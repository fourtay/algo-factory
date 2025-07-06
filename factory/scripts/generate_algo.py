#!/usr/bin/env python
import argparse, json, pathlib, uuid, openai

BASE_PROMPT = pathlib.Path("factory/prompts/base.md").read_text()

def call_gpt(task: str):
    sys_part, user_part = BASE_PROMPT.split("### USER")
    messages = [
        {"role": "system", "content": sys_part.replace("### SYSTEM\n", "")},
        {"role": "user",   "content": user_part.replace("{strategy_desc}", task)},
    ]
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format={"type": "json_object"},
        max_tokens=600,
        temperature=0.7,
    )
    return json.loads(response.choices[0].message.content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", default="simple RSI strategy")
    args = parser.parse_args()

    cid = f"ALG_{uuid.uuid4().hex[:6]}"
    dest = pathlib.Path("factory/candidates") / cid
    dest.mkdir(parents=True, exist_ok=True)

    files = call_gpt(args.task)
    for f in files["files"]:
        (dest / f["name"]).write_text(f["content"])
    print(f"Generated → {dest}")

if __name__ == "__main__":
    main()
