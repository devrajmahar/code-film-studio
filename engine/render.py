"""Unified CLI for Code Film Studio — build stills, audio, frames & MP4 for any film in films/<slug>/."""

import argparse
import glob
import importlib
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor

STUDIO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE_DIR = os.path.join(STUDIO_ROOT, "engine")


def _setup_paths(film_dir):
    for p in (film_dir, ENGINE_DIR, STUDIO_ROOT):
        if p not in sys.path:
            sys.path.insert(0, p)


def _render_chunk(args):
    film_dir, mod_name, start_global, n_frames, idx_list, out_dir = args
    _setup_paths(film_dir)
    mod = importlib.import_module(mod_name)
    for local_i in idx_list:
        global_i = start_global + local_i
        img = mod.render(local_i, n_frames, global_i)
        img.save(os.path.join(out_dir, f"f_{global_i:05d}.png"), compress_level=1)
    return len(idx_list)


def build_audio(film_dir):
    narration_py = os.path.join(ENGINE_DIR, "narration.py")
    audio_mjs = os.path.join(ENGINE_DIR, "audio_engine.mjs")
    spec_path = os.path.join(film_dir, "build", "audio_spec.json")
    subprocess.run([sys.executable, narration_py, film_dir], check=True)
    subprocess.run(["node", audio_mjs, spec_path], check=True)


def render_stills(film_dir):
    _setup_paths(film_dir)
    film = importlib.import_module("film")
    stills_dir = os.path.join(film_dir, "build", "stills")
    os.makedirs(stills_dir, exist_ok=True)
    for shot in film.SHOTS:
        shot_id, mod_name = shot[0], shot[1]
        start_f, n_frames = film.shot_frame_range(shot)
        mod = importlib.import_module(mod_name)
        mid = n_frames // 2
        img = mod.render(mid, n_frames, start_f + mid)
        out = os.path.join(stills_dir, f"{shot_id}_mid.png")
        img.save(out)
        print(f"Saved still: {out}")


def render_frames(film_dir, jobs):
    _setup_paths(film_dir)
    film = importlib.import_module("film")
    frames_dir = os.path.join(film_dir, "build", "frames")
    os.makedirs(frames_dir, exist_ok=True)
    for old in glob.glob(os.path.join(frames_dir, "f_*.png")):
        os.remove(old)

    t0 = time.time()
    tasks = []
    for shot in film.SHOTS:
        mod_name = shot[1]
        start_f, n_frames = film.shot_frame_range(shot)
        for c0 in range(0, n_frames, 30):
            tasks.append((film_dir, mod_name, start_f, n_frames, list(range(c0, min(n_frames, c0 + 30))), frames_dir))

    done, total = 0, film.TOTAL_FRAMES
    print(f"Rendering {total} frames ({film.WIDTH}x{film.HEIGHT} @ {film.FPS}fps) using {jobs} workers...")
    with ProcessPoolExecutor(max_workers=jobs) as ex:
        for count in ex.map(_render_chunk, tasks):
            done += count
            if done % 180 == 0 or done == total:
                rate = done / max(0.1, time.time() - t0)
                print(f"  {done}/{total} ({100.0 * done / total:.0f}%) — {rate:.1f} frames/s")
    print(f"Rendered {total} frames in {time.time() - t0:.1f}s")


def assemble(film_dir, slug):
    _setup_paths(film_dir)
    film = importlib.import_module("film")
    frames_pattern = os.path.join(film_dir, "build", "frames", "f_%05d.png")
    audio_path = os.path.join(film_dir, "build", "master.wav")
    dist_dir = os.path.join(film_dir, "dist")
    os.makedirs(dist_dir, exist_ok=True)
    out_mp4 = os.path.join(dist_dir, f"{slug}.mp4")

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-framerate", str(film.FPS),
            "-i", frames_pattern,
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "21", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart",
            out_mp4,
        ],
        check=True,
    )
    print(f"DONE! Wrote {out_mp4} ({os.path.getsize(out_mp4) / (1024 * 1024):.2f} MB)")


def main():
    ap = argparse.ArgumentParser(description="Code Film Studio CLI")
    ap.add_argument("film", help="Film folder name inside films/ (e.g. india-vs-europe)")
    ap.add_argument("--stills", action="store_true", help="Render 1 mid-frame still per shot")
    ap.add_argument("--audio", action="store_true", help="Generate narration & procedural audio mix")
    ap.add_argument("--render", action="store_true", help="Render all video frames")
    ap.add_argument("--assemble", action="store_true", help="Encode final MP4 with FFmpeg")
    ap.add_argument("--all", action="store_true", help="Run audio + render + assemble")
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 4) - 1))
    args = ap.parse_args()

    film_dir = os.path.join(STUDIO_ROOT, "films", args.film)
    if not os.path.isdir(film_dir):
        print(f"Film not found: {film_dir}")
        sys.exit(1)

    run_all = args.all or not (args.stills or args.audio or args.render or args.assemble)
    if args.stills:
        render_stills(film_dir)
    if args.audio or run_all:
        build_audio(film_dir)
    if args.render or run_all:
        render_frames(film_dir, args.jobs)
    if args.assemble or run_all:
        assemble(film_dir, args.film)


if __name__ == "__main__":
    main()
