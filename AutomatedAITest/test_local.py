import time
import grpc
from pathlib import Path

import testautomation_pb2 as ta
import testautomation_pb2_grpc as ta_grpc

GRPC_ADDR = "localhost:50051"
ROOT_NODE = "AICORE"  # ou "Model" selon votre config AI-Core
MODEL_CFG = r"D:\DetectMode\model.modelcfg"  # si vous forcez un SwitchModel
CSV_OUT   = Path(r"D:\results\detectmode_run01.csv")

def connect():
    ch = grpc.insecure_channel(GRPC_ADDR)
    app = ta_grpc.ApplicationStub(ch)
    sys = ta_grpc.SystemStub(ch)
    mea = ta_grpc.MeasureStub(ch)
    return app, sys, mea

def init_app(app):
    app.Init(ta.ApplicationInitRequest())

def switch_model_if_needed(sys):
    # Optionnel: forcer le modèle (sinon sauter cette étape si géré par la test config AI-Core)
    req = ta.SystemModifyModelNodeConfigRequest(
        strModelNodeName=ROOT_NODE,
        strConfig=f"SwitchModel IconDetection '{MODEL_CFG}'",
        lTimeoutInSeconds=45
    )
    sys.ModifyModelNodeConfig(req)

def start_measure(mea):
    # Activer la vidéo/av si nommé côté config
    mea.SetVideoAudio(ta.MeasureSetVideoAudioRequest(
        strName="LocalVideo",         # Adapter au nom de la source si nécessaire
        bActivate=True,
        bPauseVideoInitially=False,
        bPauseAudioInitially=False
    ))
    mea.Start(ta.MeasureStartRequest())

def poll_signals(sys, duration_s=10, period_s=0.2):
    rows = [("t", "Result", "Score")]
    t0 = time.time()
    while time.time() - t0 < duration_s:
        res  = sys.GetSignal(ta.SystemGetSignalRequest(
            strSignalName=f"{ROOT_NODE}.IconDetection.Result", bInterpreted=True
        )).RetVal_string
        score = sys.GetSignal(ta.SystemGetSignalRequest(
            strSignalName=f"{ROOT_NODE}.IconDetection.Score", bInterpreted=True
        )).RetVal_double
        rows.append((f"{time.time()-t0:.2f}", res, f"{score:.3f}"))
        time.sleep(period_s)
    return rows

def stop_measure(mea):
    mea.Stop(ta.MeasureStopRequest())

def save_csv(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join([",".join(map(str, r)) for r in rows]), encoding="utf-8")

if __name__ == "__main__":
    app, sys, mea = connect()
    init_app(app)

    # Optionnel: forcer un modèle précis (sinon commenter)
    # switch_model_if_needed(sys)

    start_measure(mea)
    rows = poll_signals(sys, duration_s=15, period_s=0.2)
    stop_measure(mea)

    # Option 1: sauvegarde par TA (si support CSV actif côté TA)
    # mea.SaveFile(ta.MeasureSaveFileRequest(
    #     strLabel="DetectMode_Run_01", strType="CSV",
    #     strFileName=str(CSV_OUT)
    # ))

    # Option 2: CSV côté Python
    save_csv(rows, CSV_OUT)
    print(f"Résultats exportés: {CSV_OUT}")
