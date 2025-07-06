import ast, sys, pathlib

FORBIDDEN_SNIPPETS = ("datetime.utcnow(", ".Now(")

def main():
    path = pathlib.Path(sys.argv[1])
    code = path.read_text()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            snippet = ast.get_source_segment(code, node) or ""
            if any(bad in snippet for bad in FORBIDDEN_SNIPPETS):
                print("🔴 Forbidden time call:", snippet.strip())
                sys.exit(1)
    # clean exit = good
if __name__ == "__main__":
    main()
