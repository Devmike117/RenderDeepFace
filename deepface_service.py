from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
import os
import tempfile

app = FastAPI(title="DeepFace Embedding Service (Optimizado)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Servicio activo", "endpoint": "/generate_embedding"}

@app.post("/generate_embedding/")
async def generate_embedding(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado")

    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Usar modelo ligero y forzar CPU
        result = DeepFace.represent(
            img_path=tmp_path,
            model_name='OpenFace',  # Más ligero que Facenet
            enforce_detection=True,
            enforce_cpu=True        # Evita inicializar CUDA
        )

        if not result or len(result) == 0:
            raise HTTPException(status_code=400, detail="No se detectó ninguna cara en la imagen")

        embedding_vector = result[0]["embedding"]
        embedding_list = embedding_vector if isinstance(embedding_vector, list) else embedding_vector.tolist()

        return {
            "embedding": embedding_list,
            "model": "OpenFace",
            "dimensions": len(embedding_list)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando embedding: {str(e)}")

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)




