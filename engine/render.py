"""Unified CLI for Code Film Studio — dynamic camera motion, whip-slide transitions & audio-synced MP4."""

import argparse
import glob
import importlib
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import cv2
import numpy as np
from PIL import Image

STUDIO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE_DIR = os.path.join(STUDIO_ROOT, "engine")
TRANS_FRAMES = 6  # 0.20s snappy whip-slide transition between every shot


def _setup_paths(film_dir):
    for p in (film_dir, ENGINE_DIR, STUDIO_ROOT):
        if p not in sys.path:
            sys.path.insert(0, p)


def _load_shot_schedule(film_dir, film):
    spec_path = os.path.join(film_dir, "build", "audio_spec.json")
    if os.path.exists(spec_path):
        with open(spec_path, "r", encoding="utf-8") as f:
            spec = json.load(f)
        if spec.get("shots"):
            sched = [(s["id"], s["module"], int(s["start_frame"]), int(s["n_frames"])) for s in spec["shots"]]
            return sched, int(spec["total_frames"])
    sched = []
    for shot in film.SHOTS:
        sf, nf = film.shot_frame_range(shot)
        sched.append((shot[0], shot[1], sf, nf))
    return sched, int(film.TOTAL_FRAMES)


def _apply_camera_motion(arr, local_i, n_frames):
    """Subtle energetic Shorts camera punch-in on entrance + smooth continuous push-in."""
    h, w = arr.shape[:2]
    t = local_i / max(1, n_frames - 1)
    # Quick 7-frame punch-out settle (1.045 -> 1.00) + gentle push-in across shot (1.00 -> 1.028)
    punch = 0.045 * max(0.0, 1.0 - local_i / 7.0) ** 2
    zoom = 1.0 + punch + 0.028 * t
    if zoom <= 1.001:
        return arr
    nw, nh = int(w / zoom), int(h / zoom)
    x0 = (w - nw) // 2
    y0 = (h - nh) // 2
    crop = arr[y0 : y0 + nh, x0 : x0 + nw]
    return cv2.resize(crop, (w, h), interpolation=cv2.INTER_LINEAR)


def _whip_blend(prev_arr, cur_arr, u, direction=1):
    """Snappy directional whip-slide transition with slight motion blur for high-retention Shorts flow."""
    h, w = cur_arr.shape[:2]
    # Fast S-curve ease
    e = u * u * (3.0 - 2.0 * u)
    shift = int(w * e)
    out = np.empty_like(cur_arr)
    if direction >= 0:
        # Incoming slides in from right -> left
        split = w - shift
        if split > 0:
            out[:, :split] = prev_arr[:, shift:]
        if shift > 0:
            out[:, split:] = cur_arr[:, :shift]
    else:
        # Incoming slides in from left -> right
        if shift > 0:
            out[:, :shift] = cur_arr[:, w - shift :]
        if w - shift > 0:
            out[:, shift:] = prev_arr[:, : w - shift]

    # Subtle horizontal motion blur peak mid-transition
    blur_k = int(1 + 2 * round(10 * np.sin(np.pi * u)))
    if blur_k >= 3:
        out = cv2.blur(out, (blur_k, 1))
    return out


def _render_chunk(args):
    film_dir, shot_idx, mod_name, prev_mod_name, prev_n_frames, start_global, n_frames, idx_list, out_dir = args
    _setup_paths(film_dir)
    mod = importlib.import_module(mod_name)
    prev_mod = importlib.import_module(prev_mod_name) if prev_mod_name else None

    for local_i in idx_list:
        global_i = start_global + local_i
        cur_arr = np.array(mod.render(local_i, n_frames, global_i), dtype=np.uint8)
        cur_arr = _apply_camera_motion(cur_arr, local_i, n_frames)

        # Blend first TRANS_FRAMES of each shot (after shot 0) with a snappy whip-slide from previous shot
        if prev_mod is not None and local_i < TRANS_FRAMES:
            prev_local = max(0, prev_n_frames - 1)
            prev_arr = np.array(prev_mod.render(prev_local, prev_n_frames, max(0, start_global - 1)), dtype=np.uint8)
            prev_arr = _apply_camera_motion(prev_arr, prev_local, prev_n_frames)
            u = (local_i + 1) / float(TRANS_FRAMES + 1)
            direction = 1 if (shot_idx % 2 == 1) else -1
            cur_arr = _whip_blend(prev_arr, cur_arr, u, direction=direction)

        Image.fromarray(cur_arr, mode="RGB").save(os.path.join(out_dir, f"f_{global_i:05d}.png"), compress_level=1)
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
    sched, _total = _load_shot_schedule(film_dir, film)
    stills_dir = os.path.join(film_dir, "build", "stills")
    os.makedirs(stills_dir, exist_ok=True)
    for shot_id, mod_name, start_f, n_frames in sched:
        mod = importlib.import_module(mod_name)
        mid = n_frames // 2
        img = mod.render(mid, n_frames, start_f + mid)
        out = os.path.join(stills_dir, f"{shot_id}_mid.png")
        img.save(out)
        print(f"Saved still: {out}")


def render_frames(film_dir, jobs):
    _setup_paths(film_dir)
    film = importlib.import_module("film")
    sched, total = _load_shot_schedule(film_dir, film)
    frames_dir = os.path.join(film_dir, "build", "frames")
    os.makedirs(frames_dir, exist_ok=True)
    for old in glob.glob(os.path.join(frames_dir, "f_*.png")):
        os.remove(old)

    t0 = time.time()
    tasks = []
    for idx, (_shot_id, mod_name, start_f, n_frames) in enumerate(sched):
        prev_mod_name = sched[idx - 1][1] if idx > 0 else None
        prev_n_frames = sched[idx - 1][3] if idx > 0 else 0
        for c0 in range(0, n_frames, 30):
            chunk = list(range(c0, min(n_frames, c0 + 30)))
            tasks.append((film_dir, idx, mod_name, prev_mod_name, prev_n_frames, start_f, n_frames, chunk, frames_dir))

    done = 0
    print(f"Rendering {total} frames ({film.WIDTH}x{film.HEIGHT} @ {film.FPS}fps) with whip transitions using {jobs} workers...")
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
    ap.add_argument("film", help="Film folder name inside films/ (e.g. japan-vs-india-trains)")
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
    if args.audio or run_all:
        build_audio(film_dir)
    if args.stills:
        render_stills(film_dir)
    if args.render or run_all:
        render_frames(film_dir, args.jobs)
    if args.assemble or run_all:
        assemble(film_dir, args.film)


if __name__ == "__main__":
    main()
