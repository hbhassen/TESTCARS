import time
import json
from pathlib import Path
from difflib import SequenceMatcher
import grpc

import testautomation_pb2 as ta
import testautomation_pb2_grpc as ta_grpc

# ========= CONFIG =========
GRPC_ADDR = "localhost:50051"
ROOT_NODE = "AICORE"   # Doit correspondre au Root Node dans AI-Core
TEST_NAME = "DetectMode_AutoTest"  # Nom logique du test si ton proto le supporte
TEST_CFG = r"C:/Users/py13733/modeTo/DetectModeTest/DetectModeTest.testcfg"  # utilisé SEULEMENT si le proto expose un champ approprié
REF_JSON = Path(r"C:/Users/py13733/modeTo/DetectModeTest/testso.json")
CSV_OUT  = Path(r"./detectmode_run01.csv")

# Signaux cibles (adapte-les si ton arbo change)
SIG_RESULT = "IconDetection.Result"
SIG_SCORE  = "IconDetection.Score"
SIG_CNTNT  = "IconDetection.Content"

# ========= OUTILS =========
def has_field(msg_cls, field_name: str) -> bool:
    """Vérifie si un champ existe dans un message Protobuf généré."""
    return field_name in msg_cls.DESCRIPTOR.fields_by_name

def connect():
    ch  = grpc.insecure_channel(GRPC_ADDR)
    app = ta_grpc.ApplicationStub(ch) if hasattr(ta_grpc, "ApplicationStub") else None
    sys = ta_grpc.SystemStub(ch)       if hasattr(ta_grpc, "SystemStub")       else None
    mea = ta_grpc.MeasureStub(ch)      if hasattr(ta_grpc, "MeasureStub")      else None

    # Le service qui contient StartTesting peut s'appeler différemment selon les .proto
    # On essaye plusieurs stubs possibles :
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
        print("[WARN] Pas de service Application.Init dans ce proto.")

# ========= LANCEMENT TEST =========
def build_start_test_request():
    """
    Construit un StartTestRequest en ne renseignant QUE les champs qui existent réellement
    dans ton testautomation_pb2.py (évite ValueError: field inexistant).
    """
    if not hasattr(ta, "StartTestRequest"):
        return None

    req = ta.StartTestRequest()

    # Nom du test / modèle : on tente plusieurs variantes de champ
    for field in ["model", "strModelName", "testName", "strTestName", "name"]:
        if has_field(ta.StartTestRequest, field):
            setattr(req, field, TEST_NAME)
            break

    # Fichier de config : on tente plusieurs variantes ; on n'utilise PAS strConfigFile
    for field in ["configFile", "strConfig", "testConfigPath", "config_path"]:
        if has_field(ta.StartTestRequest, field):
            setattr(req, field, TEST_CFG)
            break

    return req

def start_test(tst):
    """
    Essaye d'appeler StartTesting sur le service disponible, sinon fallback:
    - démarrage de mesure (Measure.Start) si exposé,
    - ou simple attente des signaux si AI-Core est déjà lancé via TA.
    """
    if not tst:
        print("[WARN] Aucun stub 'test' disponible. On passera en fallback Measure.Start.")
        return False

    # Prépare la requête si le message existe
    request = build_start_test_request() if hasattr(ta, "StartTestRequest") else None

    # Tente StartTesting sur la méthode existante (nom selon proto)
    for meth_name in ["StartTesting", "StartTest", "Start"]:
        if hasattr(tst, meth_name):
            print(f"[INFO] Tentative de lancement via {meth_name}...")
            if request:
                res = getattr(tst, meth_name)(request)
            else:
                # S'il n'y a pas de message StartTestRequest, on tente un Empty()
                empty = ta.Empty() if hasattr(ta, "Empty") else None
                res = getattr(tst, meth_name)(empty) if empty else getattr(tst, meth_name)(ta.ApplicationInitRequest())
            # Si le message de retour a (success/message), on trace
            if hasattr(res, "success") and not res.success:
                print(f"[ERREUR] {meth_name} a échoué : {getattr(res, 'message', '(sans message)')}")
                return False
            print(f"[OK] Lancement via {meth_name}.")
            return True

    print("[WARN] Aucune méthode StartTesting/StartTest/Start trouvée sur ce service.")
    return False

def stop_test(tst, mea=None):
    # Essaye StopTesting ; sinon fallback Measure.Stop
    if tst:
        for meth in ["StopTesting", "StopTest", "Stop"]:
            if hasattr(tst, meth):
                getattr(tst, meth)(ta.StopTestRequest() if hasattr(ta, "StopTestRequest") else ta.ApplicationInitRequest())
                print(f"[OK] Test arrêté via {meth}.")
                return
    if mea and hasattr(mea, "Stop"):
        mea.Stop(ta.MeasureStopRequest())
        print("[OK] Mesure arrêtée (fallback Measure.Stop).")

# ========= MESURE =========
def ensure_measure_started(mea):
    """
    Fallback si StartTesting n'existe pas : démarre directement l'acquisition via Measure.
    """
    if not mea:
        return False

    # SetVideoAudio si dispo (pour source vidéo nommée côté config)
    if hasattr(mea, "SetVideoAudio") and hasattr(ta, "MeasureSetVideoAudioRequest"):
        mea.SetVideoAudio(ta.MeasureSetVideoAudioRequest(
            strName="FrontCam",  # adapte si ta source a un autre nom
            bActivate=True,
            bPauseVideoInitially=False,
            bPauseAudioInitially=False
        ))
        print("[INFO] Source vidéo activée (Measure.SetVideoAudio).")

    if hasattr(mea, "Start") and hasattr(ta, "MeasureStartRequest"):
        mea.Start(ta.MeasureStartRequest())
        print("[OK] Mesure démarrée (Measure.Start).")
        return True

    print("[WARN] Impossible de démarrer la mesure (pas de Measure.Start).")
    return False

def wait_for_signals(sys, timeout_s=20, poll=0.5):
    """
    Attend que les signaux AICORE.* deviennent lisibles (connection AI-Core établie).
    """
    if not sys:
        print("[WARN] Pas de service SystemStub.")
        return False

    t0 = time.time()
    path = f"{ROOT_NODE}.{SIG_SCORE}"
    while time.time() - t0 < timeout_s:
        try:
            val = sys.GetSignal(ta.SystemGetSignalRequest(strSignalName=path, bInterpreted=True)).RetVal_double
            # Si on arrive à lire un double sans exception, la comm est OK
            print(f"[INFO] Signal lisible: {path} → {val:.3f}")
            return True
        except Exception as e:
            time.sleep(poll)
    print("[ERREUR] Timeout d’attente des signaux AICORE.")
    return False

def poll_ai_core_results(sys, duration_s=10, period_s=0.5):
    rows = []
    t0 = time.time()
    while time.time() - t0 < duration_s:
        try:
            res = sys.GetSignal(ta.SystemGetSignalRequest(
                strSignalName=f"{ROOT_NODE}.{SIG_RESULT}", bInterpreted=True
            )).RetVal_string

            score = sys.GetSignal(ta.SystemGetSignalRequest(
                strSignalName=f"{ROOT_NODE}.{SIG_SCORE}", bInterpreted=True
            )).RetVal_double

            content = ""
            # Content n'existe pas dans toutes les configs — on tente prudemment
            try:
                content = sys.GetSignal(ta.SystemGetSignalRequest(
                    strSignalName=f"{ROOT_NODE}.{SIG_CNTNT}", bInterpreted=True
                )).RetVal_string
            except Exception:
                content = ""

            frame = round(time.time() - t0, 2)
            rows.append({"Frame": frame, "Detected": res.strip(), "Score": round(score, 3), "Content": content.strip()})
            print(f"[Frame {frame}] {res} (score={score:.2f})")
        except Exception as e:
            print(f"[WARN] Lecture signal échouée : {e}")
        time.sleep(period_s)
    return rows

# ========= COMPARAISON =========
def load_reference_results(path: Path):
    if not path.exists():
        print(f"[WARN] Fichier de référence absent: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"[INFO] {len(data)} entrées de référence chargées depuis {path.name}")
    return data

def compare_results(live, ref):
    def similarity(a, b):
        return SequenceMatcher(None, a or "", b or "").ratio()

    out = []
    for i, frame in enumerate(live):
        if i < len(ref):
            expected = (ref[i].get("Result") or "").strip()
            detected = (frame.get("Detected") or "").strip()
            sim = similarity(expected, detected)
            match = "OK" if sim >= 0.9 else "DIFF"
            score_live = float(frame.get("Score", 0) or 0)
            score_ref  = float(ref[i].get("Score", 0) or 0)
            out.append({
                "Frame": i,
                "Expected": expected,
                "Detected": detected,
                "Match": match,
                "Similarity": round(sim, 2),
                "ScoreDiff": round(abs(score_live - score_ref), 3)
            })
        else:
            out.append({"Frame": i, "Expected": "N/A", "Detected": frame.get("Detected"), "Match": "EXTRA",
                        "Similarity": 0.0, "ScoreDiff": "-"})
    return out

def save_report_csv(data, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("Frame,Expected,Detected,Match,Similarity,ScoreDiff\n")
        for d in data:
            f.write(f"{d['Frame']},{d['Expected']},{d['Detected']},{d['Match']},{d['Similarity']},{d['ScoreDiff']}\n")
    print(f"[INFO] Rapport CSV exporté → {path}")

def save_report_json(data, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[INFO] Rapport JSON exporté → {path}")

# ========= MAIN =========
if __name__ == "__main__":
    app, sys, mea, tst = connect()
    init_app(app)

    launched = start_test(tst)
    if not launched:
        # Fallback si pas de StartTesting dans ce proto : on tente via Measure.*
        launched = ensure_measure_started(mea)

    # Attente que les signaux deviennent lisibles (AI-Core chargé, modèle up)
    if not wait_for_signals(sys, timeout_s=30, poll=0.5):
        # On arrête proprement si possible
        try:
            stop_test(tst, mea)
        except Exception:
            pass
        raise SystemExit(1)

    print("[INFO] Lecture des signaux pendant 20 secondes...")
    live = poll_ai_core_results(sys, duration_s=20, period_s=0.5)

    # Stop (peu importe la voie utilisée)
    try:
        stop_test(tst, mea)
    except Exception:
        pass

    ref = load_reference_results(REF_JSON)
    comp = compare_results(live, ref)

    save_report_csv(comp, CSV_OUT)
    save_report_json(comp, CSV_OUT.with_suffix(".json"))

    print("[✅] Test terminé et comparé avec succès.")
