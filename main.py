import sys
import os
import json

NODE_MODULES = 'node_modules'
PACKAGE = 'package.json'
ADDITION_KEY = 'publishConfig'
ADDITION = {
    'registry': 'http://sonatype-nexus.livetex.ru/nexus/content/repositories/livetex-npm/'
}


def main(args):
    process_module(os.getcwd(), root=True)


def process_module(path, root=False):
    if not root:
        add_package_addition(path)
        publish(path)

    for module in ls_node_modules(path):
        process_module(module)


def ls_node_modules(path):
    module_container = os.path.join(path, NODE_MODULES)
    if os.path.isdir(module_container):
        result = [os.path.join(path, NODE_MODULES, i) for i in os.listdir(module_container)]
        return [i for i in result if is_module(i)]
    return []


def is_module(path):
    result = os.path.isdir(path)
    return result & os.path.isfile(os.path.join(path, PACKAGE))


def add_package_addition(path):
    package = os.path.join(path, PACKAGE)

    f = file(package)
    data = json.load(f)
    data[ADDITION_KEY] = ADDITION
    f.close()

    f = open(package, 'w')
    f.write(json.dumps(data))
    f.close()


def publish(path):
    os.system('npm publish ' + path)

if __name__ == '__main__':
    main(sys.argv[1:])
