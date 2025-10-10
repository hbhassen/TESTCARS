import time
import json
from pathlib import Path
from difflib import SequenceMatcher
import grpc

import testautomation_pb2 as ta
import testautomation_pb2_grpc as ta_grpc

# ===================== CONFIG =====================
GRPC_ADDR = "localhost:50051"
ROOT_NODE = "AICORE"  # Doit correspondre au Root Node défini dans AI-Core

# Source vidéo (nom tel que défini côté TA/AI-Core ; adapter si besoin)
VIDEO_SOURCE_NAME = "FrontCam"   # ou "LocalVideo" selon votre config

# Résultats / références
REF_JSON = Path(r"C:/Users/py13733/modeTo/DetectModeTest/testso.json")
CSV_OUT  = Path(r"./detectmode_run01.csv")

# Noms de signaux (adapter si l’arbo diffère)
SIG_RESULT = "IconDetection.Result"
SIG_SCORE  = "IconDetection.Score"
SIG_CNTNT  = "IconDetection.Content"

# Durées
POLL_DURATION_S = 20
POLL_PERIOD_S   = 0.5
WAIT_SIGNALS_TIMEOUT_S = 30
# ==================================================

def grpc_status(err: Exception):
    if isinstance(err, grpc.RpcError):
        return err.code(), err.details()
    return None, None

def connect():
    ch  = grpc.insecure_channel(GRPC_ADDR)
    app = ta_grpc.ApplicationStub(ch) if hasattr(ta_grpc, "ApplicationStub") else None
    sys = ta_grpc.SystemStub(ch)       if hasattr(ta_grpc, "SystemStub")       else None
    mea = ta_grpc.MeasureStub(ch)      if hasattr(ta_grpc, "MeasureStub")      else None
    # Service "test" (souvent absent ou StartTesting non-implémenté → fallback Measure.*)
    tst = None
    for cand in ["TestAutomationServiceStub", "ApplicationStub", "SystemStub"]:
        if hasattr(ta_grpc, cand):
            tst = getattr(ta_grpc, cand)(ch)
            break
    return app, sys, mea, tst

def init_app(app):
    if app and hasattr(app, "Init"):
        app.Init(ta.ApplicationInitRequest())
        print("[INFO] Application initialisée.")
    else:
        print("[WARN] Service Application.Init indisponible dans ce proto.")

def try_start_testing(tst):
    """Essaie StartTesting si disponible ; fallback sur Measure.Start s'il est UNIMPLEMENTED."""
    if not tst:
        print("[INFO] Pas de service 'test' → on utilisera Measure.Start.")
        return False

    # Si l'RPC n'existe pas, on ne tente pas.
    if not any(hasattr(tst, m) for m in ("StartTesting", "StartTest", "Start")):
        print("[INFO] Aucune méthode StartTesting/StartTest/Start → on utilisera Measure.Start.")
        return False

    # Construit une requête vide/compatible (certains protos ne prennent qu'un Empty)
    request = None
    if hasattr(ta, "StartTestRequest"):
        request = ta.StartTestRequest()  # on n'affecte aucun champ pour éviter les ValueError
    elif hasattr(ta, "Empty"):
        request = ta.Empty()
    else:
        request = ta.ApplicationInitRequest()

    for meth_name in ("StartTesting", "StartTest", "Start"):
        if hasattr(tst, meth_name):
            print(f"[INFO] Tentative de lancement via {meth_name}...")
            try:
                getattr(tst, meth_name)(request)
                print(f"[OK] Lancement via {meth_name}.")
                return True
            except Exception as e:
                code, details = grpc_status(e)
                if code == grpc.StatusCode.UNIMPLEMENTED:
                    print(f"[WARN] {meth_name} non implémenté par le serveur → fallback Measure.Start.")
                    return False
                # Autres erreurs : on continue de tenter les variantes, sinon fallback
                print(f"[WARN] {meth_name} a échoué: {code} {details} → on tentera les variantes/fallback.")
    return False

def start_measure(mea):
    """Chemin standard : active la source vidéo et démarre la mesure."""
    if not mea:
        raise RuntimeError("MeasureStub non disponible dans ce proto.")

    # Activer la source vidéo si RPC dispo
    if hasattr(mea, "SetVideoAudio") and hasattr(ta, "MeasureSetVideoAudioRequest"):
        try:
            mea.SetVideoAudio(ta.MeasureSetVideoAudioRequest(
                strName=VIDEO_SOURCE_NAME,
                bActivate=True,
                bPauseVideoInitially=False,
                bPauseAudioInitially=False
            ))
            print(f"[INFO] Source vidéo activée: {VIDEO_SOURCE_NAME}")
        except Exception as e:
            code, details = grpc_status(e)
            print(f"[WARN] SetVideoAudio a échoué ({code} {details}) — on continue avec Start().")

    if hasattr(mea, "Start") and hasattr(ta, "MeasureStartRequest"):
        mea.Start(ta.MeasureStartRequest())
        print("[OK] Mesure démarrée (Measure.Start).")
    else:
        raise RuntimeError("Measure.Start non disponible dans ce proto.")

def wait_for_signals(sys, timeout_s=WAIT_SIGNALS_TIMEOUT_S, poll=POLL_PERIOD_S):
    """Attend que AICORE.*.Score soit lisible (AI-Core prêt)."""
    if not sys:
        print("[WARN] SystemStub non disponible; on ne peut pas vérifier les signaux.")
        return False
    target = f"{ROOT_NODE}.{SIG_SCORE}"
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        try:
            val = sys.GetSignal(ta.SystemGetSignalRequest(
                strSignalName=target, bInterpreted=True
            )).RetVal_double
            print(f"[INFO] Signal prêt: {target} → {val:.3f}")
            return True
        except Exception:
            time.sleep(poll)
    print("[ERREUR] Timeout: signaux AI-Core non disponibles dans le délai.")
    return False

def poll_ai_core_results(sys, duration_s=POLL_DURATION_S, period_s=POLL_PERIOD_S):
    rows = []
    t0 = time.time()
    for _ in range(int(duration_s/period_s)):
        try:
            res = sys.GetSignal(ta.SystemGetSignalRequest(
                strSignalName=f"{ROOT_NODE}.{SIG_RESULT}", bInterpreted=True
            )).RetVal_string

            score = sys.GetSignal(ta.SystemGetSignalRequest(
                strSignalName=f"{ROOT_NODE}.{SIG_SCORE}", bInterpreted=True
            )).RetVal_double

            content = ""
            try:
                content = sys.GetSignal(ta.SystemGetSignalRequest(
                    strSignalName=f"{ROOT_NODE}.{SIG_CNTNT}", bInterpreted=True
                )).RetVal_string
            except Exception:
                content = ""

            t_rel = round(time.time() - t0, 2)
            rows.append({"Frame": t_rel, "Detected": (res or "").strip(),
                         "Score": round(float(score), 3), "Content": (content or "").strip()})
            print(f"[Frame {t_rel}] {res} (score={score:.2f})")
        except Exception as e:
            code, details = grpc_status(e)
            print(f"[WARN] Lecture signal échouée: {code} {details}")
        time.sleep(period_s)
    return rows

def stop_everything(tst, mea):
    """Arrêt propre : tente StopTesting, sinon Measure.Stop."""
    if tst:
        for meth in ("StopTesting", "StopTest", "Stop"):
            if hasattr(tst, meth):
                try:
                    if hasattr(ta, "StopTestRequest"):
                        getattr(tst, meth)(ta.StopTestRequest())
                    else:
                        getattr(tst, meth)(ta.ApplicationInitRequest())
                    print(f"[OK] Test arrêté via {meth}.")
                    return
                except Exception:
                    pass
    if mea and hasattr(mea, "Stop") and hasattr(ta, "MeasureStopRequest"):
        try:
            mea.Stop(ta.MeasureStopRequest())
            print("[OK] Mesure arrêtée (Measure.Stop).")
        except Exception:
            pass

def load_reference_results(path: Path):
    if not path.exists():
        print(f"[WARN] Référence absente: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"[INFO] {len(data)} entrées de référence chargées depuis {path.name}")
    return data

def compare_results(live, ref):
    def similarity(a, b): return SequenceMatcher(None, a or "", b or "").ratio()
    out = []
    for i, frame in enumerate(live):
        if i < len(ref):
            expected = (ref[i].get("Result") or "").strip()
            detected = (frame.get("Detected") or "").strip()
            sim = similarity(expected, detected)
            match = "OK" if sim >= 0.9 else "DIFF"
            s_live = float(frame.get("Score", 0) or 0)
            s_ref  = float(ref[i].get("Score", 0) or 0)
            out.append({
                "Frame": i, "Expected": expected, "Detected": detected,
                "Match": match, "Similarity": round(sim, 2),
                "ScoreDiff": round(abs(s_live - s_ref), 3)
            })
        else:
            out.append({"Frame": i, "Expected": "N/A", "Detected": frame.get("Detected"),
                        "Match": "EXTRA", "Similarity": 0.0, "ScoreDiff": "-"})
    return out

def save_report_csv(data, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("Frame,Expected,Detected,Match,Similarity,ScoreDiff\n")
        for d in data:
            f.write(f"{d['Frame']},{d['Expected']},{d['Detected']},{d['Match']},{d['Similarity']},{d['ScoreDiff']}\n")
    print(f"[INFO] Rapport CSV exporté → {path.resolve()}")

def save_report_json(data, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[INFO] Rapport JSON exporté → {path.resolve()}")

# ===================== MAIN =====================
if __name__ == "__main__":
    app, sys, mea, tst = connect()
    init_app(app)

    # 1) Essai StartTesting → fallback Measure.Start si UNIMPLEMENTED
    started_by_test = try_start_testing(tst)
    if not started_by_test:
        start_measure(mea)

    # 2) Attendre que les signaux AI-Core soient lisibles
    if not wait_for_signals(sys, timeout_s=WAIT_SIGNALS_TIMEOUT_S, poll=POLL_PERIOD_S):
        stop_everything(tst, mea)
        raise SystemExit(1)

    # 3) Polling live
    print(f"[INFO] Lecture des signaux pendant {POLL_DURATION_S} s ...")
    live = poll_ai_core_results(sys, duration_s=POLL_DURATION_S, period_s=POLL_PERIOD_S)

    # 4) Stop
    stop_everything(tst, mea)

    # 5) Comparaison et exports
    ref = load_reference_results(REF_JSON)
    comp = compare_results(live, ref)
    save_report_csv(comp, CSV_OUT)
    save_report_json(comp, CSV_OUT.with_suffix(".json"))

    print("[✅] Exécution terminée (acquisition + comparaison + export).")
