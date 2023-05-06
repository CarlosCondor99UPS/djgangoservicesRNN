from django.shortcuts import render
# para utilizar el método inteligente
from appSentimientos.Logica import modeloSNN
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import render
import json
from django.http import JsonResponse


class Clasificacion():
    def determinarAprobacion(request):
        return render(request, "prediccionSentimiento.html")
    
    @api_view(['GET', 'POST'])

    def predecir(request):
        try:
            comentario =  str (request.POST.get('comentario'))
            resul = modeloSNN.modeloSNN.predecirNuevoSentimiento(modeloSNN.modeloSNN,COMENTARIO=comentario)
        except Exception as e:
            resul = f"Error: {str(e)}"
        
        return render(request, "informe.html", {"e": resul})
    @csrf_exempt

    @api_view(['GET', 'POST'])
    def predecirIOJson(request):
        print(request)
        print('***')
        print(request.body)
        print('***')
        body = json.loads(request.body.decode('utf-8'))
        # Formato de datos de entrada
        comentario = str(body.get("comentario"))
        resul = modeloSNN.modeloSNN.predecirNuevoCliente(modeloSNN.modeloSNN, comentario=comentario)
        data = {'result': resul}
        resp = JsonResponse(data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp
