import yaml

from test import Config

if __name__ == '__main__':
    conf = None
    with open('config.yaml') as fh:
        conf = Config(**yaml.safe_load(fh))
    assert conf is not None
    assert isinstance(conf, Config)
    print(conf)
    print(conf.handlers.one)
