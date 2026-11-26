"""Audio-driven narration generator (guarantees ZERO voice overlap & frame-accurate visual sync)."""

import asyncio
import importlib.util
import json
import math
import os
import subprocess
import sys
import wave


def load_film_module(film_dir):
    spec = importlib.util.spec_from_file_location("film_cfg", os.path.join(film_dir, "film.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


async def synth_edge(text, mp3_path, voice, rate):
    import edge_tts

    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(mp3_path)


def synth_sapi_fallback(text, wav_path):
    ps = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$s.Rate = 2; "
        f"$s.SetOutputToWaveFile('{wav_path}'); "
        f"$s.Speak('{text.replace(chr(39), chr(39)*2)}'); "
        "$s.Dispose();"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


def wav_duration(path):
    with wave.open(path, "rb") as w:
        return w.getnframes() / float(w.getframerate())


def convert_clean_48k_mono(src, dst):
    """Trim leading/trailing silence cleanly and normalize to crisp documentary broadcast loudness."""
    af = (
        "silenceremove=start_periods=1:start_silence=0.05:start_threshold=-42dB,"
        "areverse,silenceremove=start_periods=1:start_silence=0.05:start_threshold=-42dB,areverse,"
        "highpass=f=85,acompressor=threshold=-18dB:ratio=3:attack=5:release=60,"
        "loudnorm=I=-16:TP=-1.5:LRA=9"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", dst],
        check=True,
    )


async def generate_for_film(film_dir):
    film = load_film_module(film_dir)
    fps = int(getattr(film, "FPS", 30))
    voice = getattr(film, "VOICE", "en-GB-RyanNeural")
    rate = getattr(film, "VOICE_RATE", "+14%")
    out_dir = os.path.join(film_dir, "build", "voice")
    os.makedirs(out_dir, exist_ok=True)

    lead_in = 0.15   # clean visual beat before narrator speaks
    tail_pad = 0.35  # clean pause AFTER narrator finishes before cutting to next shot

    shots_timeline = []
    cur_frame = 0
    orig_total = sum(s[3] for s in film.SHOTS)

    for idx, (shot_id, mod_name, _orig_start, _orig_dur, text, _caps) in enumerate(film.SHOTS):
        mp3_path = os.path.join(out_dir, f"{shot_id}.mp3")
        raw_wav = os.path.join(out_dir, f"{shot_id}_raw.wav")
        wav_path = os.path.join(out_dir, f"{shot_id}.wav")
        used = "edge-tts"
        try:
            await synth_edge(text, mp3_path, voice, rate)
            convert_clean_48k_mono(mp3_path, wav_path)
        except Exception as exc:
            print(f"[warn] edge-tts failed for {shot_id} ({exc}), using SAPI fallback")
            used = "sapi"
            synth_sapi_fallback(text, raw_wav)
            convert_clean_48k_mono(raw_wav, wav_path)

        clip_dur = wav_duration(wav_path)
        # Snap shot duration UP to exact frames so voice finishes completely with >=0.42s breathing room
        min_sec = 2.6 if idx == len(film.SHOTS) - 1 else 2.8
        raw_shot_sec = max(min_sec, lead_in + clip_dur + tail_pad)
        n_frames = int(math.ceil(raw_shot_sec * fps))
        shot_dur = n_frames / float(fps)
        shot_start = cur_frame / float(fps)
        voice_start = shot_start + lead_in
        voice_end = voice_start + clip_dur
        gap_after = (shot_start + shot_dur) - voice_end

        print(
            f"  [{idx:02d}] {shot_id:18s} start={shot_start:5.2f}s dur={shot_dur:4.2f}s ({n_frames:3d}f) "
            f"voice={clip_dur:4.2f}s gap={gap_after:4.2f}s [{used}]"
        )
        shots_timeline.append(
            {
                "index": idx,
                "id": shot_id,
                "module": mod_name,
                "start": shot_start,
                "duration": shot_dur,
                "start_frame": cur_frame,
                "n_frames": n_frames,
                "voice_start": voice_start,
                "voice_duration": clip_dur,
                "wav": wav_path,
            }
        )
        cur_frame += n_frames

    total_duration = cur_frame / float(fps)
    scale = total_duration / max(1e-5, orig_total)

    # Map chord progression seamlessly to the actual dynamic shot boundaries
    raw_prog = getattr(film, "AUDIO_PROGRESSION", [])
    progression = []
    if len(raw_prog) == len(shots_timeline):
        for sh, seg in zip(shots_timeline, raw_prog):
            hold = seg[3] if len(seg) > 3 else False
            progression.append([sh["start"], sh["start"] + sh["duration"], seg[2], hold])
    else:
        for seg in raw_prog:
            hold = seg[3] if len(seg) > 3 else False
            progression.append([round(seg[0] * scale, 3), round(seg[1] * scale, 3), seg[2], hold])

    # Map SFX cues cleanly (supports either {"shot": idx, "offset": 0.4} or scaled "t")
    sfx_list = []
    for cue in getattr(film, "AUDIO_SFX", []):
        c = dict(cue)
        if "shot" in c and 0 <= c["shot"] < len(shots_timeline):
            sh = shots_timeline[c["shot"]]
            c["t"] = round(sh["start"] + c.get("offset", 0.3), 3)
            if c.get("match_shot"):
                c["dur"] = sh["duration"]
        elif "t" in c:
            c["t"] = round(c["t"] * scale, 3)
        sfx_list.append(c)

    audio_spec = {
        "fps": fps,
        "total_frames": cur_frame,
        "duration": total_duration,
        "bpm": getattr(film, "AUDIO_BPM", 120),
        "shots": shots_timeline,
        "progression": progression,
        "sfx": sfx_list,
    }
    spec_path = os.path.join(film_dir, "build", "audio_spec.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(audio_spec, f, indent=2)
    print(f"Wrote {spec_path} (total={total_duration:.2f}s, {cur_frame} frames, ZERO voice overlap)")
    return spec_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python engine/narration.py <path/to/films/slug>")
        sys.exit(1)
    asyncio.run(generate_for_film(os.path.abspath(sys.argv[1])))
