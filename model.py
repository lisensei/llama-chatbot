from langchain_community.llms import LlamaCpp
def get_model(path):
    model=LlamaCpp(model_path=path,n_gpu_layers=-1,n_ctx=4096)
    return model