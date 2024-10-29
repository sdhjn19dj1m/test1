import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

def build_engine(model_path):
    with trt.Builder(TRT_LOGGER) as builder, builder.create_network() as network, trt.OnnxParser(network, TRT_LOGGER) as parser:
        builder.max_workspace_size = 1 << 30  # 1 GiB
        builder.max_batch_size = 1
        with open(model_path, 'rb') as model:
            if not parser.parse(model.read()):
                print('Failed to parse the ONNX file.')
                for error in range(parser.num_errors):
                    print(parser.get_error(error))
                return None
        return builder.build_cuda_engine(network)

def allocate_buffers(engine):
    inputs = []
    outputs = []
    bindings = []
    stream = cuda.Stream()
    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        host_mem = cuda.pagelocked_empty(size, dtype)
        device_mem = cuda.mem_alloc(host_mem.nbytes)
        bindings.append(int(device_mem))
        if engine.binding_is_input(binding):
            inputs.append(HostDeviceMem(host_mem, device_mem))
        else:
            outputs.append(HostDeviceMem(host_mem, device_mem))
    return inputs, outputs, bindings, stream

class HostDeviceMem:
    def __init__(self, host_mem, device_mem):
        self.host = host_mem
        self.device = device_mem

def infer(engine, input_data):
    inputs, outputs, bindings, stream = allocate_buffers(engine)
    np.copyto(inputs[0].host, input_data.ravel())
    [cuda.memcpy_htod_async(inp.device, inp.host, stream) for inp in inputs]
    engine_context = engine.create_execution_context()
    engine_context.execute_async(bindings=bindings, stream_handle=stream.handle)
    [cuda.memcpy_dtoh_async(out.host, out.device, stream) for out in outputs]
    stream.synchronize()
    return [out.host for out in outputs]

if __name__ == "__main__":
    model_path = "src/models/large_language_model.onnx"
    engine = build_engine(model_path)
    if engine is None:
        print("Failed to build the engine.")
    else:
        # 示例輸入數據，這裡使用隨機數據
        input_data = np.random.random((1, 3, 224, 224)).astype(np.float32)
        output = infer(engine, input_data)
        print("Inference output:", output)
