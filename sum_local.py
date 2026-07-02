#!/usr/bin/env python3
"""sum-local — sum-the-yt 的本地檔版（支援 faster-whisper / mlx-whisper 兩種 backend）。

吃本地影片檔（mp4…），跳過 yt-dlp/字幕軌（我們的影片字幕是燒死的、抽不出文字），
直接走 Whisper：ffmpeg 抽音軌 → 轉錄 → 沿用 sum_yt 的 srt_to_text 產出 transcript。

用法：
  uv run python sum_local.py [--engine faster|mlx] [--model small|medium|large-v3]
                             [--no-summary] FILE1 [FILE2 ...]

backend：
  faster  faster-whisper（CPU/int8，吃滿 CPU）
  mlx     mlx-whisper（Apple GPU/Metal，較快、不搶 CPU）

環境變數：SUMLOCAL_MODEL / SUMLOCAL_ENGINE / SUMLOCAL_OUT
產物：videos/local/<slug>/{subtitle.srt, transcript.txt[, summary.md]}（已轉的會跳過）
"""
from __future__ import annotations
import argparse, os, subprocess, time
from pathlib import Path

import sum_yt  # 複用 slugify / segments_to_srt / srt_to_text / summarize_with_claude / _sec_to_srt

INIT_PROMPT = "以下是繁體中文的投資與產業分析教學。"
MLX_REPO = {
    "small": "mlx-community/whisper-small-mlx",
    "medium": "mlx-community/whisper-medium-mlx",
    "large-v3": "mlx-community/whisper-large-v3-mlx",
}


def extract_audio(src: Path, wav: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-nostdin", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000",
         "-f", "wav", str(wav), "-y"],
        check=True, capture_output=True,
    )


def _mlx_segments_to_srt(segments) -> str:
    out = []
    for i, s in enumerate(segments, 1):
        out += [str(i),
                f"{sum_yt._sec_to_srt(s['start'])} --> {sum_yt._sec_to_srt(s['end'])}",
                s["text"].strip(), ""]
    return "\n".join(out)


def make_transcriber(engine: str, model_size: str):
    """回傳 transcribe(wav_path) -> (srt_text, plain_text)。模型只載一次。"""
    if engine == "mlx":
        import mlx_whisper
        repo = MLX_REPO.get(model_size, model_size)

        def t(wav: str):
            r = mlx_whisper.transcribe(wav, path_or_hf_repo=repo, language="zh",
                                       initial_prompt=INIT_PROMPT)
            return _mlx_segments_to_srt(r["segments"]), r["text"].strip()
        return t

    from faster_whisper import WhisperModel
    m = WhisperModel(model_size, device="cpu", compute_type="int8")

    def t(wav: str):
        segs, _ = m.transcribe(wav, vad_filter=True, language="zh", initial_prompt=INIT_PROMPT)
        srt = sum_yt.segments_to_srt(segs)
        return srt, sum_yt.srt_to_text(srt)
    return t


def process(src: Path, transcribe, out_root: Path, do_summary: bool) -> Path:
    d = out_root / sum_yt.slugify(src.stem)
    d.mkdir(parents=True, exist_ok=True)
    if (d / "summary.md").exists() or (d / "transcript.txt").exists():
        sum_yt.log(f"skip（已轉錄）：{d.name}")
        return d

    wav = d / "audio.wav"
    sum_yt.log(f"抽音軌：{src.name}")
    extract_audio(src, wav)

    sum_yt.log(f"轉錄中：{src.name}")
    t0 = time.time()
    srt, text = transcribe(str(wav))
    (d / "subtitle.srt").write_text(srt, encoding="utf-8")
    (d / "transcript.txt").write_text(text, encoding="utf-8")
    sum_yt.log(f"轉錄完成：{len(text)} 字，耗時 {time.time()-t0:.0f}s → {d.name}")

    if do_summary and text.strip():
        sum_yt.log("摘要中（claude -p）…")
        (d / "summary.md").write_text(
            sum_yt.summarize_with_claude(text, src.stem, None, 120000), encoding="utf-8")

    try:
        wav.unlink()
    except OSError:
        pass
    return d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--engine", default=os.environ.get("SUMLOCAL_ENGINE", "faster"),
                    choices=["faster", "mlx"])
    ap.add_argument("--model", default=os.environ.get("SUMLOCAL_MODEL", "small"))
    ap.add_argument("--no-summary", action="store_true")
    args = ap.parse_args()

    out_root = Path(os.environ.get("SUMLOCAL_OUT", "videos/local"))
    sum_yt.log(f"backend={args.engine} model={args.model}")
    transcribe = make_transcriber(args.engine, args.model)

    for f in args.files:
        src = Path(f)
        if not src.exists():
            sum_yt.log(f"找不到：{f}")
            continue
        try:
            print(f"✅ {process(src, transcribe, out_root, not args.no_summary)}")
        except Exception as e:  # noqa: BLE001
            sum_yt.log(f"處理失敗：{f}：{e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
