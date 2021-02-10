import PIL
from PIL import Image
import pyarmnn as ann
import numpy as np
import cv2
import os

print(f"Working with ARMNN {ann.ARMNN_VERSION}")

# ONNX, Caffe and TF parsers also exist.
parser = ann.ITfLiteParser()  

network = parser.CreateNetworkFromBinaryFile('./mnist_model.tflite')

graph_id = parser.GetSubgraphCount() - 1
print("Graph Id:", graph_id)

input_names = parser.GetSubgraphInputTensorNames(graph_id)
print("Input Names: ",input_names)

input_binding_info = parser.GetNetworkInputBindingInfo(graph_id, input_names[0])

input_tensor_id = input_binding_info[0]
input_tensor_info = input_binding_info[1]

print(f"""
tensor id: {input_tensor_id}, 
tensor info: {input_tensor_info}
""")

# Create a runtime object that will perform inference.
options = ann.CreationOptions()
runtime = ann.IRuntime(options)

# Backend choices earlier in the list have higher preference.
preferredBackends = [ann.BackendId('CpuAcc'), ann.BackendId('CpuRef')]

opt_network, messages = ann.Optimize(network, preferredBackends, runtime.GetDeviceSpec(), ann.OptimizerOptions())

# Load the optimized network into the runtime.
net_id, _ = runtime.LoadNetwork(opt_network)
print(f"Loaded network, id={net_id}")

image_dict = {}
for image_name in os.listdir('./images'):
    img_path = f'./images/{image_name}'
    
    print(f"Actual Image : {img_path}")
    image = cv2.imread(img_path, 0)
    
    image = np.array(image, dtype=np.float32) / 255.0

    # Create an inputTensor for inference.
    input_tensors = ann.make_input_tensors([input_binding_info], [image])

    # Get output binding information for an output layer by using the layer name.
    output_names = parser.GetSubgraphOutputTensorNames(graph_id)
    output_binding_info = parser.GetNetworkOutputBindingInfo(0, output_names[0])
    output_tensors = ann.make_output_tensors([output_binding_info])
    runtime.EnqueueWorkload(0, input_tensors, output_tensors)

    out_tensor = ann.workload_tensors_to_ndarray(output_tensors)[0][0]
    results = np.argsort(out_tensor)[::-1]
    print("=#="*30)
    print(f"[RESULT] Actual Character : {image_name.split('.')[0]} | Predicted Value : {results[0]}")
    print("=#="*30)

    image_dict[results[0]] = image
    
try:
    for key in image_dict.keys():
        cv2.imshow(f"Predicted Label : {key}", image_dict[key])

    cv2.waitKey(5000)
    cv2.destroyAllWindows()
except KeyboardInterrupt:
    cv2.destroyAllWindows()
