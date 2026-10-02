"""fal.ai fallback for the visual generator (used when Higgsfield MCP is not connected).

Usage:
  python3 scripts/fal_generate.py image --prompt "..." --out runs/<RUN>/images/A-product.png
  python3 scripts/fal_generate.py rembg --image runs/<RUN>/images/A-product.png --out runs/<RUN>/images/A-cutout.png
  python3 scripts/fal_generate.py 3d    --image runs/<RUN>/images/A-cutout.png  --out runs/<RUN>/model.glb

Without FAL_KEY the script prints what it would send and exits 0 (dry run),
so the pipeline keeps going with prompts only.

Model ids are fal.ai endpoints and can be swapped with --model; check fal.ai/models
if one has been renamed.
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from _env import load_env

DEFAULT_MODELS = {
    "image": "fal-ai/flux/schnell",
    "rembg": "fal-ai/imageutils/rembg",
    "3d": "fal-ai/trellis",
}


def to_data_uri(path: str) -> str:
    mime = mimetypes.guess_type(path)[0] or "image/png"
    data = base64.b64encode(Path(path).read_bytes()).decode()
    return f"data:{mime};base64,{data}"


def call_fal(model: str, payload: dict, key: str) -> dict:
    req = urllib.request.Request(
        f"https://fal.run/{model}",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.loads(resp.read())


def result_url(kind: str, result: dict) -> str:
    if kind == "image":
        return result["images"][0]["url"]
    if kind == "rembg":
        return result["image"]["url"]
    return result["model_mesh"]["url"]


def download(url: str, out: str) -> None:
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    if url.startswith("data:"):
        Path(out).write_bytes(base64.b64decode(url.split(",", 1)[1]))
        return
    with urllib.request.urlopen(url, timeout=300) as resp:
        Path(out).write_bytes(resp.read())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=["image", "rembg", "3d"])
    parser.add_argument("--prompt")
    parser.add_argument("--image")
    parser.add_argument("--out", required=True)
    parser.add_argument("--model")
    parser.add_argument("--size", default="square_hd")
    args = parser.parse_args()

    model = args.model or DEFAULT_MODELS[args.kind]
    if args.kind == "image":
        if not args.prompt:
            parser.error("image needs --prompt")
        payload = {"prompt": args.prompt, "image_size": args.size, "num_images": 1}
    else:
        if not args.image:
            parser.error(f"{args.kind} needs --image")
        payload = {"image_url": to_data_uri(args.image)}

    load_env()
    key = os.environ.get("FAL_KEY")
    if not key:
        preview = {k: (v[:60] + "...") if isinstance(v, str) and len(v) > 60 else v for k, v in payload.items()}
        print(json.dumps({"dry_run": True, "reason": "FAL_KEY not set", "model": model,
                          "payload": preview, "out": args.out}, ensure_ascii=False, indent=2))
        return 0

    try:
        result = call_fal(model, payload, key)
        download(result_url(args.kind, result), args.out)
    except urllib.error.HTTPError as e:
        print(f"fal.ai error {e.code}: {e.read().decode(errors='replace')[:500]}", file=sys.stderr)
        return 1
    except (KeyError, IndexError):
        print(f"Unexpected fal.ai response shape for {model}: {json.dumps(result)[:500]}", file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "model": model, "out": args.out}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
