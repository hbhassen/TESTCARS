import time
import grpc
import json
from pathlib import Path
from difflib import SequenceMatcher

import testautomation_pb2 as ta
import testautomation_pb2_grpc as ta_grpc

# === CONFIGURATION ===
GRPC_ADDR = "localhost:50051"
ROOT_NODE = "AICORE"  # ou "Model"
MODEL_CFG = r"C:/Users/py13733/modeTo/DetectModeTrain/Models/MODDETECTOBJ/model.modelcfg"
CSV_OUT = Path(r"D:\results\detectmode_comparison.csv")
REF_JSON = Path(r"D:\DetectMode\testso.json")  # ton fichier de référence

# ---------------------------------------------------------------------
# 1️⃣ Connexion et configuration de PROVEtech:TA / AI-Core
# ---------------------------------------------------------------------
def connect():
    ch = grpc.insecure_channel(GRPC_ADDR)
    app = ta_grpc.ApplicationStub(ch)
    sys = ta_grpc.SystemStub(ch)
    mea = ta_grpc.MeasureStub(ch)
    return app, sys, mea

def init_app(app):
    app.Init(ta.ApplicationInitRequest())
    print("[INFO] Application initialisée.")

def start_measure(mea):
    mea.SetVideoAudio(ta.MeasureSetVideoAudioRequest(
        strName="LocalVideo",
        bActivate=True,
        bPauseVideoInitially=False,
        bPauseAudioInitially=False
    ))
    mea.Start(ta.MeasureStartRequest())
    print("[INFO] Mesure démarrée.")

def stop_measure(mea):
    mea.Stop(ta.MeasureStopRequest())
    print("[INFO] Mesure arrêtée.")

# ---------------------------------------------------------------------
# 2️⃣ Lecture dynamique des signaux AI-Core
# ---------------------------------------------------------------------
def poll_ai_core_results(sys, duration_s=10, period_s=0.5):
    rows = []
    t0 = time.time()

    while time.time() - t0 < duration_s:
        try:
            res = sys.GetSignal(ta.SystemGetSignalRequest(
                strSignalName=f"{ROOT_NODE}.IconDetection.Result", bInterpreted=True
            )).RetVal_string

            score = sys.GetSignal(ta.SystemGetSignalRequest(
                strSignalName=f"{ROOT_NODE}.IconDetection.Score", bInterpreted=True
            )).RetVal_double

            content = sys.GetSignal(ta.SystemGetSignalRequest(
                strSignalName=f"{ROOT_NODE}.IconDetection.Content", bInterpreted=True
            )).RetVal_string

            frame = round(time.time() - t0, 2)
            rows.append({
                "Frame": frame,
                "Detected": res.strip(),
                "Score": round(score, 3),
                "Content": content.strip()
            })
            print(f"[Frame {frame}] {res} (score={score:.2f})")
        except Exception as e:
            print(f"[WARN] Lecture signal échouée: {e}")
        time.sleep(period_s)

    return rows

# ---------------------------------------------------------------------
# 3️⃣ Chargement du fichier testso.json (référence)
# ---------------------------------------------------------------------
def load_reference_results(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[INFO] {len(data)} entrées de référence chargées depuis {path.name}")
        return data
    except Exception as e:
        print(f"[ERREUR] Impossible de charger {path}: {e}")
        return []

# ---------------------------------------------------------------------
# 4️⃣ Comparaison des résultats obtenus vs référence
# ---------------------------------------------------------------------
def compare_results(live, ref):
    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()

    comparison = []
    for i, frame in enumerate(live):
        if i < len(ref):
            expected = ref[i].get("Result", "").strip()
            detected = frame.get("Detected", "").strip()
            sim = similarity(expected, detected)
            match = "OK" if sim > 0.9 else "DIFF"
            score_diff = round(abs(float(frame.get("Score", 0)) - float(ref[i].get("Score", 0))), 3)
            comparison.append({
                "Frame": i,
                "Expected": expected,
                "Detected": detected,
                "Match": match,
                "Similarity": round(sim, 2),
                "ScoreDiff": score_diff
            })
        else:
            comparison.append({
                "Frame": i,
                "Expected": "N/A",
                "Detected": frame.get("Detected"),
                "Match": "EXTRA",
                "Similarity": 0.0,
                "ScoreDiff": "-"
            })
    return comparison

# ---------------------------------------------------------------------
# 5️⃣ Sauvegarde du rapport CSV et JSON
# ---------------------------------------------------------------------
def save_report_csv(data, path: Path):
    header = "Frame,Expected,Detected,Match,Similarity,ScoreDiff\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(header)
        for d in data:
            f.write(f"{d['Frame']},{d['Expected']},{d['Detected']},{d['Match']},{d['Similarity']},{d['ScoreDiff']}\n")
    print(f"[INFO] Rapport CSV exporté → {path}")

def save_report_json(data, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[INFO] Rapport JSON exporté → {path}")

# ---------------------------------------------------------------------
# 6️⃣ Main
# ---------------------------------------------------------------------
if __name__ == "__main__":
    app, sys, mea = connect()
    init_app(app)

    start_measure(mea)
    live_results = poll_ai_core_results(sys, duration_s=20, period_s=0.5)
    stop_measure(mea)

    ref_results = load_reference_results(REF_JSON)
    comparison = compare_results(live_results, ref_results)

    save_report_csv(comparison, CSV_OUT)
    save_report_json(comparison, CSV_OUT.with_suffix(".json"))

    print("[✅] Comparaison terminée.")
