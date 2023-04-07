from keras.models import load_model
import constant.path.localpath as LocalPath
import constant.path.serverpath as ServerPath

def model_load():
    #local
    model, fa_path, gochu_path, kong_path, mu_path, bachu_path = LocalPath.localPath()
    #server
    #model, fa_path, gochu_path, kong_path, mu_path, bachu_path = ServerPath.serverPath()

    model = load_model(model)
    fa_model = load_model(fa_path)
    gochu_model = load_model(gochu_path)
    kong_model = load_model(kong_path)
    mu_model = load_model(mu_path)
    bachu_model = load_model(bachu_path)
    return model, fa_model, gochu_model, kong_model, mu_model, bachu_model