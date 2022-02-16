from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework import status
from mydarknet.python.darknet import load_net, load_image, load_meta, detect
from pathlib import Path
from .models import ImageModel
import subprocess

darknet = Path(__file__).parent.parent/'mydarknet'
yolo_path = darknet/'config/yolov3-vertebrae.cfg'
yolo_weights = darknet/'yolov3-vertebrae_final.weights'
vertebrae_data = darknet/'config/vertebrae.data'

net = load_net(bytes(yolo_path), bytes(yolo_weights), 0)
meta = load_meta(bytes(vertebrae_data))


@parser_classes((MultiPartParser,))
class ImageDetectorView(APIView):

    def post(self, request, format=None):
        im = request.FILES["file"]
        # print(im)
    
        image = ImageModel.objects.create(image=im, name=im.name)
 
        r = detect(net, meta, bytes(darknet.parent/'images'/image.name))
        if r:
            # print(r)
            subprocess.run(["rm", darknet.parent/'images'/image.name])
            return Response(r, status=status.HTTP_200_OK)
        return Response({"msg": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        

class ImageDetectorReturnImage(APIView):

    def post(self, request, format=None):

        im = request.FILES["file"]
        image = ImageModel.objects.create(image=im, name=im.name)
        r = detect(net, meta, bytes(darknet.parent/'images'/image.name))
        # print(r)
        return Response(r)

# Create your views here.
