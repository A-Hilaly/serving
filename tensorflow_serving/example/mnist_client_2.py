import argparse
import time
import numpy as np
from grpc.beta import implementations
from tensorflow.contrib.util import make_tensor_proto

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from scipy.misc import imread, imresize


def run(host, port, image, model, signature_name):

    # channel = grpc.insecure_channel('%s:%d' % (host, port))
    channel = implementations.insecure_channel(host, port)
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    # Read an image
    data = imread(image)
    data = imresize(data, [28, 28])
    data = data.astype(np.float32)
    print(len(data))
    start = time.time()

    # Call classification model to make prediction on the image
    request = predict_pb2.PredictRequest()
    request.model_spec.name = model
    request.model_spec.signature_name = signature_name
    request.inputs['images'].CopyFrom(make_tensor_proto(data, shape=[1, 784]))

    result = stub.Predict(request, 10.0)

    end = time.time()
    time_diff = end - start

    # Reference:
    # How to access nested values
    # https://stackoverflow.com/questions/44785847/how-to-retrieve-float-val-from-a-predictresponse-object
    print(result)
    print('time elapased: {}'.format(time_diff))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Tensorflow server host name', default='localhost', type=str)
    parser.add_argument('--port', help='Tensorflow server port number', default=9000, type=int)
    parser.add_argument('--image', help='input image', type=str)
    parser.add_argument('--model', help='model name', default='mnist', type=str)
    parser.add_argument('--signature_name', default="predict_images",help='Signature name of saved TF model', type=str)

    args = parser.parse_args()
    run(args.host, args.port, args.image, args.model, args.signature_name)
