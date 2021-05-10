import yaml
run = False
if not run:
    with open('./config/config.yaml', 'r') as f:
        data = f.read()
        config_data = yaml.load(data)
    run = True