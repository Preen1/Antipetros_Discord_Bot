import os
import importlib.util
import inspect

SUB_SUPPORT_DIR = os.path.abspath(os.path.dirname(__file__))
if os.path.islink(SUB_SUPPORT_DIR) is True:

    SUB_SUPPORT_DIR = os.readlink(SUB_SUPPORT_DIR).replace('\\\\?\\', '')


def module_files():
    for file in os.scandir(SUB_SUPPORT_DIR):
        if file.is_file() and file.name != '__init__.py':
            module_name = file.name.removesuffix('.py')
            yield module_name, file.path


def _get_class_from_module(in_module):
    return in_module.get_class()


def _import_sub_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    _module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_module)
    return _get_class_from_module(_module)


def collect_sub_support_classes():
    class_list = []
    for module_name, file_path in module_files():
        sub_support_class = _import_sub_module(module_name, file_path)
        if sub_support_class not in class_list:
            class_list.append(sub_support_class)
    return class_list


SUB_SUPPORT_CLASSES = collect_sub_support_classes()
