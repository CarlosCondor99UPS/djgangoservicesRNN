from django.urls import reverse
import pandas as pd
from sklearn.pipeline import Pipeline
from tensorflow.python.keras.models import load_model, model_from_json
from keras import backend as K
from appSentimientos.Logica import modeloSNN
import pickle


class modeloSNN():

    
    """Clase modelo Preprocesamiento y SNN"""
    # Función para cargar preprocesador
    def cargarPipeline(self, nombreArchivo):
        with open(nombreArchivo+'.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline
    # Función para cargar red neuronal
    def cargarNN(self, nombreArchivo):
        model = load_model(nombreArchivo+'.h5')
        print("Red Neuronal Cargada desde Archivo")
        return model
    # Función para integrar el preprocesador y la red neuronal en un Pipeline

    def cargarModelo(self):
        # Se carga el Pipeline de Preprocesamiento
        nombreArchivoPreprocesador = 'Recursos/Transformador'
        pipe = self.cargarPipeline(self, nombreArchivoPreprocesador)
        print('Pipeline de Preprocesamiento Cargado')
        cantidadPasos = len(pipe.steps)
        print("Cantidad de pasos: ", cantidadPasos)
        print(pipe.steps)
        # Se carga la Red Neuronal
        modeloOptimizado = self.cargarNN(self, 'Recursos/modelo_keras')
        # Se integra la Red Neuronal al final del Pipeline
        pipe.steps.append(['modelNN', modeloOptimizado])
        cantidadPasos = len(pipe.steps)
        print("Cantidad de pasos: ", cantidadPasos)
        print(pipe.steps)
        print('Red Neuronal integrada al Pipeline')
        return pipe


    def predecirNuevoSentimiento(self, COMENTARIO):
        c=[COMENTARIO]
        df = pd.DataFrame(data=[c],columns=['COMENTARIO'])
        with open('Recursos/Transformador.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        X_new = pipeline.transform(df)
        model = load_model('Recursos/modelo_keras.h5')
        pred_sent = model.predict(X_new) 
        prediccion = pd.DataFrame(pred_sent, columns=['MAL', 'BIEN', 'EXCELENTE'])
        prediccion = prediccion.astype(float)

        if (prediccion.loc[0, 'MAL']>prediccion.loc[0, 'BIEN'] and prediccion.loc[0, 'MAL']>prediccion.loc[0, 'EXCELENTE']):
            respuesta='Lamentamos por tu mala experiencia, espero que consideres retomar el servicio nuevamente.'

        elif (prediccion.loc[0, 'BIEN']>prediccion.loc[0, 'MAL'] and prediccion.loc[0, 'BIEN']>prediccion.loc[0, 'EXCELENTE']):
            respuesta='Gracias por tu comentario,  nos alegra saber que disfrutó de su experiencia en nuestro negocio y que nuestro equipo pudo satisfacer sus expectativas.'
        else:
            respuesta='Gracias por tu comentario,  nos alegra saber que disfrutó de su experiencia en nuestro negocio y que nuestro equipo pudo satisfacer sus expectativas.'
        return str(respuesta)
    
