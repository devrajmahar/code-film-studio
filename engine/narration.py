"""Generic per-film narration generator (edge-tts with Windows SAPI fallback)."""

import asyncio
import importlib.util
import json
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


def convert_to_48k_mono(src, dst, max_dur=None):
    probe = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            src,
        ],
        text=True,
    ).strip()
    dur = float(probe) if probe else 0.0
    af = (
        "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.15:stop_threshold=-45dB,"
        "highpass=f=85,acompressor=threshold=-18dB:ratio=3:attack=5:release=60,"
        "loudnorm=I=-16:TP=-1.5:LRA=9"
    )
    if max_dur and dur > max_dur:
        tempo = min(1.45, (dur / max_dur) * 1.06)
        af = f"atempo={tempo:.4f}," + af
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", dst],
        check=True,
    )


async def generate_for_film(film_dir):
    film = load_film_module(film_dir)
    voice = getattr(film, "VOICE", "en-GB-RyanNeural")
    rate = getattr(film, "VOICE_RATE", "+15%")
    out_dir = os.path.join(film_dir, "build", "voice")
    os.makedirs(out_dir, exist_ok=True)

    manifest = []
    for shot_id, _mod, start_s, dur_s, text, _caps in film.SHOTS:
        mp3_path = os.path.join(out_dir, f"{shot_id}.mp3")
        raw_wav = os.path.join(out_dir, f"{shot_id}_raw.wav")
        wav_path = os.path.join(out_dir, f"{shot_id}.wav")
        used = "edge-tts"
        try:
            await synth_edge(text, mp3_path, voice, rate)
            convert_to_48k_mono(mp3_path, wav_path, max_dur=dur_s - 0.25)
        except Exception as exc:
            print(f"[warn] edge-tts failed for {shot_id} ({exc}), using SAPI fallback")
            used = "sapi"
            synth_sapi_fallback(text, raw_wav)
            convert_to_48k_mono(raw_wav, wav_path, max_dur=dur_s - 0.25)
        d = wav_duration(wav_path)
        print(f"  {shot_id}: {d:.2f}s (shot={dur_s:.2f}s) [{used}]")
        manifest.append({"id": shot_id, "start": start_s + 0.12, "clip_duration": d, "wav": wav_path})

    audio_spec = {
        "duration": float(film.TOTAL_DURATION),
        "bpm": getattr(film, "AUDIO_BPM", 120),
        "progression": getattr(film, "AUDIO_PROGRESSION", []),
        "sfx": getattr(film, "AUDIO_SFX", []),
        "narration": manifest,
    }
    spec_path = os.path.join(film_dir, "build", "audio_spec.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(audio_spec, f, indent=2)
    print(f"Wrote {spec_path}")
    return spec_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python engine/narration.py <path/to/films/slug>")
        sys.exit(1)
    asyncio.run(generate_for_film(os.path.abspath(sys.argv[1])))
